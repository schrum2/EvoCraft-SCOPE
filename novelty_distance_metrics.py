from minecraft_pb2 import *
import numpy as np


def euclidean_distance(arr1,arr2):
    """
    Calculates the euclidean distance between two arrays
    
    Parameters:
    arr1(numpy array): Array containg the information of one shape
    arr2(numpy array): Array containg the information of another shape

    Return:
    edist (float): The distance calculated between the two arrays
    """
    edist = np.linalg.norm(arr1.ravel() - arr2.ravel())
    return float(edist)

def hamming_distance(arr1,arr2):
    """
    Calculates the hamming distance between two arrays. Adds 1 to sum if the 
    values are different, nothing if they're the same
    
    Parameters:
    arr1(numpy array): Array containg the information of one shape
    arr2(numpy array): Array containg the information of another shape

    Return:
    hdist (float): The distance calculated between the two arrays
    """
    hdist = sum(h1 != h2 for h1, h2 in zip(arr1, arr2))
    return float(hdist)

def custom_hamming_distance(arr1,arr2):
    """
    Custom version of the hamming distance. If one block is air and another block
    isn't, 1 is added. If the two blocks are different, but not air, .05 is added.
    If the block is the same, nothing is added 
    
    Parameters:
    arr1(numpy array): Array containg the information of one shape
    arr2(numpy array): Array containg the information of another shape

    Return:
    chdist (float): The distance calculated between the two arrays
    """
    chdist = 0
    for h1, h2 in zip(arr1, arr2):
        if h1 != h2:
            if h1==AIR or h2==AIR:
                chdist+=1
            else:
                chdist+=.05
    return float(chdist)

