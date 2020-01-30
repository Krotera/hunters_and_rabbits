# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
# Contact: 01101011@tuta.io
import random
import webbrowser
from time import sleep

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import networkx as nx
from flask import request

import hr_graph
import hr_io
import hr_logic

# Dash app
app = dash.Dash(__name__)
# Variables to be used by app as globals.
loaded_hr_graph = hr_graph.Graph()
clicked_verts_this_turn = dict()
node_positions = None
# (Ideally, we'd have to/from JSON functions and store globals in hidden
# divs.
# Dash discourages using globals but only in the sense that it breaks
# multi-user sessions.
# This, though, is intended for a single user at a time, so it's probably not
# a problem. Probably.)

def figure_from_hr_graph(hr_graph):
    """Return a plotly.graph_objects.Figure of the given hr_graph.Graph."""
    global node_positions

    graph_fig = go.Figure(
        data = [],
        layout = go.Layout(
            title = "Hunters and Rabbits",
            titlefont = dict(size=16),
            showlegend = False,
            hovermode = "closest",
            margin = dict(b = 20, l = 5, r = 5, t = 40),
            annotations=[
                dict(
                    text = "Enter a file path and press \"Load\" to open a graph.",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005,
                    y=-0.002
                )
            ],
            xaxis = dict(
                showgrid = False,
                zeroline = False, showticklabels = False
            ),
            yaxis = dict(
                showgrid = False,
                zeroline = False, showticklabels = False
            )
        )
    )

    if hr_graph is not None:
        # Remove "Press LOAD" prompt
        graph_fig.layout.annotations[0].pop("text")

        # Turn hr_graph.Graph to an nx.Graph
        nx_graph = nx.Graph()

        for node in hr_graph:
            for neighbor in hr_graph.neighbors(node.id):
                # nx.Graph adds nodes while adding edges
                nx_graph.add_edge(node, neighbor)

        # Assign node positions (but don't re-assign them)
        if node_positions is None:
            node_positions = nx.layout.spring_layout(nx_graph)

        # Construct node trace
        node_trace = go.Scatter(
            x = [],
            y = [],
            text = [],
            mode = "markers",
            hoverinfo = "text",
            marker = dict(
                showscale = False,
                #colorscale = "Greys",
                reversescale = True,
                color = [],
                size = 10,
                line = dict(width = 2))
        )
        for node in nx_graph.nodes():
            # Store node coords in trace
            x, y = node_positions[node]
            node_trace["x"] += tuple([x])
            node_trace["y"] += tuple([y])

            # and node color
            if node.color == "black":
                node_trace["marker"]["color"] += tuple(["black"])
            elif node.color == "white":
                node_trace["marker"]["color"] += tuple(["white"])

            # and ID
            node_trace["text"]+=tuple([node.id])

        # Construct edge trace
        edge_trace = go.Scatter(
            x = [],
            y = [],
            line=dict(width=0.5,color="#888"),
            hoverinfo="none",
            mode="lines"
        )
        for edge in nx_graph.edges():
            x_0, y_0 = node_positions[edge[0]]
            x_1, y_1 = node_positions[edge[1]]
            edge_trace["x"] += tuple([x_0, x_1, None])
            edge_trace["y"] += tuple([y_0, y_1, None])

        # Add traces to figure
        graph_fig.add_traces((node_trace, edge_trace))

    return graph_fig

