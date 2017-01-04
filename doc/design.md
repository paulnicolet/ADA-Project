# Design
This document presents a rough idea about the design we plan to implement.

## End goal
We start by describing the desired end product.

The product of this study should represent flows in Switzerland. 
Flows are very likely to vary depending on the date and time of the tweets, as well as various
events, such as the opening of a new freeway... Thus, the representation of those flows should take all those factors into account.
In order to visualize these flows in a clear way, we choose to create an interface with a dynamic representation of the flows. 




![flows](assets/product_example.png)




The image above represents an idea of what the end product should look like. Of course, our map will be scaled so that only relevant areas are represented (Switzerland, and part of its neighboring coutries).
The visualization should convey the same ideas:
- The importance of the flow (shown by the thickness of the lines)
- The nature of the flow (shown by the starting point and the color of the lines)

In addition, additional tools should enable users to visualize flows at different point in time (date, time, special event). The time scale would depend on the data, which is not necessarly accurate enough to be able to see short terms movements. 


## Thinking about Flows 

**People flow**: refers to numerous people moving around buildings, around cities or across borders. 

**Question** : what kind of flows are we interested in ?

![flows](assets/flows.png)

* Option 1 represents a big flows between two mains geographical nodes, in our context we can imagine nodes as cities. 
* Option 2 represents several individual flows comming from small places to one main node (we can also imagine little flows from a main nodes to smaller places).

Given the pretty large geographical zone we have to consider, it doesn't really scale, or even make sense to look into individual moves of people to a same node. We should probably limit our analysis to movement between important points of Switzerland, as modeled by *figure 1*.

## Modeling Flows
### Nodes
If we consider a flow as a being movement from a node to another, we need to decide what is a node. 

It makes sense here to considere cities as nodes, and so detect movement between cities. Of course we still need to decide what cities are large enough to be able to add more information in our analysis.

### Edges
There are two ways to think of links between nodes : 

* An edge represents only movement between two nodes, without geographical significance. 
* An edge also brings geographical information about the flow between two nodes. 

More concretely, in the current context, the question is : *should we consider roads between cities ?*

Intuitively, it would make sense, given it brings more precise information of the flow, by knowing with path people exactly take.

Now we have to keep in mind that our analysis is based on tweets, which needs either a laptop or a smartphone to be posted, and it seems reasonable to consider that people *don't text and drive*. So if one can tweet in city A, and later in the day in city B, there is very little chance that one tweets while traveling from A to B. 
*But*, driving is not the only way to travel in Switzerland, it's absolutely fine to post a tweet in the train, so this could be a good reason to look into intermediate tweets, which could gives us information about the use of train lines, given that there is a chance that most people not professionaly active (16 - 25 years old), -or even some active people- take the train on a daily basis. 

## Detecting Flows
### Detection strategy 
*When can we say that someone is moving in a flow ?*

- Someone is moving if we can find tweets in different locations, with a time relation.
- A flow should not be determined by only one person. Assuming the path of one person at a certain time, we need to see whether several people use the same path.
- There are two main time relations between tweets of the same person, the strategy can be adapted during the process :
	- If a lot of tweets are actually posted the same day, there is an easy way to detect flows in a small time scale, and an easy way to predict the direction of the flow, using the earliest tweet as starting point (assuming that a majority of people start moving in the morning).
	- If tweets are actually spread over days, we can suppose there is a flow if the location is changing, but it is not easy to predict the direction.

*When can we say that a flow is significant ?*

- A flow is significant when it is used by a minimum number of people. 
- The specific minimum should be determined by tests. A potential test would consist in visualizing the map with different minimums. Eligible minimum should yield maps which display great information, without being bloated.

### Detecting cities
*Given a point (longitude, latitude), how can we find the corresponding node ?*

- A tweet is associated to a node by using a **nearest neighbor** method.
	- See [geonames downloads](http://download.geonames.org/export/dump/) for coordinates of main locations in Switzerland.
- A node is determined by its center, and includes all points situated within its diameter. 
- The diameter of a node ideally depends on the surface on which the city is spread. It might not be easy to find the actual surface of cities, in which case we could simplify our model to base the surface on the population.
- Consequently, certain points (absence of nearby city) will not be considered.

*Which cities to consider ? Which population ?*

- All cities that contain a number of inhabitants equal or greater than the minimum number of paths required to create a flow (as described above) should be taken into consideration.

### Detecting paths
The analysis could potentially take into account the exact path of flows. This would be useful detect for example which train lines or main roads are used in practice. This is possible only if we suppose that people post tweets while traveling. This assumption doesn't really hold when traveling by car, but could actually be acceptable in the context of trains.


[Here](https://github.com/vasile/transit-map/blob/master/api/geojson/edges.geojson) is some data potentially useful.

**But**, given the potential complexity this task task could bring up, and the weakness of the assumptions, this part can be considered as an improvement of the basic flow detection.

### Across borders
The problem of finding outgoing or incoming flows should be treated in the same way. Consequently, we will need to build nodes for neighboring countries as well.

## Putting it all together
*How to go from the tweets to the described end product?*

Here is a very high level view of the potential pipeline : 

1. Build list of tweets belonging to the same user, emmited in a certain time period (1 day for example).
2. Filter out lists that can not be used for flow detection (lists with unique tweets, lists with tweets posted in the same location).
3. We are left with relevant list of tweets. For every list, associate tweets with corresponding nodes, and try to find a direction. Nodes are computed beforehand based on cities.
4. Filter out paths which are only used by a minority. This leaves us with the most important flows.
5. Visualize those paths on a map.

# Warning
**It seems all of this relies on the fact that a lot of people (at least a good amount) tweet often enough.**