import json
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

G = nx.Graph()
edges = G.edges()

fig = plt.figure()
ax = fig.add_subplot(111)

patch = None
verts = np.zeros(shape=[7,2])

def update_vein_nodes(i):
    G.add_node(i+4, pos=(1, i))
    G.add_edge(0,i+4)
    edges = G.edges()
    pos = nx.get_node_attributes(G, 'pos')
    nx.draw(G, pos, with_labels=True, edges=edges, width=2, edge_color='lightgreen', node_size=0)

def update_leaf(i):
    print("update leaf", verts)
    for ver in range(len(verts)):
        verts[ver] = 1.05 * verts[ver]
    return [patch, ]

def update(i):
    print("update", i)
    update_vein_nodes(i)
    return update_leaf(i)

def animate(data):
    print("start animation", data)
     # Create a nx Graph, add vein nodes and draw them
    vein_node_index = 0
    for vein in data["vein_nodes"]:
        G.add_node(vein_node_index, pos=(vein['x'], vein['y']))
        vein_node_index += 1

    G.add_edge(0,1)   
    G.add_edge(1,2)
    pos=nx.get_node_attributes(G,'pos')
    nx.draw(G, pos, with_labels=True, edges=edges, width=2, edge_color='lightgreen', node_size=0)

    # Draw a leaf
    verts[:] = [
    [0., 0.],
    [10., 3.],
    [3., 9.],
    [0, 18.],
    [-3, 9],
    [-10, 3],
    [0, 0],
    ]

    codes = [Path.MOVETO,
         Path.CURVE4,
         Path.CURVE4,
         Path.CURVE4,
         Path.CURVE4,
         Path.CURVE4,
         Path.CURVE4,
         ]

    path = Path(verts, codes)
    patch = patches.PathPatch(path, facecolor='none', lw=1)
    ax.add_patch(patch)

    # Note: the variable 'animation' is needed to see something
    animation = FuncAnimation(fig, update, 5, interval=500, repeat=False)
    plt.show()

with open("src/data.json", "r") as read_file:
    data = json.load(read_file)
    animate(data)
