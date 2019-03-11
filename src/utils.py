import random
import numpy as np
import networkx as nx

def euclidean_distance(v1,v2):
    return np.linalg.norm(v1-v2)

# returns the index of the array that has the smallest value in the array
def minimum_index(arr):
    a = np.array(arr)
    indices = np.where(a == a.min())
    return indices[0][0]

def get_auxin_nodes(ymin, ymax, xvari, nr, path):
    """Returns a list of random points within the given path
    nr - is the number of points to return
    """
    
    auxin_list = []

    for _ in range(0,nr):
        x = random.normalvariate(0,xvari)
        y = random.uniform(ymin,ymax)
        while(not path.contains_point([x,y])):
            x = random.normalvariate(0,xvari)
            y = random.uniform(ymin,ymax)

        auxin_list.append((x,y))
    return np.array(auxin_list)

def get_new_vein_nodes(v, a, G):
    """Returns the graph object with new vein nodes given the previouse vein and the auxin nodes"""

    # ---------calculate new vein nodes--------------------------

    # create an array of zeros (vein nodes normalized)
    vnn = [np.zeros(2) for _ in range(len(v))]

    # Foreach auxin node find the closest vein node
    for ai in range(len(a)):
        dist = []
        for vi in range(len(v)):
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
            new_vein_nodes.append((v[vi] + vnn[vi]).tolist())
            G.add_node(vein_node_index, pos=(v[vi] + vnn[vi]))
            G.add_edge(vi,vein_node_index)   
            vein_node_index += 1
    
    return G, new_vein_nodes