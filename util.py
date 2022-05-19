"""
Utility functions used will be kept in this module.
"""
import math

def argmax(l):
    """
    Finds the maximum value in a list of values
    :param l a list of numeric elements
    :return index of first maximal element
    """
    f = lambda i: l[i]
    return max(range(len(l)), key=f)

def distance(v, u):
    """
    This function uses two vectors of the same length, u and v, to 
    find the Euclidean distance between the two vectors.
    
    Parameters:
    u (Vector): Vector being used to find the distance.
    v (Vector): Vector being used to find the distance.
    
    Returns:
    int: Euclidean distance between two vectors u and v.
    """
    d = 0
    for i in range(len(u)):
        d += (u[i] - v[i])**2
    return math.sqrt(d)

def scale_and_center(index, top):    
    """
    This scales the block index to the range [-1,1]. 

    Parameters:
    index (int): The x coordinate where the number will start.
    top (int): The y coordinate where the number will start.
    """
    return 0.0 if top == 1 else -1.0 + 2.0 * index / (top - 1)
