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
    Euclidean distance between two vectors of the same length.
    :param u a vectors
    :param v other vector
    :return distance between vectors
    """
    d = 0
    for i in range(len(u)):
        d += (u[i] - v[i])**2
    return math.sqrt(d)

def scale_and_center(index, top):
    """
    This scales the block index to the range [-1,1]
    
    :param index: index of block along a given dimension
    :param top: number of blocks along the given dimension
    """
    return 0.0 if top == 1 else -1.0 + 2.0 * index / (top - 1)
