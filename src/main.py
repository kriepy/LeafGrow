import json
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

import utils

G = nx.Graph()
edges = G.edges()

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlim(-100, 100)
ax.set_ylim(-0.1, 200)

patch = None
codes = [Path.MOVETO,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        ]
verts = np.zeros(shape=[7,2])
vein_nodes_list = []
path = Path(verts, codes)

def update_vein_nodes(i):
    ymin = 0
    ymax = verts[3,1]
    xvari = verts[2,0]

    auxin_nodes = utils.get_auxin_nodes(ymin, ymax, xvari, 10, path)
    H, new_vein_nodes = utils.get_new_vein_nodes(np.array(vein_nodes_list), auxin_nodes, G)
    vein_nodes_list.extend(new_vein_nodes)

    edges = H.edges()
    pos = nx.get_node_attributes(G, 'pos')
    nx.draw(H, pos, with_labels=False, edges=edges, width=2, edge_color='lightgreen', node_size=0)

def update_leaf(i):
    for ver in range(len(verts)):
        verts[ver] = 1.05 * verts[ver]

def update(i):
    print(i)
    update_vein_nodes(i)
    update_leaf(i)

def animate(data):
    print("start animation")
     # Create a nx Graph, add vein nodes and draw them
    vein_node_index = 0
    for vein in data["vein_nodes"]:
        G.add_node(vein_node_index, pos=(vein['x'], vein['y']))
        vein_nodes_list.append([vein["x"],vein["y"]])
        vein_node_index += 1

    G.add_edge(0,1)   
    G.add_edge(1,2)
    pos=nx.get_node_attributes(G,'pos')
    nx.draw(G, pos, with_labels=False, edges=edges, width=2, edge_color='lightgreen', node_size=0)

    # Draw a leaf
    # TODO: get leaf data from json file
    verts[:] = [
    [0., 0.],
    [10., 3.],
    [3., 9.],
    [0, 18.],
    [-3, 9],
    [-10, 3],
    [0, 0],
    ]

    patch = patches.PathPatch(path, facecolor='none', lw=1)
    ax.add_patch(patch)

    # Note: the variable 'animation' is needed to see something
    animation = FuncAnimation(fig, update, 50, interval=1000, repeat=False)
    plt.show()

with open("src/data.json", "r") as read_file:
    data = json.load(read_file)
    animate(data)
