# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
# Contact: 01101011@tuta.io
import xml.etree.ElementTree as ET

from hr_graph import Vertex, Graph

def load_graph(path):
    """Read an XML file at 'path' and return the graph it describes."""
    g = Graph()
    vertices = []
    edges = []
    tree = ET.parse(path)
    root = tree.getroot()

    if not root.tag.lower() == "graph":
        raise RuntimeError("load_graph(" + path + "): Root tag of a graph " +\
                            "file must be \"graph\"; instead, found: \"" +\
                            root.tag + "\"")

    # Collect vertices and edges
    for child in root:
        # Lowercase the keys of the child.attrib dict to tolerate
        # mixed case XML attributes
        child.attrib = dict((k.lower(), v) for k,v in child.attrib.items())

        if ((child.tag.lower() == "vertex") or
            (child.tag.lower() == "v")):
            # Vertex element
            if not "id" in child.attrib:
                raise RuntimeError("load_graph(" + path + "): Vertex " +\
                                    "element missing \"id\" attribute!")

            new_vert = Vertex(child.attrib["id"], "black")

            if "color" in child.attrib:
                if ((child.attrib["color"].strip().lower() == "white") or
                    (child.attrib["color"].strip().lower() == "w")):
                    new_vert.color = "white"
                elif not ((child.attrib["color"].strip().lower() == "black") or
                    (child.attrib["color"].strip().lower() == "b")):
                    raise RuntimeError("load_graph(" + path + "): " +\
                    "Unrecognized vertex color attribute: \"" +\
                    child.attrib["color"] + "\"")

            vertices.append(new_vert)
        elif ((child.tag.lower() == "edge") or
            (child.tag.lower() == "e")):
            # Edge element
            if not (("id1" in child.attrib) and
                ("id2" in child.attrib)):
                raise RuntimeError("load_graph(" + path + "): Edge element " +\
                "missing \"id1\" and/or \"id2\" attributes!")

            edges.append((child.attrib["id1"], child.attrib["id2"]))
        else:
            # Unrecognized element
            raise RuntimeError("load_graph(" + path + "): Unrecognized " +\
                                "graph element: \"" + child.tag + "\"")

    # Add collected vertices...
    for v in vertices:
        g.add_vert(v)

    # ...then collected edges
    for e in edges:
        g.add_edge(e[0], e[1])

    return g

def save_graph(g, path):
    """Save the graph 'g' to an XML file at 'path'."""
    raise NotImplementedError()
