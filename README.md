# Applied Data Analysis Project
## Mobility patterns in Switzerland with Twitter

This project proposal aims to provide a high-level description of the project we plan to realize, by giving information about the data, feasability, risks, deliverables, timeplan and challenging parts.

This is a very approximative thinking. We didn't investigate in the data or the possible solutions to solve the main problem yet, these are just very basic ideas of what seems to be possible.

### AbstractCan we get insights into high-frequency migration patterns (e.g., the “frontaliers” who commute from France to Geneva every day; Germans who commute to Zurich; etc.)? 

Can we detect changes in migration patterns when, e.g., a new Alpine tunnel gets opened (e.g., according to [this](http://www.nzz.ch/tessin/der-polentagraben-lockt-1.18108822) NZZ article, the Gotthard in particular is expected to be a game changer for the relations between the German and Italian parts of CH)?

### Data Description
The data will mainly consists of Twitter data from 2012. This gather geolocated tweets of the 4 past years accross Switzerland. The amount of data is potentially huge, which is why we plan to consider Big Data solutions.

### Risks & Feasibility
#### Risks
The main risk is to realize that the data doesn't contain any relevant information about what we aim to analyze. This mean that after a deep analysis, we could see that the tweets location doesn't present any relation in order to deduce mobility flows. 

#### Feasibility
However, we can imagine that the feasibility of the project is reasonnable given the amount of available data. Big Data processing is possible with the hardware resources provided by the course staff.


### Deliverables

#### First deliverable
**Deadline** : checkpoint.

**Description** : Mid-project report to analyse and explain the findings of the first half of the project. This would contain some basic visualisation, and conclusions about the feasibility of the total project.

#### Final deliverable
**Deadline** : end of the project.

**Description** : The final deliverable of the project will consist of clear visualisations of mobility flows in Switzerland, supposing they are any from tweets. The form is not defined yet, but the goal is to provide a visualisation as advanced as possible in order to show the mains movements in the country.

### Timeplan

| Date | Task |
|------|------|
| November 6th | Project proposal |
| November 6th - End of November | Getting familiar with data, choosing framworks and tools |
| Beginning of December | First deliverable development |
| Mid December (TBD) | Checkpoint |
| Mid December | Review of timeplan |
| Mid December - January | Final deliverable development |
| End of January (TBD) | Mini-Symposium |

### Challenge : Big Data

This project will be challenging given the amount of data we have to process. Big Data is a new field that we have never experimented before, so the challenge will be to discover, learn, practice and apply Big Data solutions for the project. In particular, we are considering looking at [Spark](http://spark.apache.org), which has been recommanded at the lectures at the very beginning of the semester.