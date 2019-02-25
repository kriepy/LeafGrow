import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches

verts = [
    (0., 0.),  # P0
    (100., 30.), # P1
    (30., 90.), # P2
    (0, 180.), # P3
    (-30, 90),
    (-100, 30),
    (0, 0),
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

fig = plt.figure()
ax = fig.add_subplot(111)
patch = patches.PathPatch(path, facecolor='green', lw=1)
ax.add_patch(patch)

ax.set_xlim(-100, 100)
ax.set_ylim(-0.1, 200)
# plt.axis('off')
plt.show()