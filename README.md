# Hunters and Rabbits
![alt text][example_anim]

[example_anim]: ./example_anim.gif "Example animation"
## What
A [Dash](https://dash.plot.ly/) implementation of Hunters and Rabbits, 

"*a game in which, on each time-step, a collection of k hunters fire at k vertices of a graph. On one of those vertices is an invisible rabbit, which is forced to move along an edge to a new vertex after each round of shots.*"

Alfaro, Blankenship, Cummings, & Humburg. "Hunters and Rabbits on Path- and Cycle-like Graphs." (2019)

## How
**Windows:** To use without installing Python, pip, or anything else, download and extract the `hr_windows` ZIP from the [releases](https://github.com/Krotera/hunters_and_rabbits/releases) of this repo and double-click the `hunters_and_rabbits.exe`. 

**Linux:** Similarly, pick the `hr_linux` ZIP and launch the `hunters_and_rabbits` executable.

To use the traditional way, first install Python and pip. Then, download and extract the ZIP of this repo. In the extracted directory, run 

`pip install .`

and then 

`python .../hunters_and_rabbits.py`

A browser window or tab should open (with some delay) with the running Dash app on a local port.

There, load a graph by entering the path to a graph file like `example_graph.xml`. (On Windows, `Shift + Right-click > Copy as path` is handy for copying file paths.) The graph will be displayed as a network graph with clickable vertices. Fire at *k* vertices, press *GO* to recolor the graph, and repeat. 

Happy hunting.

## License
[Mozilla Public License 2.0](https://mozilla.org/MPL/2.0/)
