import novelty_distance_metrics as ndm
import pytest
import numpy as np

# Global vars
def pytest_namespace():
    return {'arr1': np.array([1,2,3,4,5]),'arr2': np.array([1,2,3,4,5]),'arr3': np.array([0,0,0,0,0]),'arr4': np.array([5,4,3,2,1]),
    'long_arr1': np.array([1,2,3,4,5,6,7,8,9,10]),'long_arr2': np.array([1,80,0,9,8,8,2,3,0,0]),'long_arr3': np.array([2,34,8,5,-2,30,-123,7,23,4]),
    'point1': np.array([0,0]),'point2': np.array([2,2]),'point3': np.array([5,-1]),'point4': np.array([-3,6]),'zeroes':np.zeros(50),'ones':np.ones(50)}

def test_euclidean_distance():
    assert ndm.euclidean_distance(pytest_namespace()['arr1'],pytest_namespace()['arr2']) == 0
    assert ndm.euclidean_distance(pytest_namespace()['arr1'],pytest_namespace()['arr3']) == np.sqrt(55)
    assert ndm.euclidean_distance(pytest_namespace()['arr4'],pytest_namespace()['arr3']) == np.sqrt(55)
    assert ndm.euclidean_distance(pytest_namespace()['arr1'],pytest_namespace()['arr4']) == np.sqrt(40)
    assert ndm.euclidean_distance(pytest_namespace()['arr2'],pytest_namespace()['arr4']) == np.sqrt(40)

    assert ndm.euclidean_distance(pytest_namespace()['point1'],pytest_namespace()['point2']) == np.sqrt(8)
    assert ndm.euclidean_distance(pytest_namespace()['point1'],pytest_namespace()['point3']) == np.sqrt(26)
    assert ndm.euclidean_distance(pytest_namespace()['point1'],pytest_namespace()['point4']) == np.sqrt(45)
    assert ndm.euclidean_distance(pytest_namespace()['point2'],pytest_namespace()['point3']) == np.sqrt(18)
    assert ndm.euclidean_distance(pytest_namespace()['point2'],pytest_namespace()['point4']) == np.sqrt(41)
    assert ndm.euclidean_distance(pytest_namespace()['point3'],pytest_namespace()['point4']) == np.sqrt(113)
    assert ndm.euclidean_distance(pytest_namespace()['point3'],pytest_namespace()['point3']) == 0

    # Calculated by hand to verify
    assert ndm.euclidean_distance(pytest_namespace()['long_arr1'],pytest_namespace()['long_arr1']) == 0
    assert ndm.euclidean_distance(pytest_namespace()['long_arr1'],pytest_namespace()['long_arr2']) == np.sqrt(6362)
    assert ndm.euclidean_distance(pytest_namespace()['long_arr1'],pytest_namespace()['long_arr3']) == np.sqrt(18809)
    assert ndm.euclidean_distance(pytest_namespace()['long_arr2'],pytest_namespace()['long_arr3']) == np.sqrt(18967)

    assert ndm.euclidean_distance(pytest_namespace()['ones'],pytest_namespace()['zeroes']) == np.sqrt(50)
    assert ndm.euclidean_distance(pytest_namespace()['ones'],pytest_namespace()['ones']) == 0
    assert ndm.euclidean_distance((pytest_namespace()['ones']+3),pytest_namespace()['zeroes']) == np.sqrt(800)
