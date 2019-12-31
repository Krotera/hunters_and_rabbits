# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
# Contact: 01101011@tuta.io
import unittest
import sys

sys.path.insert(0, '../hunters_and_rabbits') # Source files
from hr_graph import Vertex, Graph

class BasicGraph(unittest.TestCase):
    def setUp(self):
        self.g = Graph()

        self.v1 = Vertex(1,0)
        self.v2 = Vertex(2,0)
        self.v3 = Vertex(3,0)
        self.v4 = Vertex(4,0)

        self.g.add_vert(self.v1)
        self.g.add_vert(self.v2)
        self.g.add_vert(self.v3)
        self.g.add_vert(self.v4)

        self.g.add_edge(self.v1.id, self.v2.id)
        self.g.add_edge(self.v1.id, self.v3.id)
        self.g.add_edge(self.v2.id, self.v3.id)
        self.g.add_edge(self.v3.id, self.v4.id)

        # Sanity check
        self.assertEqual(self.g.get_vert_count(), 4)
        self.assertEqual(self.g.get_edge_count(), 4)

        self.assertTrue(self.g.has_vert(self.v1.id))
        self.assertTrue(self.g.has_vert(self.v2.id))
        self.assertTrue(self.g.has_vert(self.v3.id))
        self.assertTrue(self.g.has_vert(self.v4.id))

        self.assertTrue(self.g.has_edge(self.v1.id, self.v2.id))
        self.assertTrue(self.g.has_edge(self.v1.id, self.v3.id))
        self.assertTrue(self.g.has_edge(self.v2.id, self.v3.id))
        self.assertTrue(self.g.has_edge(self.v3.id, self.v4.id))
        self.assertFalse(self.g.has_edge(self.v2.id, self.v4.id))

        self.assertEqual(self.g.neighbors(self.v1.id), {self.v2, self.v3})

    def test_0_add_vert_normal(self):
        new_vert = Vertex(5,0)

        self.g.add_vert(new_vert)

        self.assertEqual(self.g.get_vert_count(), 5)
        self.assertTrue(self.g.has_vert(new_vert.id))
        self.assertEqual(self.g.neighbors(new_vert.id), set())

    def test_1_add_vert_already_in(self):
        v1_copy = Vertex(1,0)

        with self.assertRaises(ValueError):
            self.g.add_vert(v1_copy)

        v1_copy = Vertex(1,1) # Same id, different color

        with self.assertRaises(ValueError):
            # Should also err; Vertex equality and hashing is based only on id.
            self.g.add_vert(v1_copy)

        self.assertEqual(self.g.get_vert_count(), 4)

    def test_2_add_edge(self):
        new_vert = Vertex(5,0)

        self.g.add_vert(new_vert)
        self.g.add_edge(self.v4.id, new_vert.id)

        self.assertEqual(self.g.get_vert_count(), 5)
        self.assertEqual(self.g.get_edge_count(), 5)
        self.assertTrue(self.g.has_vert(new_vert.id))
        self.assertTrue(self.g.has_edge(new_vert.id, self.v4.id))
        self.assertEqual(self.g.neighbors(new_vert.id), {self.v4})

        self.g.add_edge(self.v4.id, self.v1.id)

        self.assertEqual(self.g.get_edge_count(), 6)
        self.assertTrue(self.g.has_edge(self.v1.id, self.v4.id))
        self.assertEqual(self.g.neighbors(self.v4.id), {new_vert, self.v1, self.v3})

        # Edge to self
        self.g.add_edge(new_vert.id, new_vert.id)

        self.assertEqual(self.g.get_edge_count(), 7)
        self.assertTrue(self.g.has_edge(new_vert.id, new_vert.id))
        self.assertEqual(self.g.neighbors(new_vert.id), {new_vert, self.v4})

    def test_3_add_edge_already_in(self):
        with self.assertRaises(ValueError):
            self.g.add_edge(self.v3.id, self.v2.id)

        self.assertEqual(self.g.get_edge_count(), 4)

        # Edge to self
        new_vert = Vertex(5,0)

        self.g.add_vert(new_vert)
        self.g.add_edge(new_vert.id, new_vert.id)

        with self.assertRaises(ValueError):
            self.g.add_edge(new_vert.id, new_vert.id)

        self.assertEqual(self.g.get_edge_count(), 5)
        self.assertTrue(self.g.has_edge(new_vert.id, new_vert.id))

    def test_4_add_edge_missing_vert(self):
        new_vert = Vertex(5,0)

        with self.assertRaises(KeyError):
            self.g.add_edge(self.v1.id, new_vert.id)

        self.assertEqual(self.g.get_edge_count(), 4)
        self.assertFalse(self.g.has_edge(self.v1.id, new_vert.id))

    def test_5_add_edge_missing_verts(self):
        new_vert_1 = Vertex(5,0)
        new_vert_2 = Vertex(6,0)

        with self.assertRaises(KeyError):
            self.g.add_edge(new_vert_1.id, new_vert_2.id)

        self.assertEqual(self.g.get_edge_count(), 4)
        self.assertFalse(self.g.has_edge(new_vert_1.id, new_vert_2.id))

    def test_6_del_vert(self):
        self.g.del_vert(self.v1.id)

        self.assertFalse(self.g.has_vert(self.v1.id))
        self.assertTrue(self.g.has_vert(self.v2.id))
        self.assertTrue(self.g.has_vert(self.v3.id))
        self.assertTrue(self.g.has_vert(self.v4.id))
        self.assertFalse(self.g.has_edge(self.v1.id, self.v2.id))
        self.assertFalse(self.g.has_edge(self.v1.id, self.v3.id))
        self.assertTrue(self.g.has_edge(self.v2.id, self.v3.id))
        self.assertTrue(self.g.has_edge(self.v3.id, self.v4.id))
        self.assertEqual(self.g.get_vert_count(), 3)
        self.assertEqual(self.g.get_edge_count(), 2)
        with self.assertRaises(KeyError):
            self.g.neighbors(self.v1.id)
        self.assertEqual(self.g.neighbors(self.v2.id), {self.v3})
        self.assertEqual(self.g.neighbors(self.v3.id), {self.v2, self.v4})
        self.assertEqual(self.g.neighbors(self.v4.id), {self.v3})

        v2_copy = Vertex(2,1) # Same id, different color

        self.g.del_vert(v2_copy.id)

        self.assertFalse(self.g.has_vert(self.v1.id))
        self.assertFalse(self.g.has_vert(self.v2.id))
        self.assertTrue(self.g.has_vert(self.v3.id))
        self.assertTrue(self.g.has_vert(self.v4.id))
        self.assertFalse(self.g.has_edge(self.v1.id, self.v2.id))
        self.assertFalse(self.g.has_edge(self.v1.id, self.v3.id))
        self.assertFalse(self.g.has_edge(self.v2.id, self.v3.id))
        self.assertTrue(self.g.has_edge(self.v3.id, self.v4.id))
        self.assertEqual(self.g.get_vert_count(), 2)
        self.assertEqual(self.g.get_edge_count(), 1)
        with self.assertRaises(KeyError):
            self.g.neighbors(self.v1.id)
        with self.assertRaises(KeyError):
            self.g.neighbors(self.v2.id)
        self.assertEqual(self.g.neighbors(self.v3.id), {self.v4})
        self.assertEqual(self.g.neighbors(self.v4.id), {self.v3})

    def test_7_del_vert_missing(self):
        new_vert = Vertex(5,0)

        with self.assertRaises(KeyError):
            self.g.del_vert(new_vert.id)

        self.assertEqual(self.g.get_vert_count(), 4)
        self.assertEqual(self.g.get_edge_count(), 4)

    def test_8_del_edge(self):
        self.g.del_edge(self.v1.id, self.v2.id)

        self.assertTrue(self.g.has_vert(self.v1.id))
        self.assertTrue(self.g.has_vert(self.v2.id))
        self.assertTrue(self.g.has_vert(self.v3.id))
        self.assertTrue(self.g.has_vert(self.v4.id))
        self.assertFalse(self.g.has_edge(self.v1.id, self.v2.id))
        self.assertTrue(self.g.has_edge(self.v1.id, self.v3.id))
        self.assertTrue(self.g.has_edge(self.v2.id, self.v3.id))
        self.assertTrue(self.g.has_edge(self.v3.id, self.v4.id))
        self.assertEqual(self.g.get_vert_count(), 4)
        self.assertEqual(self.g.get_edge_count(), 3)
        self.assertEqual(self.g.neighbors(self.v1.id), {self.v3})
        self.assertEqual(self.g.neighbors(self.v2.id), {self.v3})
        self.assertEqual(self.g.neighbors(self.v3.id), {self.v4, self.v1, self.v2})
        self.assertEqual(self.g.neighbors(self.v4.id), {self.v3})

        self.g.del_edge(self.v3.id, self.v1.id) # Isolate v1

        self.assertTrue(self.g.has_vert(self.v1.id))
        self.assertTrue(self.g.has_vert(self.v2.id))
        self.assertTrue(self.g.has_vert(self.v3.id))
        self.assertTrue(self.g.has_vert(self.v4.id))
        self.assertFalse(self.g.has_edge(self.v1.id, self.v2.id))
        self.assertFalse(self.g.has_edge(self.v1.id, self.v3.id))
        self.assertTrue(self.g.has_edge(self.v2.id, self.v3.id))
        self.assertTrue(self.g.has_edge(self.v3.id, self.v4.id))
        self.assertEqual(self.g.get_vert_count(), 4)
        self.assertEqual(self.g.get_edge_count(), 2)
        self.assertEqual(self.g.neighbors(self.v1.id), set())
        self.assertEqual(self.g.neighbors(self.v2.id), {self.v3})
        self.assertEqual(self.g.neighbors(self.v3.id), {self.v4, self.v2})
        self.assertEqual(self.g.neighbors(self.v4.id), {self.v3})

    def test_9_del_edge_missing(self):
        with self.assertRaises(ValueError):
            self.g.del_edge(self.v1.id, self.v4.id)

        self.assertEqual(self.g.get_vert_count(), 4)
        self.assertEqual(self.g.get_edge_count(), 4)

    def test_10_del_all_vertices(self):
        self.g.del_vert(self.v1.id)
        self.g.del_vert(self.v2.id)
        self.g.del_vert(self.v3.id)
        self.g.del_vert(self.v4.id)

        self.assertFalse(self.g.has_vert(self.v1.id))
        self.assertFalse(self.g.has_vert(self.v2.id))
        self.assertFalse(self.g.has_vert(self.v3.id))
        self.assertFalse(self.g.has_vert(self.v4.id))
        self.assertFalse(self.g.has_edge(self.v1.id, self.v2.id))
        self.assertFalse(self.g.has_edge(self.v1.id, self.v3.id))
        self.assertFalse(self.g.has_edge(self.v2.id, self.v3.id))
        self.assertFalse(self.g.has_edge(self.v3.id, self.v4.id))
        self.assertEqual(self.g.get_vert_count(), 0)
        self.assertEqual(self.g.get_edge_count(), 0)
        with self.assertRaises(KeyError):
            self.g.neighbors(self.v1.id)
        with self.assertRaises(KeyError):
            self.g.neighbors(self.v2.id)
        with self.assertRaises(KeyError):
            self.g.neighbors(self.v3.id)
        with self.assertRaises(KeyError):
            self.g.neighbors(self.v4.id)

    def test_13_del_all_edges(self):
        self.g.del_edge(self.v1.id, self.v2.id)
        self.g.del_edge(self.v1.id, self.v3.id)
        self.g.del_edge(self.v2.id, self.v3.id)
        self.g.del_edge(self.v3.id, self.v4.id)

        self.assertTrue(self.g.has_vert(self.v1.id))
        self.assertTrue(self.g.has_vert(self.v2.id))
        self.assertTrue(self.g.has_vert(self.v3.id))
        self.assertTrue(self.g.has_vert(self.v4.id))
        self.assertFalse(self.g.has_edge(self.v1.id, self.v2.id))
        self.assertFalse(self.g.has_edge(self.v1.id, self.v3.id))
        self.assertFalse(self.g.has_edge(self.v2.id, self.v3.id))
        self.assertFalse(self.g.has_edge(self.v3.id, self.v4.id))
        self.assertEqual(self.g.get_vert_count(), 4)
        self.assertEqual(self.g.get_edge_count(), 0)
        self.assertEqual(self.g.neighbors(self.v1.id), set())
        self.assertEqual(self.g.neighbors(self.v2.id), set())
        self.assertEqual(self.g.neighbors(self.v3.id), set())
        self.assertEqual(self.g.neighbors(self.v4.id), set())

    def test_16_neighbors(self):
        v5 = Vertex(5,0)
        v6 = Vertex(6,0)

        self.g.add_vert(v5)

        self.assertEqual(self.g.neighbors(v5.id), set())

        self.g.add_vert(v6)
        self.g.add_edge(v5.id, v6.id)

        self.assertEqual(self.g.neighbors(v5.id), {v6})
        self.assertEqual(self.g.neighbors(v6.id), {v5})

if __name__ == "__main__":
    unittest.main()
