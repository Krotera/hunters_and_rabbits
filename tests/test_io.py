# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
# Contact: 01101011@tuta.io
import unittest
import sys

sys.path.insert(0, '../hunters_and_rabbits') # Source files
from hr_graph import Vertex, Graph
from hr_io import load_graph, save_graph

class LoadGoodXML(unittest.TestCase):
    def test_0_normal(self):
        correct_g = Graph()

        v1 = Vertex("1", 0)
        v2 = Vertex("2", 0)
        v3 = Vertex("3", 0)
        v4 = Vertex("4", 0)
        v5 = Vertex("5", 0)

        correct_g.add_vert(v1)
        correct_g.add_vert(v2)
        correct_g.add_vert(v3)
        correct_g.add_vert(v4)
        correct_g.add_vert(v5)

        correct_g.add_edge(v1.id, v2.id)
        correct_g.add_edge(v1.id, v3.id)
        correct_g.add_edge(v2.id, v3.id)
        correct_g.add_edge(v3.id, v4.id)

        # Sanity check
        self.assertEqual(correct_g.get_vert_count(), 5)
        self.assertEqual(correct_g.get_edge_count(), 4)

        self.assertTrue(correct_g.has_vert(v1.id))
        self.assertTrue(correct_g.has_vert(v2.id))
        self.assertTrue(correct_g.has_vert(v3.id))
        self.assertTrue(correct_g.has_vert(v4.id))
        self.assertTrue(correct_g.has_vert(v5.id))

        self.assertTrue(correct_g.has_edge(v1.id, v2.id))
        self.assertTrue(correct_g.has_edge(v1.id, v3.id))
        self.assertTrue(correct_g.has_edge(v2.id, v3.id))
        self.assertTrue(correct_g.has_edge(v3.id, v4.id))
        self.assertFalse(correct_g.has_edge(v2.id, v4.id))

        self.assertEqual(correct_g.get_vert(v1.id).color, 0)
        self.assertEqual(correct_g.get_vert(v2.id).color, 0)
        self.assertEqual(correct_g.get_vert(v3.id).color, 0)
        self.assertEqual(correct_g.get_vert(v4.id).color, 0)
        self.assertEqual(correct_g.get_vert(v5.id).color, 0)

        self.assertEqual(correct_g.neighbors(v1.id), {v2, v3})
        self.assertEqual(correct_g.neighbors(v2.id), {v3, v1})
        self.assertEqual(correct_g.neighbors(v3.id), {v1, v2, v4})
        self.assertEqual(correct_g.neighbors(v4.id), {v3})
        self.assertEqual(correct_g.neighbors(v5.id), set())

        # Parse XML file
        parsed_g = load_graph("./0_normal.xml")

        # g1 == g2 if they have same edges and same vertices by id
        # (even if vertices differ otherwise)
        self.assertTrue(parsed_g == correct_g)

        self.assertEqual(parsed_g.get_vert(v1.id).color, "black")
        self.assertEqual(parsed_g.get_vert(v2.id).color, "black")
        self.assertEqual(parsed_g.get_vert(v3.id).color, "black")
        self.assertEqual(parsed_g.get_vert(v4.id).color, "black")
        self.assertEqual(parsed_g.get_vert(v5.id).color, "black")

        # Modify edge or vert inventory to break equality
        correct_g.del_edge("1", "2")
        self.assertTrue(parsed_g != correct_g)

    def test_1_good_colors(self):
        correct_g = Graph()

        v1 = Vertex("1", "white")
        v2 = Vertex("2", "black")
        v3 = Vertex("3", "white")
        v4 = Vertex("4", "white")
        v5 = Vertex("5", "white")
        v6 = Vertex("6", "white")
        v7 = Vertex("7", "white")
        v8 = Vertex("8", "black")
        v9 = Vertex("9", "black")

        correct_g.add_vert(v1)
        correct_g.add_vert(v2)
        correct_g.add_vert(v3)
        correct_g.add_vert(v4)
        correct_g.add_vert(v5)
        correct_g.add_vert(v6)
        correct_g.add_vert(v7)
        correct_g.add_vert(v8)
        correct_g.add_vert(v9)

        correct_g.add_edge(v1.id, v2.id)
        correct_g.add_edge(v1.id, v3.id)
        correct_g.add_edge(v2.id, v3.id)
        correct_g.add_edge(v3.id, v4.id)

        parsed_g = load_graph("./1_good_color.xml")

        self.assertTrue(parsed_g == correct_g)

        self.assertEqual(parsed_g.get_vert(v1.id).color, "white")
        self.assertEqual(parsed_g.get_vert(v2.id).color, "black")
        self.assertEqual(parsed_g.get_vert(v3.id).color, "white")
        self.assertEqual(parsed_g.get_vert(v4.id).color, "white")
        self.assertEqual(parsed_g.get_vert(v5.id).color, "white")
        self.assertEqual(parsed_g.get_vert(v6.id).color, "white")
        self.assertEqual(parsed_g.get_vert(v7.id).color, "white")
        self.assertEqual(parsed_g.get_vert(v8.id).color, "black")
        self.assertEqual(parsed_g.get_vert(v9.id).color, "black")

    def test_2_bad_graph_repeated_vert(self):
        with self.assertRaises(ValueError):
            parsed_g = load_graph("./2_bad_graph_repeated_vert.xml")

    def test_3_bad_graph_repeated_edge(self):
        with self.assertRaises(ValueError):
            parsed_g = load_graph("./3_bad_graph_repeated_edge.xml")

    def test_4_bad_graph_edge_to_missing_vert(self):
        with self.assertRaises(KeyError):
            parsed_g = load_graph("./4_bad_graph_edge_to_missing_vert.xml")

class LoadBadXML(unittest.TestCase):
    def test_5_missing_vert_id_att(self):
        with self.assertRaises(RuntimeError):
            parsed_g = load_graph("./5_missing_vert_id_att.xml")

    def test_6_missing_edge_id_att(self):
        with self.assertRaises(RuntimeError):
            parsed_g = load_graph("./6_missing_edge_id_att.xml")

    def test_7_bad_vert_id_att(self):
        with self.assertRaises(RuntimeError):
            parsed_g = load_graph("./7_bad_vert_id_att.xml")

    def test_8_bad_edge_id_att(self):
        with self.assertRaises(RuntimeError):
            parsed_g = load_graph("./8_bad_edge_id_att.xml")

    def test_9_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            parsed_g = load_graph("./thisfiledoesnotexist")

    def test_10_bad_root_elt(self):
        with self.assertRaises(RuntimeError):
            parsed_g = load_graph("./10_bad_root_elt.xml")

    def test_11_invalid_elt(self):
        with self.assertRaises(RuntimeError):
            parsed_g = load_graph("./11_invalid_elt.xml")

    def test_12_bad_vert_elt(self):
        with self.assertRaises(RuntimeError):
            parsed_g = load_graph("./12_bad_vert_elt.xml")

    def test_13_bad_vert_elt(self):
        with self.assertRaises(RuntimeError):
            parsed_g = load_graph("./13_bad_edge_elt.xml")

    def test_14_bad_color(self):
        with self.assertRaises(RuntimeError):
            parsed_g = load_graph("./14_bad_color.xml")

if __name__ == "__main__":
    unittest.main()
