function draw(geo_data, current_filename) {

  "use strict";
  var margin = 0,
      width = 960 - margin,
      height = 850 - margin;

  var svg = d3.select("body")
      .append("svg")
      .attr("width", width + margin)
      .attr("height", height + margin)
      .append('g')
      .attr('class', 'map');

  var projection = d3.geo.mercator()
                         .scale(9000)
                         .center([8.03667, 46.70111]) // because of scroll, not perfectly centered on CH
                         .translate( [width / 2, height / 2]);

  var path = d3.geo.path().projection(projection);

  var map = svg.selectAll('path')
               .data(geo_data.features)
               .enter()
               .append('path')
               .attr('d', path)
               .style('fill', 'white')
               .style('stroke', 'black')
               .style('stroke-width', 0.5);

  function plot_points(data) {
      
      // Find the maximum weight among all nodes 
      var weight_max = d3.max(data, function(node) {
          return node['weight'];
      });

      // Scale the radius so that circles are visible if if they have extreme weights 
      var radius = d3.scale.sqrt()
                     .domain([0, weight_max])
                     .range([0, 15]);

      // Draw circles
      svg.append('svg')
         .attr("class", "bubble")
         .selectAll("circle")
         .data(data)
         .enter()
         .append("circle")
         .attr('cx', function(node) { 
            return projection([node['longitude'], node['latitude']])[0]; 
          })
         .attr('cy', function(node) { 
            return projection([node['longitude'], node['latitude']])[1]; 
          })
         .attr('r', function(node) {
              return radius(node['weight']);
         })
         .attr('fill', 'rgb(247, 148, 32)')
         .attr('stroke', 'black')
         .attr('stroke-width', 0.7)
         .attr('opacity', 0.7);

      // Write node name on top
      svg.selectAll("text")
         .data(data)
         .enter()
         .append("text")
         .attr("x", function(node) { 
           // The node's name is placed on its right side 
           return projection([node['longitude'], node['latitude']])[0] + radius(node['weight']) + 1; 
         })
         .attr("y", function(node) {  
           return projection([node['longitude'], node['latitude']])[1];
         })
         .text( function (node) { 
          return node['name']; 
         })
         .attr("font-family", "sans-serif")
         .attr("font-size", "15px")
         .attr("fill", "black");
         
  }

  function plot_flows(data) {

    // Define the reusable arrow tip
    svg.append("svg:defs") 
        .append("svg:marker") 
        .attr("id", "triangle") 
        .attr("refX", 6) 
        .attr("refY", 6)
        .attr("markerWidth", 30)
        .attr("markerHeight", 30)
        .attr("orient", "auto") 
        .append("path")
        .attr("d", "M 0 0 12 6 0 12 3 6") 
        .style("fill", "black"); 

    // Plot the lines programatically
    svg.selectAll("line")
       .data(data)
       .enter()
       .append("line")
       .attr("x1", function(flow) { 
         var orientation = flow['src_longitude'] - flow['dest_longitude'];
         if(orientation < 0) {
          return projection([flow['src_longitude'], flow['src_latitude']])[0] - 5; 
         } else {
          return projection([flow['src_longitude'], flow['src_latitude']])[0] + 5;
         }
       })
       .attr("y1", function(flow) {  
         return projection([flow['src_longitude'], flow['src_latitude']])[1];
       })
       .attr("x2", function(flow) {  
         var orientation = flow['src_longitude'] - flow['dest_longitude'];
         if(orientation < 0) {
          return projection([flow['dest_longitude'], flow['dest_latitude']])[0] - 5; 
         } else {
          return projection([flow['dest_longitude'], flow['dest_latitude']])[0] + 5;
         }
       })
       .attr("y2", function(flow) {  
         return projection([flow['dest_longitude'], flow['dest_latitude']])[1];
       })
       .attr("stroke-width", 1)
       .attr("stroke", "black")
       .attr("marker-end", "url(#triangle)");

  }

  // Load the nodes and plot them 
  d3.tsv("dummy_nodes.tsv", function(d) {
    return d;
  }, plot_points);

  // Load the flows and plot them 
  d3.tsv(current_filename, function(d) {
    return d;
  }, plot_flows);

};