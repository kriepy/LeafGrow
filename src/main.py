import json
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
from configparser import ConfigParser
from matplotlib.animation import FuncAnimation

import utils

# load config file
parser = ConfigParser()
parser.read('init.config')
config = parser['DEFAULT']

# init graph with edges
graph = nx.Graph()
edges = graph.edges()

# init figure for matplotlib
fig = plt.figure(figsize=(config.getfloat('figure_size_x'),config.getfloat('figure_size_y')))
ax = fig.add_subplot(111)
x_min = config.getint('scale_factor') * config.getint('axis_xlim_min')
x_max = config.getint('scale_factor') * config.getint('axis_xlim_max')
y_min = config.getint('scale_factor') * config.getfloat('axis_ylim_min')
y_max = config.getint('scale_factor') * config.getint('axis_ylim_max')
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)

# init used variables with empty values
patch = None
path_codes = [Path.MOVETO,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        ]
leaf_outline_verts = np.zeros(shape=[7,2])
vein_nodes_list = []

# init the path to be drawn
path = Path(leaf_outline_verts, path_codes)

def update_vein_nodes(i):

    # the leaf outline changes in every iteration
    # new auxin nodes must fall within this outlines
    # locations of the new auxin nodes are chosen randomly
    # for now the x locations are gathered from a uniform distribution
    # as well as the y locations
    bounding_box = path.get_extents()
    ymin = bounding_box.y0
    ymax = bounding_box.y1
    xmin = bounding_box.x0
    xmax = bounding_box.x1
    nr_auxin_nodes = config.getint('nr_auxin_nodes')

    auxin_nodes = utils.get_auxin_nodes(ymin, ymax, xmin, xmax, nr_auxin_nodes, path)
    # auxin_transpose = auxin_nodes.transpose()
    # plt.plot(auxin_transpose[0], auxin_transpose[1])
    H, new_vein_nodes = utils.get_new_graph_and_vein_nodes(np.array(vein_nodes_list), auxin_nodes, graph)
    vein_nodes_list.extend(new_vein_nodes)

    edges = H.edges()
    pos = nx.get_node_attributes(graph, 'pos')
    nx.draw(H, pos, with_labels=False, edges=edges, width=1, edge_color=config.get('edge_color'), node_size=0)

def update_leaf(i):
    for ver in range(len(leaf_outline_verts)):
        leaf_outline_verts[ver] = (1.01 - 0.0002*i) * leaf_outline_verts[ver]

def update(i):
    update_vein_nodes(i)
    update_leaf(i)

def animate(data):
    print("start animation")
     # Create a nx Graph, add vein nodes and draw them
    vein_node_index = 0
    for vein in data["vein_nodes_init"]:
        graph.add_node(vein_node_index, pos=(vein['x'], vein['y']))
        vein_nodes_list.append([vein["x"],vein["y"]])
        vein_node_index += 1

    graph.add_edge(0,1)
    graph.add_edge(1,2)
    pos=nx.get_node_attributes(graph,'pos')
    nx.draw(graph, pos, with_labels=False, edges=edges, width=1, edge_color=config.get('edge_color'), node_size=0)

    leaf_path = data["leaf_path"]
    leaf_outline_verts[:] = config.getint('scale_factor') * np.asarray(leaf_path)

    patch = patches.PathPatch(path, facecolor=config.get('face_color'), lw=1)
    patch.set_edgecolor(config.get('edge_color'))
    ax.add_patch(patch)

    # Note: the variable 'animation' is needed to see something
    #pylint: disable=unused-variable
    animation = FuncAnimation(fig, update, config.getint('nr_of_steps'), interval=100, repeat=False)
    # animation.save('leaf.gif', dpi=80, writer='imagemagick')
    plt.show()

with open("data.json", "r") as read_file:
    data = json.load(read_file)
    animate(data)
