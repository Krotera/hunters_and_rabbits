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
    def test_LoadGoodXML_0_normal(self):
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
        parsed_g = load_graph("LoadGoodXML_0_normal.xml")

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

    def test_LoadGoodXML_1_good_colors(self):
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

        parsed_g = load_graph("LoadGoodXML_1_good_color.xml")

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

    def test_LoadGoodXML_2_bad_graph_repeated_vert(self):
        with self.assertRaises(ValueError):
            parsed_g = load_graph("LoadGoodXML_2_bad_graph_repeated_vert.xml")

    def test_LoadGoodXML_3_bad_graph_repeated_edge(self):
        with self.assertRaises(ValueError):
            parsed_g = load_graph("LoadGoodXML_3_bad_graph_repeated_edge.xml")

    def test_LoadGoodXML_4_bad_graph_edge_to_missing_vert(self):
        with self.assertRaises(KeyError):
            parsed_g = load_graph("LoadGoodXML_4_bad_graph_edge_to_missing_vert.xml")

    def test_LoadGoodXML_5_bad_graph_edge_to_missing_vert(self):
        parsed_g = load_graph("LoadGoodXML_5_empty.xml")

        self.assertEqual(parsed_g.get_vert_count(), 0)
        self.assertEqual(parsed_g.get_edge_count(), 0)

class LoadBadXML(unittest.TestCase):
    def test_LoadBadXML_0_missing_vert_id_att(self):
        with self.assertRaises(RuntimeError):
            parsed_g = load_graph("LoadBadXML_0_missing_vert_id_att.xml")

    def test_LoadBadXML_1_missing_edge_id_att(self):
        with self.assertRaises(RuntimeError):
            parsed_g = load_graph("LoadBadXML_1_missing_edge_id_att.xml")

    def test_LoadBadXML_2_bad_vert_id_att(self):
        with self.assertRaises(RuntimeError):
            parsed_g = load_graph("LoadBadXML_2_bad_vert_id_att.xml")

    def test_LoadBadXML_3_bad_edge_id_att(self):
        with self.assertRaises(RuntimeError):
            parsed_g = load_graph("LoadBadXML_3_bad_edge_id_att.xml")

    def test_LoadBadXML_4_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            parsed_g = load_graph("thisfiledoesnotexist")

    def test_LoadBadXML_5_bad_root_elt(self):
        with self.assertRaises(RuntimeError):
            parsed_g = load_graph("LoadBadXML_5_bad_root_elt.xml")

    def test_LoadBadXML_6_invalid_elt(self):
        with self.assertRaises(RuntimeError):
            parsed_g = load_graph("LoadBadXML_6_invalid_elt.xml")

    def test_LoadBadXML_7_bad_vert_elt(self):
        with self.assertRaises(RuntimeError):
            parsed_g = load_graph("LoadBadXML_7_bad_vert_elt.xml")

    def test_LoadBadXML_8_bad_vert_elt(self):
        with self.assertRaises(RuntimeError):
            parsed_g = load_graph("LoadBadXML_8_bad_edge_elt.xml")

    def test_LoadBadXML_9_bad_color(self):
        with self.assertRaises(RuntimeError):
            parsed_g = load_graph("LoadBadXML_9_bad_color.xml")

class SaveGraph(unittest.TestCase):
    def test_SaveGraph_0_normal_graph(self):
        saved_g = Graph()

        v1 = Vertex("1", "black")
        v2 = Vertex("2", "white")
        v3 = Vertex("3", "black")
        v4 = Vertex("4", "white")
        v5 = Vertex("5", "black")

        saved_g.add_vert(v1)
        saved_g.add_vert(v2)
        saved_g.add_vert(v3)
        saved_g.add_vert(v4)
        saved_g.add_vert(v5)

        saved_g.add_edge(v1.id, v2.id)
        saved_g.add_edge(v1.id, v3.id)
        saved_g.add_edge(v2.id, v3.id)
        saved_g.add_edge(v3.id, v4.id)

        saved_xml_str = save_graph(saved_g, "SaveGraph_0_saved_normal_graph.xml")
        # Note: testing the string against a model is tedious because the order
        # of edges varies.

        # Test loaded graph
        loaded_g = load_graph("SaveGraph_0_saved_normal_graph.xml")

        self.assertEqual(loaded_g.get_vert_count(), 5)
        self.assertEqual(loaded_g.get_edge_count(), 4)

        self.assertTrue(loaded_g.has_vert(v1.id))
        self.assertTrue(loaded_g.has_vert(v2.id))
        self.assertTrue(loaded_g.has_vert(v3.id))
        self.assertTrue(loaded_g.has_vert(v4.id))
        self.assertTrue(loaded_g.has_vert(v5.id))

        self.assertTrue(loaded_g.has_edge(v1.id, v2.id))
        self.assertTrue(loaded_g.has_edge(v1.id, v3.id))
        self.assertTrue(loaded_g.has_edge(v2.id, v3.id))
        self.assertTrue(loaded_g.has_edge(v3.id, v4.id))
        self.assertFalse(loaded_g.has_edge(v2.id, v4.id))

        self.assertEqual(loaded_g.get_vert(v1.id).color, "black")
        self.assertEqual(loaded_g.get_vert(v2.id).color, "white")
        self.assertEqual(loaded_g.get_vert(v3.id).color, "black")
        self.assertEqual(loaded_g.get_vert(v4.id).color, "white")
        self.assertEqual(loaded_g.get_vert(v5.id).color, "black")

        self.assertEqual(loaded_g.neighbors(v1.id), {v2, v3})
        self.assertEqual(loaded_g.neighbors(v2.id), {v3, v1})
        self.assertEqual(loaded_g.neighbors(v3.id), {v1, v2, v4})
        self.assertEqual(loaded_g.neighbors(v4.id), {v3})
        self.assertEqual(loaded_g.neighbors(v5.id), set())

    def test_SaveGraph_1_empty_graph(self):
        saved_g = Graph()

        saved_xml_str = save_graph(saved_g, "SaveGraph_1_empty_graph.xml")
        empty_graph_xml_str = '<?xml version="1.0" ?>\n<graph/>\n'

        self.assertEqual(saved_xml_str, empty_graph_xml_str)

        loaded_g = load_graph("SaveGraph_1_empty_graph.xml")

        self.assertEqual(loaded_g.get_vert_count(), 0)
        self.assertEqual(loaded_g.get_edge_count(), 0)

        # Add some stuff to the graph
        v1 = Vertex("1", "black")
        v2 = Vertex("2", "white")

        loaded_g.add_vert(v1)
        loaded_g.add_vert(v2)
        loaded_g.add_edge("1", "2")

        saved_xml_str = save_graph(loaded_g, "SaveGraph_1_empty_graph.xml")

        reloaded_g = load_graph("SaveGraph_1_empty_graph.xml")

        self.assertEqual(reloaded_g.get_vert_count(), 2)
        self.assertEqual(reloaded_g.get_edge_count(), 1)
        self.assertTrue(reloaded_g.has_vert("1"))
        self.assertTrue(reloaded_g.has_vert("2"))
        self.assertTrue(reloaded_g.has_edge("2", "1"))
        self.assertEqual(reloaded_g.get_vert("1").color, "black")
        self.assertEqual(reloaded_g.get_vert("2").color, "white")

        # Remove the stuff
        reloaded_g.del_vert("1")
        reloaded_g.del_vert("2")

        saved_xml_str = save_graph(reloaded_g, "SaveGraph_1_empty_graph.xml")

        self.assertEqual(saved_xml_str, empty_graph_xml_str)

if __name__ == "__main__":
    unittest.main()
