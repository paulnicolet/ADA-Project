# Applied Data Analysis Project
## Mobility patterns in Switzerland with Twitter

### Goal
The goal is to look for geographical people flows in Switzerland, from  a set of geolocalized tweets.

### Dependencies
* `pandas`
* `haversine`
* `pickle`

### References
* [GeoNames](http://www.geonames.org) for the Swiss geographical data.

## Project proposal

This project proposal aims to provide a high-level description of the project, by giving information about the data, feasability, risks, deliverables, timeplan and challenging parts.

The approach taken is conceptual. The data or the possible solutions were not yet investigated, these are just very basic ideas of what seems to be possible.

### Abstract
Can we get insights into high-frequency migration patterns (e.g., the “frontaliers” who commute from France to Geneva every day; Germans who commute to Zurich; etc.)? 

Can we detect changes in migration patterns when, e.g., a new Alpine tunnel gets opened (e.g., according to [this](http://www.nzz.ch/tessin/der-polentagraben-lockt-1.18108822) NZZ article, the Gotthard in particular is expected to be a game changer for the relations between the German and Italian parts of CH)?

### Data Description
The data will mainly consists in Twitter data from the year 2012. This dataset represents a gathering of geolocated tweets of the past 4 years accross Switzerland. The amount of data is potentially huge, which is why we plan on considering Big Data solutions.

### Risks & Feasibility
#### Risks
The main risk is to realize that the data doesn't contain enough relevant information for our purpose. Indeed, the analysis of the tweet locations could lead us to the conclusion that no substantial relation can be shown through this particular data, thus making it impossible for us to deduce any relevant mobility flows.

#### Feasibility
However, we can imagine that the feasibility of the project is reasonnable given the amount of available data. 
Besides, Big Data processing is possible with the hardware resources provided by the course staff.


### Deliverables

#### First deliverable
*Deadline* : checkpoint.

*Description* : Mid-project report to analyse and explain the findings of the first half of the project. This would contain some basic visualisation, and conclusions on the feasibility of the overall project.

#### Final deliverable
*Deadline* : end of the project.

*Description* : The final deliverable of the project will consists in clear visualisations of mobility flows in Switzerland (assuming the data was sufficiently relevant for our purpose). The form is not defined yet, but the goal is to provide a visualisation as advanced as possible in order to show the mains movements in the country.

### Timeplan

| Date | Task |
|------|------|
| November 6th | Project proposal |
| November 6th - End of November | Getting familiar with data, choosing frameworks and tools |
| Beginning of December | First deliverable development |
| Mid December (TBD) | Checkpoint |
| Mid December | Review of timeplan |
| Mid December - January | Final deliverable development |
| End of January (TBD) | Mini-Symposium |

### Reviewed Timeplan

| Date | Task |
|------|------|
| November 6th | Project proposal |
| November 6th - End of November | Getting familiar with data, choosing frameworks and tools |
| December | Design and basic flow detection code|
| End of December| Checkpoint |
| January - Mid January | Final flow detection algorithms |
| Mid January - End of January | Final deliverable development |
| End of January (TBD) | Mini-Symposium |

### Challenge : Big Data

- This project will be challenging given the amount of data we have to process. Big Data is a new field that we have never experimented before, so the challenge will be to discover, learn, practice and apply Big Data solutions for the project. In particular, we are considering looking at [Spark](http://spark.apache.org), which has been recommended at the lectures at the very beginning of the semester.
- Making sense of this data is another challenge. Extracting relevant migration patterns,
as well as quantifying the influence of new infrastructure represent a conceptual model which needs to
be reflected.
