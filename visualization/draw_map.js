// Plot the nodes and their label
function plot_nodes(data) {

    console.log(data);
    
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
       .attr('opacity', 0.7); // make the nodes translucid in case they overlap

    // Write node label on top
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
       .attr("font-size", "5px")
       .attr("fill", "black");
       
};

// Draws the map, the nodes and the flows
function draw(geo_data) {
      "use strict";
      var margin = 75,
          width = 1400 - margin,
          height = 600 - margin;

      var svg = d3.select("body")
          .append("svg")
          .attr("width", width + margin)
          .attr("height", height + margin)
          .append('g')
          .attr('class', 'map');

      var projection = d3.geo.mercator()
                             .scale(5000)
                             .center([9.02667, 46.40111]) // because of scroll, not perfectly centered on CH
                             .translate( [width / 2, height / 2]);

      var path = d3.geo.path().projection(projection);

      var map = svg.selectAll('path')
                   .data(geo_data.features)
                   .enter()
                   .append('path')
                   .attr('d', path)
                   .style('fill', 'lightBlue')
                   .style('stroke', 'black')
                   .style('stroke-width', 0.5);

      // Load the nodes and plot them 
      d3.tsv("nodes.tsv", function(d) {
        return d;
      }, plot_nodes);

};

