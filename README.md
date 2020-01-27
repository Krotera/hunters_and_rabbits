# Hunters and Rabbits
![alt text][example_anim]

[example_anim]: ./example_anim.gif "Example animation"
## What
A [Dash](https://dash.plot.ly/) implementation of Hunters and Rabbits, 

"*a game in which, on each time-step, a collection of k hunters fire at k vertices of a graph. On one of those vertices is an invisible rabbit, which is forced to move along an edge to a new vertex after each round of shots.*"

Alfaro, Blankenship, Cummings, & Humburg. "Hunters and Rabbits on Path- and Cycle-like Graphs." (2019)

## How
Download and extract the ZIP of this repo. In the extracted directory, run: "`pip install .`"

Then, running `python hunters_and_rabbits.py` should open a browser window or tab with the running Dash app. 

There, use the GUI to load a graph file (see `example_graph.xml` for the format), and it'll be displayed as a network graph with clickable vertices. Fire at *k* vertices, press *GO* to recolor the graph, and repeat. 

Happy hunting.

## License
[Mozilla Public License 2.0](https://mozilla.org/MPL/2.0/)
