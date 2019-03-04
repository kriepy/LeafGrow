import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
import matplotlib.animation as animation

import utils
import numpy as np

import json

# ----------------LEAF SHAPE------------------
verts = np.array([
    [0., 0.],
    [10., 3.],
    [3., 9.],
    [0, 18.],
    [-3, 9],
    [-10, 3],
    [0, 0],
    ])

codes = [Path.MOVETO,
         Path.CURVE4,
         Path.CURVE4,
         Path.CURVE4,
         Path.CURVE4,
         Path.CURVE4,
         Path.CURVE4,
         ]

def update(i):
    for ver in range(len(verts)):
        verts[ver] = 1.05 * verts[ver]
    return [patch, ]

path = Path(verts, codes)

fig = plt.figure()
ax = fig.add_subplot(111)
patch = patches.PathPatch(path, facecolor='green', lw=1)
ax.add_patch(patch)

ax.set_xlim(-10, 10)
ax.set_ylim(-0.1, 20)
# plt.axis('off')

with open("src/data.json", "r") as read_file:
    data = json.load(read_file)

    # Draw vein nodes
    xv = [d["x"] for d in data["vein_nodes"]]
    yv = [d["y"] for d in data["vein_nodes"]]
    ax.plot(xv, yv, 'ko-')


    # Draw auxin nodes
    xa = [d["x"] for d in data["auxin_nodes"]]
    ya = [d["y"] for d in data["auxin_nodes"]]
    ax.plot(xa, ya, 'ro')

    print(utils.get_new_vein_nodes(xv, yv, xa, ya))
    ani = animation.FuncAnimation(fig, update, 0, repeat=False, blit=True)

    plt.show()