from minecraft_pb2 import *
import numpy as np

def euclidean_distance(arr1,arr2):
    adist = np.linalg.norm(arr1.ravel() - arr2.ravel())
    return adist