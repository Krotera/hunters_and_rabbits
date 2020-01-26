# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
# Contact: 01101011@tuta.io

from hr_graph import Vertex, Graph

def recolor(g):
    """Recolors the given graph's vertices based on certain rules.

    1: If a vertex has at least one adjacent black neighbor, recolor it
    black.
    2: Otherwise, recolor it white.
    """
    to_recolor_black = []
    to_recolor_white = []

    for vert, neighbors in g.items():
        for n in neighbors:
            if n.color == "black":
                to_recolor_black.append(vert)

        if vert not in to_recolor_black:
            to_recolor_white.append(vert)

    for vert in to_recolor_black:
        vert.color = "black"

    for vert in to_recolor_white:
        vert.color = "white"
