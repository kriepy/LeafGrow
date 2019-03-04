import numpy as np

def euclidean_distance(v1,v2):
    return np.linalg.norm(v1-v2)

# returns the index of the array that has the smallest value in the array
def minimum_index(arr):
    a = np.array(arr)
    indices = np.where(a == a.min())
    return indices[0][0]

# returns new vein nodes
def get_new_vein_nodes(xv, yv, xa, ya):

    # make numpy arrays of vein- and auxin-nodes 
    v = []
    for vi in range(len(xv)):
        v.append(np.array((xv[vi], yv[vi])))
    a = []
    for ai in range(len(xa)):
        a.append(np.array((xa[ai], ya[ai])))

    # calculate new vein nodes
    vnv = [np.zeros(2) for _ in range(len(v))]
    for ai in range(len(xa)):
        dist = []
        for vi in range(len(xv)):
            dist.append(euclidean_distance(a[ai], v[vi]))
        min_index = minimum_index(dist)
        normalized_vec = (a[ai]-v[min_index])/np.linalg.norm(a[ai]-v[min_index])
        vnv[min_index] += normalized_vec
    vnv = list(map(lambda vec: vec/np.linalg.norm(vec) if vec.any() else vec, vnv))
    new_vein_nodes = []
    for vi in range(len(v)):
        if vnv[vi].any():
            new_vein_nodes.append(v[vi] + vnv[vi])

    return new_vein_nodes