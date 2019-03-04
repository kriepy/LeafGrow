import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.path import Path
import matplotlib.patches as patches
import numpy as np

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

patch = None

def update(i):
    for ver in range(len(verts)):
        verts[ver] = 1.05 * verts[ver]
    print(path)
    return [patch, ]

fig, ax = plt.subplots()
path = Path(verts, codes)
patch = patches.PathPatch(path, facecolor='green', lw=1)
ax.add_patch(patch)

ax.set_xlim(-100, 100)
ax.set_ylim(-0.1, 200)

ani = animation.FuncAnimation(fig, update, 40, repeat=False, blit=True)

plt.show()