# Graph canvas + surrounding HTML elements, all here in app.layout!
app.layout = html.Div([
    html.Div(
        [
            # Graph canvas
            dcc.Graph(
                id = "displayed-graph",
                figure = figure_from_hr_graph(None) # Graph to display
            ),

            # Counter of k vertices manipulated by user this turn
            html.Div(
                [
                    html.Div(
                        id = "k-label",
                        children = "Vertices flipped:",
                        style = {
                            "display": "inline-block",
                            "padding-right": "10px"
                        }
                    ),
                    html.Div(
                        id = "k",
                        children = "0",
                    ),
                ],
                id = "k-stuff",
                title = "The \'k\' vertices color-flipped this turn by clicking"
            ),

            html.Div(
                [
                    # Button to advance turn
                    html.Br(),
                    html.Button(
                        id = "go-button",
                        children = "GO",
                        n_clicks = 0
                    ),

                    # Turn counter
                    html.Div(
                        id = "turn-count",
                        children = "Turn: 0",
                        style = {
                            "float": "right"
                        },
                    ),

                    # On-screen instructions
                    html.Br(),
                    html.Br(),
                    html.Div(
                        [
                            "Press \"GO\" to recolor the graph. Recoloring follows two rules:",
                            dcc.Markdown("""
                                1. If a vertex has at least one adjacent black neighbor, recolor it black.
                                2. Otherwise, recolor it white.
                            """),
                        ],
                        id = "instructions",
                    )
                ], id = "turn-stuff"
            ),

            # Error dialog for load problems
            dcc.ConfirmDialog(
                id = "error-dialog",
                displayed = False,
                message = ""
            ),

            # Graph loading via path input
            html.Hr(),
            html.Div(
                dcc.Input(
                    id = "file-path-input-box",
                    placeholder = "Enter path to graph file...",
                    type = "text",
                    value = "",
                    style = {
                        "padding-bottom": "1px"
                    }
                )
            ),
            html.Button(
                id = "load-button",
                children = "Load"
            ),
        ], id = "non-quit-elements"
    ),
    html.Div(
        [
            # Quit button
            html.Br(),
            html.Button(
                id = "quit-button",
                children = "Quit",
                n_clicks = 0,
                style = {
                    "display": "inline-block",
                    "padding-right": "10px"
                }
            ),
            html.Div(
                id = "quit-info",
                children = "(?)",
                style = {
                    "display": "inline-block",
                    "color": "rgba(0, 0, 0, 0.25)",
                    "font-weight": "900"
                },
                title = "Press when finished to stop the app and free up the port being used."
            ),
            # Quit screen
            html.Div(
                id = "quit-screen",
                style = {"display": "none"}
            )
        ], id = "quit-elements"
    )
])


@app.callback(
    [
        Output("displayed-graph", "figure"),
        Output("k", "children"),
        Output("k", "style"),
        Output("error-dialog", "displayed"),
        Output("error-dialog", "message"),
        Output("turn-count", "children")
    ],
    [
        Input("displayed-graph", "clickData"),
        Input("go-button", "n_clicks"),
        Input("load-button", "n_clicks")
    ],
    [
        State("displayed-graph", "figure"),
        State("k", "children"),
        State("file-path-input-box", "value"),
        State("turn-count", "children")
    ]
)
def clicked_vertex_or_go_or_turn_button(clickData, go_clicks, load_clicks, displayed_fig, k_curr, path, curr_turn):
    """
    This callback handles reaction to clicking:
        - a vertex in the graph
        - the "GO" button to advance the turn
        - the "Load" button to import a graph
    All three events are lumped together in this callback because all share
    Output("displayed-graph", "figure"), and an Output can only be assigned
    to one callback.
    """
    global loaded_hr_graph
    global clicked_verts_this_turn
    global node_positions

    ctx = dash.callback_context
    thing_clicked = ctx.triggered[0]["prop_id"].split(".")[0]

    k_nums = [int(i) for i in k_curr.split("/")]
    turn_num = int(curr_turn[6:])
    normal_k_color = {
        "display": "inline-block",
        "color": "black",
        "background": "white"
    }
    inverted_k_color = {
        "display": "inline-block",
        "color": "white",
        "background": "black"
    }
    ret_color = normal_k_color

    # Clicked graph vertex ###################################################
    if (thing_clicked == "displayed-graph") and (clickData is not None):
        clicked_vert_color = clickData["points"][0]["marker.color"]
        clicked_vert_id = clickData["points"][0]["text"]

        #############################
        # Flip clicked vertex color #
        #############################
        if clicked_vert_color == "black":
            new_color = "white"
        else:
            new_color = "black"

        displayed_fig["data"][0]["marker"]["color"][clickData["points"][0]["pointNumber"]] = new_color

        ####################
        # Update k readout #
        ####################
        if clicked_vert_id not in clicked_verts_this_turn:
            # If clicking this vertex for the first time (its id is not in
            # clicked_verts_this_turn), increment k
            # and store new_color (for reference when recoloring
            # loaded_hr_graph later)
            clicked_verts_this_turn[clicked_vert_id] = new_color
            if len(k_nums) == 1:
                # Still on first turn; k is shown as a single number with
                # no denominator.
                ret_str = f"{k_nums[0] + 1}"
            elif len(k_nums) == 2:
                # On turn 2 or greater; show k as n/d where n is the d from
                # previous turn and n is verts clicked this turn
                ret_str = f"{k_nums[0] + 1} / {k_nums[1]}"

                # Invert k background and color if n != d
                # (This serves as a visual aid so the user clicks the
                # same number of vertices each turn)
                if (k_nums[0] + 1) != k_nums[1]:
                    ret_color = inverted_k_color
                else:
                    ret_color = normal_k_color
        else:
            # If this vertex was already clicked (its id is already in
            # clicked_verts_this_turn), decrement k.
            clicked_verts_this_turn.pop(clicked_vert_id)
            if len(k_nums) == 1:
                ret_str = f"{k_nums[0] - 1}"
            elif len(k_nums) == 2:
                ret_str = f"{k_nums[0] - 1 } / {k_nums[1]}"

                if (k_nums[0] - 1) != k_nums[1]:
                    ret_color = inverted_k_color
                else:
                    ret_color = normal_k_color

        return displayed_fig, ret_str, ret_color, False, "", curr_turn
    # Clicked GO button ########################################################
    elif (thing_clicked == "go-button") and (go_clicks):
        ################################
        # Recolor graph and update fig #
        ################################
        for id in clicked_verts_this_turn.keys():
            loaded_hr_graph.get_vert(id).color = clicked_verts_this_turn[id]
        hr_logic.recolor(loaded_hr_graph)

        new_fig = figure_from_hr_graph(loaded_hr_graph)

        ####################
        # Update k readout #
        ####################
        clicked_verts_this_turn.clear()

        # Show n/d where n is 0 and d is n from previous turn
        if k_nums[0] == 0:
            ret_color = normal_k_color
        else:
            ret_color = inverted_k_color

        return new_fig, f"0 / {k_nums[0]}", ret_color, False, "", f"Turn: {turn_num + 1}"
    # Clicked Load button ######################################################
    elif (thing_clicked == "load-button") and (load_clicks):
        try:
            loaded_hr_graph = hr_io.load_graph(path)
        except Exception as e:
            return displayed_fig, k_curr, normal_k_color, True, repr(e), curr_turn

        node_positions = None # Wipe positions to regenerate for new graph
        new_fig = figure_from_hr_graph(loaded_hr_graph)

        return new_fig, k_curr, normal_k_color, False, "", "Turn: 0"
    # Nothing clicked; standard Dash trigger of all callbacks at startup #######
    else:
        return displayed_fig, k_curr, normal_k_color, False, "", curr_turn


