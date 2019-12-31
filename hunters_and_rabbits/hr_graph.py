# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
# Contact: 01101011@tuta.io
class Vertex:
    """Vertex with an id and color field.

    Vertices are equality-checked and hashed by id alone.
    E.g.,
    v0 = Vertex("same_id", "black", foo, ...)
    v1 = Vertex("same_id", "white", bar, ...)
    v_list = [v0]

    >>> v1 in v_list
    True

    >>> v0 == v1
    True
    """
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
        if self.has_vert(vert.id):
            raise ValueError("Graph.add_vert(): Vertex already in graph!")

        self[vert] = set()

    # Avg O(1), worst O(|V|)
    def add_edge(self, id0, id1):
        """Add an edge between two vertices by their id (id0 and id1).

        The vertices must already be in the graph.
        """
        if self.has_edge(id0, id1):
            raise ValueError("Graph.add_edge(): Edge already in graph!")
        if not ((self.has_vert(id0)) and
            (self.has_vert(id1))):
            raise KeyError("Graph.add_edge(): One or both edge endpoints are" +\
                           " not vertices in the graph!")

        v0 = self.get_vert(id0)
        v1 = self.get_vert(id1)

        self[v0].add(v1)
        self[v1].add(v0)
        self.__edge_count += 1

    # Avg O(v°), worst O(|V|^2)
    def del_vert(self, id):
        """Delete a vertex in the graph by its id."""
        if not self.has_vert(id):
            raise KeyError("Graph.del_vert(): Vertex not in graph!")

        vert = self.get_vert(id)
        # Shallow copy adj list to avoid list change during iteration
        neighbors_copy = self[vert].copy()

        for n in neighbors_copy:
            self.del_edge(vert, n)

        del self[vert]

    # Avg O(1), worst O(|E|)
    def del_edge(self, v0, v1):
        """Delete an edge between two vertices, v0 and v1, in the graph.

        v0 and v1 can either be Vertex objects or vertex ids.
        When used with ids, the necessary calls to get_vert() incur an expensive
        linear search.
        """
        # Vertices, as called by del_vert()
        if ((type(v0) == Vertex) and
            (type(v1) == Vertex)):
            if not self.has_edge(v0.id, v1.id):
                raise ValueError("Graph.del_edge(): Edge not in graph!")

            self[v0].remove(v1)
            self[v1].remove(v0)
        # ids
        else:
            if not self.has_edge(v0, v1):
                raise ValueError("Graph.del_edge(): Edge not in graph!")

            vert0 = self.get_vert(v0)
            vert1 = self.get_vert(v1)

            self[vert0].remove(vert1)
            self[vert1].remove(vert0)

        self.__edge_count -= 1

    def get_vert_count(self):
        """Return the number of vertices in the graph."""
        return len(self)

    def get_edge_count(self):
        """Return the number of edges in the graph."""
        return self.__edge_count

    def has_vert(self, id):
        """Return whether a vertex is in the graph by its id."""
        # Graph is a dict, Python dicts are hash tables, and vertices are
        # hashed by id, so we can do fast lookup with a dummy vertex possessing
        # the same id.
        return Vertex(id, "dummy") in self

    def has_edge(self, id0, id1):
        """Return whether two vertices by id (v0 and v1) share an edge."""
        return ((self.has_vert(id0)) and
            (self.has_vert(id1)) and
            (Vertex(id1, "dummy") in self[Vertex(id0, "dummy")]) and
            (Vertex(id0, "dummy") in self[Vertex(id1, "dummy")]))

    # Avg and worst O(|V|)
    def get_vert(self, id):
        """Return a vertex by its id."""
        if not self.has_vert(id):
            raise KeyError("Graph.get_vert(): Vertex not in graph!")

        for k in self.keys():
            if k.id == id:
                return k
        raise RuntimeError("Graph.get_vert(): Fatal disagreement with " +\
                           "has_vert()! This must be a bug.")

    def neighbors(self, id):
        """Return a vertex's neighbors as a set. Vertex specified by its id."""
        if not self.has_vert(id):
            raise KeyError("Graph.neighbors(): Vertex not in graph!")

        return self[Vertex(id, "dummy")]
