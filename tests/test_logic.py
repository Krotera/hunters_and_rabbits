# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
# Contact: 01101011@tuta.io
import unittest
import sys

sys.path.insert(0, '../hunters_and_rabbits') # Source files
from hr_graph import Vertex, Graph
from hr_logic import recolor

def print_graph_colors(g):
    for vert, _ in g.items():
        print(f"{vert.id}: {vert.color}")

class RecolorGraph(unittest.TestCase):
    def test_RecolorGraph_0_normal(self):
        g = Graph()

        g.add_vert(Vertex("1", "white"))
        g.add_vert(Vertex("2", "white"))
        g.add_vert(Vertex("3", "black"))
        g.add_vert(Vertex("4", "white"))
        g.add_vert(Vertex("5", "white"))

        g.add_edge("1", "2")
        g.add_edge("1", "3")
        g.add_edge("3", "2")
        g.add_edge("4", "3")
        g.add_edge("5", "4")
        g.add_edge("5", "5")

        self.assertTrue(g.get_vert("1").color == "white")
        self.assertTrue(g.get_vert("2").color == "white")
        self.assertTrue(g.get_vert("3").color == "black")
        self.assertTrue(g.get_vert("4").color == "white")
        self.assertTrue(g.get_vert("5").color == "white")

        # print("Before recoloring:")
        # print_graph_colors(g)

        # After 4 recolorings, the entire graph should be black.

        recolor(g) # 1

        # print("Recolor 1:")
        # print_graph_colors(g)

        self.assertTrue(g.get_vert("1").color == "black")
        self.assertTrue(g.get_vert("2").color == "black")
        self.assertTrue(g.get_vert("3").color == "white")
        self.assertTrue(g.get_vert("4").color == "black")
        self.assertTrue(g.get_vert("5").color == "white")

        recolor(g) # 2

        # print("Recolor 2:")
        # print_graph_colors(g)

        self.assertTrue(g.get_vert("1").color == "black")
        self.assertTrue(g.get_vert("2").color == "black")
        self.assertTrue(g.get_vert("3").color == "black")
        self.assertTrue(g.get_vert("4").color == "white")
        self.assertTrue(g.get_vert("5").color == "black") # Neighbor of self!

        recolor(g) # 3

        # print("Recolor 3:")
        # print_graph_colors(g)

        self.assertTrue(g.get_vert("1").color == "black")
        self.assertTrue(g.get_vert("2").color == "black")
        self.assertTrue(g.get_vert("3").color == "black")
        self.assertTrue(g.get_vert("4").color == "black")
        self.assertTrue(g.get_vert("5").color == "black") # So still black.

        recolor(g) # 4

        # print("Recolor 4:")
        # print_graph_colors(g)

        self.assertTrue(g.get_vert("1").color == "black")
        self.assertTrue(g.get_vert("2").color == "black")
        self.assertTrue(g.get_vert("3").color == "black")
        self.assertTrue(g.get_vert("4").color == "black")
        self.assertTrue(g.get_vert("5").color == "black")

    def test_RecolorGraph_1_empty(self):
        g = Graph()

        self.assertEqual(g.get_vert_count(), 0)
        self.assertEqual(g.get_edge_count(), 0)

        recolor(g)

        self.assertEqual(g.get_vert_count(), 0)
        self.assertEqual(g.get_edge_count(), 0)

    def test_RecolorGraph_2_all_black(self):
        g = Graph()

        g.add_vert(Vertex("1", "black"))
        g.add_vert(Vertex("2", "black"))
        g.add_vert(Vertex("3", "black"))
        g.add_vert(Vertex("4", "black"))
        g.add_vert(Vertex("5", "black"))
        g.add_vert(Vertex("6", "black"))
        g.add_vert(Vertex("7", "black"))

        g.add_edge("1", "2")
        g.add_edge("1", "3")
        g.add_edge("2", "3")
        g.add_edge("4", "3")
        g.add_edge("4", "5")
        g.add_edge("5", "6")
        g.add_edge("6", "7")

        self.assertTrue(g.get_vert("1").color == "black")
        self.assertTrue(g.get_vert("2").color == "black")
        self.assertTrue(g.get_vert("3").color == "black")
        self.assertTrue(g.get_vert("4").color == "black")
        self.assertTrue(g.get_vert("5").color == "black")
        self.assertTrue(g.get_vert("6").color == "black")
        self.assertTrue(g.get_vert("7").color == "black")

        recolor(g)

        self.assertTrue(g.get_vert("1").color == "black")
        self.assertTrue(g.get_vert("2").color == "black")
        self.assertTrue(g.get_vert("3").color == "black")
        self.assertTrue(g.get_vert("4").color == "black")
        self.assertTrue(g.get_vert("5").color == "black")
        self.assertTrue(g.get_vert("6").color == "black")
        self.assertTrue(g.get_vert("7").color == "black")

    def test_RecolorGraph_3_all_white(self):
        g = Graph()

        g.add_vert(Vertex("1", "white"))
        g.add_vert(Vertex("2", "white"))
        g.add_vert(Vertex("3", "white"))
        g.add_vert(Vertex("4", "white"))
        g.add_vert(Vertex("5", "white"))
        g.add_vert(Vertex("6", "white"))
        g.add_vert(Vertex("7", "white"))

        g.add_edge("1", "2")
        g.add_edge("1", "3")
        g.add_edge("2", "3")
        g.add_edge("4", "3")
        g.add_edge("4", "5")
        g.add_edge("5", "6")
        g.add_edge("6", "7")

        self.assertTrue(g.get_vert("1").color == "white")
        self.assertTrue(g.get_vert("2").color == "white")
        self.assertTrue(g.get_vert("3").color == "white")
        self.assertTrue(g.get_vert("4").color == "white")
        self.assertTrue(g.get_vert("5").color == "white")
        self.assertTrue(g.get_vert("6").color == "white")
        self.assertTrue(g.get_vert("7").color == "white")

        recolor(g)

        self.assertTrue(g.get_vert("1").color == "white")
        self.assertTrue(g.get_vert("2").color == "white")
        self.assertTrue(g.get_vert("3").color == "white")
        self.assertTrue(g.get_vert("4").color == "white")
        self.assertTrue(g.get_vert("5").color == "white")
        self.assertTrue(g.get_vert("6").color == "white")
        self.assertTrue(g.get_vert("7").color == "white")

    def test_RecolorGraph_4_black_star(self):
        g = Graph()

        g.add_vert(Vertex("center", "white"))
        # Spokes:
        g.add_vert(Vertex("1", "black"))
        g.add_vert(Vertex("2", "black"))
        g.add_vert(Vertex("3", "black"))
        g.add_vert(Vertex("4", "black"))
        g.add_vert(Vertex("5", "black"))
        g.add_vert(Vertex("6", "black"))
        g.add_vert(Vertex("7", "black"))
        g.add_vert(Vertex("8", "black"))

        g.add_edge("center", "1")
        g.add_edge("center", "2")
        g.add_edge("center", "3")
        g.add_edge("center", "4")
        g.add_edge("center", "5")
        g.add_edge("center", "6")
        g.add_edge("center", "7")
        g.add_edge("center", "8")

        # The center and the spokes will alternate colors on each recoloring.
        for i in range(100):
            central_color = None
            spoke_color = None

            recolor(g)

            if i % 2 == 0:
                central_color = "black"
                spoke_color = "white"
            else:
                central_color = "white"
                spoke_color = "black"

            self.assertTrue(g.get_vert("center").color == central_color)
            self.assertTrue(g.get_vert("1").color == spoke_color)
            self.assertTrue(g.get_vert("2").color == spoke_color)
            self.assertTrue(g.get_vert("3").color == spoke_color)
            self.assertTrue(g.get_vert("4").color == spoke_color)
            self.assertTrue(g.get_vert("5").color == spoke_color)
            self.assertTrue(g.get_vert("6").color == spoke_color)
            self.assertTrue(g.get_vert("7").color == spoke_color)
            self.assertTrue(g.get_vert("8").color == spoke_color)

if __name__ == "__main__":
    unittest.main()
