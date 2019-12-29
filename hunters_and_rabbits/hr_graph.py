# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
# Contact: 01101011@tuta.io
class Vertex:
    """Vertex with an id and color field. Equality-checked and hashed by id."""
    def __init__(self, id, color):
        self.id = id
        self.color = color

    def __eq__(self, other):
        if type(other) is type(self):
            return self.id == other.id
        else:
            return False

    def __hash__(self):
        return hash(self.id)

class Graph(dict):
    """Undirected adjacency list graph (dict of vertex keys, adj set values)

    vertex: {neighbor(s)}
    a: {b, c}
    b: {a}
    c: {a}

    Usage:
    g = Graph(['a', 'b'], [('a', 'b')])
    g.add_vert('c')
    g.add_edge(('a', 'c'))
    a_neighbors = g['a']

    Adjacency list graphs are best for SPARSE graphs (low edge:vertex ratio)
    since they use O(|V|+2|E|) memory, where |V| and |E| are the number of verts
    and edges in the graph, resp.
    For DENSE graphs (high edge:vertex ratio), an adjacency MATRIX graph's
    O(|V|^2) memory footprint is more efficient.

    Sets (and dicts) are actually hash tables in Python, so to search, add, or
    delete a vertex's edge is average O(1) and worst O(|E|) where |E| is number
    of edges in the graph (which is the most edges a vertex can have).
    Similarly, search and add operations on vertices in the graph are average
    O(1) and worst O(|V|), but deleting a vertex, v, is average O(v°) where
    v°, the degree of v, is the number of edges v has and worst O(|V|^2).
    This is because deleting the vertex is worst |V|, then deleting an edge is
    worst |E| for up to |E| edges, so we're left with |V|+|E|^2. Because we
    use sets and can't have redundant edges, and because a vertex has at most
    |V|+1 edges, |V|+|E|^2 becomes |V|+(|V|+1)^2 ≈ |V|^2.
    """
    __edge_count = 0

    def __init__(self, verts=[], edges=[]):
        # Add initialization verts and edges
        for v in verts:
            self.add_vert(v)

        for e in edges:
            self.add_edge(e)

    # Avg O(1), worst O(|E|)
    def add_vert(self, vert):
        """Add a vertex to the graph."""
        if self.has_vert(vert):
            raise ValueError("Graph.add_vert(): Vertex already in graph!")

        self[vert] = set()

    # Avg O(1), worst O(|V|)
    def add_edge(self, v0, v1):
        """Add an edge between two vertices, v0 and v1, in the graph.

        The vertices must already be in the graph.
        """
        if self.has_edge(v0, v1):
            raise ValueError("Graph.add_edge(): Edge already in graph!")
        if not ((self.has_vert(v0)) and
            (self.has_vert(v1))):
            raise KeyError("Graph.add_edge(): One or both edge endpoints are" +\
                           " not vertices in the graph!")

        self[v0].add(v1)
        self[v1].add(v0)
        self.__edge_count += 1

    # Avg O(v°), worst O(|V|^2)
    def del_vert(self, vert):
        """Delete a vertex in the graph."""
        if not self.has_vert(vert):
            raise KeyError("Graph.del_vert(): Vertex not in graph!")

        # Shallow copy adj list to avoid list change during iteration
        neighbors_tmp = self[vert].copy()

        for n in neighbors_tmp:
            self.del_edge(vert, n)

        del self[vert]

    # Avg O(1), worst O(|E|)
    def del_edge(self, v0, v1):
        """Delete an edge between two vertices, v0 and v1, in the graph."""
        if not self.has_edge(v0, v1):
            raise ValueError("Graph.del_edge(): Edge not in graph!")

        self[v0].remove(v1)
        self[v1].remove(v0)
        self.__edge_count -= 1

    def get_vert_count(self):
        """Return the number of vertices in the graph."""
        return len(self)

    def get_edge_count(self):
        """Return the number of edges in the graph."""
        return self.__edge_count

    def has_vert(self, vert):
        """Return whether a vertex is in the graph."""
        return vert in self

    def has_edge(self, v0, v1):
        """Return whether two vertices, v0 and v1, share an edge."""
        return ((self.has_vert(v0)) and
            (self.has_vert(v1)) and
            (v1 in self[v0]) and
            (v0 in self[v1]))

    def neighbors(self, vert):
        """Return a vertex's neighbors as a set."""
        if not self.has_vert(vert):
            raise KeyError("Graph.neighbors(): Vertex not in graph!")

        return self[vert]
