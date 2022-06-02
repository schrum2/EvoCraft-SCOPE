import novelty_distance_metrics as ndm
import pytest
import numpy as np

def test_euclidean_distance():
    list1 = [1,2,3,4,5]
    list2 = [1,2,3,4,5]

    arr1 = np.array(list1)
    arr2 = np.array(list2)

    zeroes = np.zeros(50)
    ones = np.ones(50)

    assert ndm.euclidean_distance(arr1,arr2) == 0
    assert ndm.euclidean_distance(ones,zeroes) == np.sqrt(50)