@app.callback(
    [
        Output("non-quit-elements", "style"),
        # Quit screen elements below this line
        Output("quit-screen", "style"),
        Output("quit-screen", "children"),
        Output("quit-button", "style"),
        Output("quit-info", "style"),
        Output("quit-button", "value") # Dummy output; only need to call func().
    ],
    [Input("quit-button", "n_clicks")],
    [
        State("quit-button", "style"),
        State("quit-info", "style")
    ]
)
def quit(n_clicks, quit_button_style, quit_info_style):
    """Terminate the app."""
    hide = {"display": "none"}
    show = {"display": "block"}

    if n_clicks > 0:
        # Quit button pressed
        shutdown_func = request.environ.get("werkzeug.server.shutdown")

        if shutdown_func is None:
            raise RuntimeError("Not running with the Werkzeug Server")

        return (
            hide, # non-quit-elements: style
            show, # quit-screen: style
            """App stopped; safe to close this tab or window.""", # quit-screen: children
            hide, # quit-button: style
            hide, # quit-info: style
            shutdown_func() # quit-button: value
        )
    else:
        return (
            show, # non-quit-elements: style
            hide, # quit-screen: style
            "", # quit-screen: children
            quit_button_style, # quit-button: style
            quit_info_style, # quit-info: style
            None # quit-button: value
        )


