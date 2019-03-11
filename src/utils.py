import numpy as np
import networkx as nx

def euclidean_distance(v1,v2):
    return np.linalg.norm(v1-v2)

# returns the index of the array that has the smallest value in the array
def minimum_index(arr):
    a = np.array(arr)
    indices = np.where(a == a.min())
    return indices[0][0]

def get_new_vein_nodes(xv, yv, xa, ya, G):
    """Returns a list of new vein nodes given the previouse vein and the auxin nodes"""

    # make numpy arrays of vein- and auxin-nodes 
    v = []
    for vi in range(len(xv)):
        v.append(np.array((xv[vi], yv[vi])))
    a = []
    for ai in range(len(xa)):
        a.append(np.array((xa[ai], ya[ai])))

    # calculate new vein nodes

    # create an array of zeros (vein nodes normalized)
    vnn = [np.zeros(2) for _ in range(len(v))]

    # Foreach auxin node find the closest vein node
    for ai in range(len(xa)):
        dist = []
        for vi in range(len(xv)):
            dist.append(euclidean_distance(a[ai], v[vi]))

        # get the index for the closest vein node
        min_index = minimum_index(dist)

        # normalize the vec between vein and auxin node
        normalized_vec = (a[ai]-v[min_index])/np.linalg.norm(a[ai]-v[min_index])
        vnn[min_index] += normalized_vec

    vnn = list(map(lambda vec: vec/np.linalg.norm(vec) if vec.any() else vec, vnn))
    new_vein_nodes = []
    vein_node_index = len(G)
    for vi in range(len(v)):
        if vnn[vi].any():
            new_vein_nodes.append(v[vi] + vnn[vi])
            G.add_node(vein_node_index, pos=(v[vi] + vnn[vi]))
            G.add_edge(vi,vein_node_index)   
            vein_node_index += 1
    

    return G