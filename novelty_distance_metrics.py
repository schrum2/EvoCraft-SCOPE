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
    Calculates the hamming distance between two arrays
    
    Parameters:
    arr1(numpy array): Array containg the information of one shape
    arr2(numpy array): Array containg the information of another shape

    Return:
    hdist (float): The distance calculated between the two arrays
    """
    hdist = sum(h1 != h2 for h1, h2 in zip(arr1, arr2))
    return float(hdist)