def main():
    # Probable free ports in the 8000s according to:
    # http://www.networksorcery.com/enp/protocol/ip/ports08000.htm
    free_ports = [
        8004, 8006, 8007, 8009, 8010, 8011, 8012, 8013, 8014, 8015, 8016, 8017,
        8018, 8023, 8024, 8027, 8028, 8029, 8030, 8031, 8035, 8036, 8037, 8038,
        8039, 8045, 8046, 8047, 8048, 8049, 8050, 8061, 8062, 8063, 8064, 8065,
        8066, 8067, 8068, 8069, 8070, 8071, 8072, 8073, 8075, 8076, 8077, 8078,
        8079, 8084, 8085, 8089, 8092, 8093, 8094, 8095, 8096, 8098, 8099, 8102,
        8103, 8104, 8105, 8106, 8107, 8108, 8109, 8110, 8111, 8112, 8113, 8114,
        8117, 8119, 8120, 8123, 8124, 8125, 8126, 8127, 8133, 8134, 8135, 8136,
        8137, 8138, 8139, 8140, 8141, 8142, 8143, 8144, 8145, 8146, 8147, 8154,
        8155, 8156, 8157, 8158, 8159, 8162, 8163, 8164, 8165, 8166, 8167, 8168,
        8169, 8170, 8171, 8172, 8173, 8174, 8175, 8176, 8177, 8178, 8179, 8180,
        8196, 8197, 8198, 8203, 8209, 8210, 8211, 8212, 8213, 8214, 8215, 8216,
        8217, 8218, 8219, 8220, 8221, 8222, 8223, 8224, 8225, 8226, 8227, 8228,
        8229, 8231, 8232, 8233, 8234, 8235, 8236, 8237, 8238, 8239, 8240, 8241,
        8242, 8244, 8245, 8246, 8247, 8248, 8249, 8250, 8251, 8252, 8253, 8254,
        8255, 8256, 8257, 8258, 8259, 8260, 8261, 8262, 8263, 8264, 8265, 8266,
        8267, 8268, 8269, 8270, 8271, 8272, 8273, 8274, 8275, 8277, 8278, 8279,
        8281, 8282, 8283, 8284, 8285, 8286, 8287, 8288, 8289, 8290, 8291, 8295,
        8296, 8297, 8298, 8299, 8302, 8303, 8304, 8305, 8306, 8307, 8308, 8309,
        8310, 8311, 8312, 8314, 8315, 8316, 8317, 8318, 8319, 8322, 8323, 8324,
        8325, 8326, 8327, 8328, 8329, 8330, 8331, 8332, 8333, 8334, 8335, 8336,
        8337, 8338, 8339, 8340, 8341, 8342, 8343, 8344, 8345, 8346, 8347, 8348,
        8349, 8350, 8352, 8353, 8354, 8355, 8356, 8357, 8358, 8359, 8360, 8361,
        8362, 8363, 8364, 8365, 8366, 8367, 8368, 8369, 8370, 8371, 8372, 8373,
        8374, 8375, 8381, 8382, 8384, 8385, 8386, 8387, 8388, 8389, 8390, 8391,
        8392, 8393, 8394, 8395, 8396, 8397, 8398, 8399, 8401, 8402, 8403, 8406,
        8407, 8408, 8409, 8410, 8411, 8412, 8413, 8414, 8418, 8419, 8420, 8421,
        8422, 8423, 8424, 8425, 8426, 8427, 8428, 8429, 8430, 8431, 8432, 8433,
        8434, 8435, 8436, 8437, 8438, 8439, 8440, 8441, 8446, 8447, 8448, 8449,
        8451, 8452, 8453, 8454, 8455, 8456, 8458, 8459, 8460, 8461, 8462, 8463,
        8464, 8465, 8466, 8467, 8468, 8469, 8475, 8476, 8477, 8478, 8479, 8480,
        8481, 8482, 8483, 8484, 8485, 8486, 8487, 8488, 8489, 8490, 8491, 8492,
        8493, 8494, 8495, 8496, 8497, 8498, 8499, 8502, 8503, 8504, 8505, 8506,
        8507, 8508, 8509, 8510, 8511, 8512, 8513, 8514, 8515, 8516, 8517, 8518,
        8519, 8520, 8521, 8522, 8523, 8524, 8525, 8526, 8527, 8528, 8529, 8530,
        8531, 8532, 8533, 8534, 8535, 8536, 8537, 8538, 8539, 8540, 8541, 8542,
        8543, 8544, 8545, 8546, 8547, 8548, 8549, 8550, 8551, 8552, 8553, 8556,
        8557, 8558, 8559, 8560, 8561, 8562, 8563, 8564, 8565, 8566, 8568, 8569,
        8570, 8571, 8572, 8573, 8574, 8575, 8576, 8577, 8578, 8579, 8580, 8581,
        8582, 8583, 8584, 8585, 8586, 8587, 8588, 8589, 8590, 8591, 8592, 8593,
        8594, 8595, 8596, 8597, 8598, 8599, 8601, 8602, 8603, 8604, 8605, 8606,
        8607, 8608, 8616, 8617, 8618, 8619, 8620, 8621, 8622, 8623, 8624, 8625,
        8626, 8627, 8628, 8629, 8630, 8631, 8632, 8633, 8634, 8635, 8636, 8637,
        8638, 8639, 8640, 8641, 8642, 8643, 8644, 8645, 8646, 8647, 8648, 8649,
        8650, 8651, 8652, 8653, 8654, 8655, 8656, 8657, 8658, 8659, 8660, 8661,
        8662, 8663, 8664, 8665, 8666, 8667, 8668, 8669, 8670, 8671, 8672, 8673,
        8674, 8676, 8677, 8678, 8679, 8680, 8681, 8682, 8683, 8684, 8685, 8687,
        8689, 8690, 8691, 8692, 8693, 8694, 8695, 8696, 8697, 8698, 8700, 8701,
        8702, 8703, 8704, 8705, 8706, 8707, 8708, 8709, 8710, 8712, 8713, 8714,
        8715, 8716, 8717, 8718, 8719, 8720, 8721, 8722, 8723, 8724, 8725, 8726,
        8727, 8728, 8729, 8730, 8731, 8734, 8735, 8736, 8737, 8738, 8739, 8740,
        8741, 8742, 8743, 8744, 8745, 8746, 8747, 8748, 8749, 8750, 8751, 8752,
        8753, 8754, 8755, 8756, 8757, 8758, 8759, 8760, 8761, 8762, 8766, 8767,
        8768, 8769, 8771, 8772, 8773, 8774, 8775, 8776, 8777, 8778, 8779, 8780,
        8781, 8782, 8783, 8784, 8785, 8788, 8789, 8790, 8791, 8792, 8794, 8795,
        8796, 8797, 8798, 8799, 8801, 8802, 8803, 8805, 8806, 8807, 8808, 8809,
        8810, 8811, 8812, 8813, 8814, 8815, 8816, 8817, 8818, 8819, 8820, 8821,
        8822, 8823, 8824, 8825, 8826, 8827, 8828, 8829, 8830, 8831, 8832, 8833,
        8834, 8835, 8836, 8837, 8838, 8839, 8840, 8841, 8842, 8843, 8844, 8845,
        8846, 8847, 8848, 8849, 8850, 8851, 8852, 8853, 8854, 8855, 8856, 8857,
        8858, 8859, 8860, 8861, 8862, 8863, 8864, 8865, 8866, 8867, 8868, 8869,
        8870, 8871, 8872, 8874, 8875, 8876, 8877, 8878, 8879, 8882, 8884, 8885,
        8886, 8887, 8895, 8896, 8897, 8898, 8902, 8903, 8904, 8905, 8906, 8907,
        8908, 8909, 8914, 8915, 8916, 8917, 8918, 8919, 8920, 8921, 8922, 8923,
        8924, 8925, 8926, 8927, 8928, 8929, 8930, 8931, 8932, 8933, 8934, 8935,
        8936, 8938, 8939, 8940, 8941, 8942, 8943, 8944, 8945, 8946, 8947, 8948,
        8949, 8950, 8951, 8952, 8955, 8956, 8957, 8958, 8959, 8960, 8961, 8962,
        8963, 8964, 8965, 8966, 8967, 8968, 8969, 8970, 8971, 8972, 8973, 8974,
        8975, 8976, 8977, 8978, 8979, 8980, 8981, 8982, 8983, 8984, 8985, 8986,
        8987, 8988, 8992, 8993, 8994, 8995, 8996, 8997, 8998
    ]
    # Launch with a random port from the above.
    #
    # Using a random port is better than hoping the user hits Quit: if the
    # user doesn't hit Quit, the port used will remain occupied.
    # If that weren't bad enough, the app can't be re-launched on the same port.
    # With 825 ports to pick from, it's unlikely that even a user who never
    # hits Quit will launch an instance of the app using the same port before
    # the next reboot (when all app instances are killed and all ports freed).
    port = random.choice(free_ports)

    webbrowser.open("") # Autolaunch browser
    # Unfortunately, the Dash app seems to start with a variable delay.
    # Every few starts (especially when the browser isn't
    # already open), the browser starts and loads http://localhost:{port}
    # before Dash has initialized.
    # A refresh on the page handles this, but it's annoying.
    # It doesn't seem to happen with a delay of 2 seconds or longer between
    # the browser starting and loading the app page.
    # Ugly since we have to open a new window and a new tab in it, but seems to
    # guarantee successful load. As a plus, it doesn't hijack existing browser
    # windows.
    sleep(2)
    webbrowser.open_new_tab(f"http://localhost:{port}") # Open tab to app
    app.run_server(debug = False, port = port) # Launch Dash app

if __name__ == "__main__":
    main()
