import novelty_distance_metrics as ndm
import pytest
import numpy as np

# Global variables, stores in a dictionary
def pytest_namespace():
    return {'arr1': np.array([1,2,3,4,5]),'arr2': np.array([1,2,3,4,5]),'arr3': np.array([0,0,0,0,0]),'arr4': np.array([5,4,3,2,1]),
    'long_arr1': np.array([1,2,3,4,5,6,7,8,9,10]),'long_arr2': np.array([1,80,0,9,8,8,2,3,0,0]),'long_arr3': np.array([2,34,8,5,-2,30,-123,7,23,4]),
    'hamming_arr1': np.array([8,6,7,5,3,0,9,1,8,0,0,9,8,8,2,3,0,0]),'hamming_arr2': np.array([8,6,7,5,3,0,9,12,-90,12,564,-1000,5,21,564,9,10,0]),
    'hamming_arr3': np.array([5,5,5,5,5,9,5,5,8,5,5,5,5,5,3,2,5,5]),'hamming_arr4': np.array([5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5]),
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

def test_hamming_distance():
    assert ndm.hamming_distance(pytest_namespace()['arr1'],pytest_namespace()['arr2']) == 0
    assert ndm.hamming_distance(pytest_namespace()['arr1'],pytest_namespace()['arr3']) == 5
    assert ndm.hamming_distance(pytest_namespace()['arr1'],pytest_namespace()['arr4']) == 4
    assert ndm.hamming_distance(pytest_namespace()['arr2'],pytest_namespace()['arr3']) == 5
    assert ndm.hamming_distance(pytest_namespace()['arr2'],pytest_namespace()['arr4']) == 4
    assert ndm.hamming_distance(pytest_namespace()['arr3'],pytest_namespace()['arr4']) == 5

    assert ndm.hamming_distance(pytest_namespace()['point1'],pytest_namespace()['point2']) == 2
    assert ndm.hamming_distance(pytest_namespace()['point1'],pytest_namespace()['point3']) == 2
    assert ndm.hamming_distance(pytest_namespace()['point1'],pytest_namespace()['point4']) == 2
    assert ndm.hamming_distance(pytest_namespace()['point2'],pytest_namespace()['point3']) == 2
    assert ndm.hamming_distance(pytest_namespace()['point2'],pytest_namespace()['point4']) == 2
    assert ndm.hamming_distance(pytest_namespace()['point3'],pytest_namespace()['point4']) == 2
    assert ndm.hamming_distance(pytest_namespace()['point3'],pytest_namespace()['point3']) == 0

    assert ndm.hamming_distance(pytest_namespace()['long_arr1'],pytest_namespace()['long_arr1']) == 0
    assert ndm.hamming_distance(pytest_namespace()['long_arr1'],pytest_namespace()['long_arr2']) == 9
    assert ndm.hamming_distance(pytest_namespace()['long_arr1'],pytest_namespace()['long_arr3']) == 10
    assert ndm.hamming_distance(pytest_namespace()['long_arr2'],pytest_namespace()['long_arr3']) == 10

    assert ndm.hamming_distance(pytest_namespace()['hamming_arr1'],pytest_namespace()['hamming_arr2']) == 10
    assert ndm.hamming_distance(pytest_namespace()['hamming_arr1'],pytest_namespace()['hamming_arr3']) == 16
    assert ndm.hamming_distance(pytest_namespace()['hamming_arr1'],pytest_namespace()['hamming_arr4']) == 17
    assert ndm.hamming_distance(pytest_namespace()['hamming_arr2'],pytest_namespace()['hamming_arr3']) == 16
    assert ndm.hamming_distance(pytest_namespace()['hamming_arr2'],pytest_namespace()['hamming_arr4']) == 16
    assert ndm.hamming_distance(pytest_namespace()['hamming_arr3'],pytest_namespace()['hamming_arr4']) == 4

    assert ndm.hamming_distance(pytest_namespace()['ones'],pytest_namespace()['zeroes']) == 50
    assert ndm.hamming_distance(pytest_namespace()['ones'],pytest_namespace()['ones']) == 0
    assert ndm.hamming_distance((pytest_namespace()['ones']+3),pytest_namespace()['zeroes']) == 50
    assert ndm.hamming_distance((pytest_namespace()['ones']-1),pytest_namespace()['zeroes']) == 0

def test_custom_hamming_distance():
    assert ndm.custom_hamming_distance(pytest_namespace()['arr1'],pytest_namespace()['arr2']) == 0
    assert ndm.custom_hamming_distance(pytest_namespace()['arr1'],pytest_namespace()['arr3']) == pytest.approx(1.2)
    assert ndm.custom_hamming_distance(pytest_namespace()['arr1'],pytest_namespace()['arr4']) == pytest.approx(2.1)
    assert ndm.custom_hamming_distance(pytest_namespace()['arr2'],pytest_namespace()['arr3']) == pytest.approx(1.2)
    assert ndm.custom_hamming_distance(pytest_namespace()['arr2'],pytest_namespace()['arr4']) == pytest.approx(2.1)
    assert ndm.custom_hamming_distance(pytest_namespace()['arr3'],pytest_namespace()['arr4']) == pytest.approx(1.2)

    assert ndm.custom_hamming_distance(pytest_namespace()['point1'],pytest_namespace()['point2']) == pytest.approx(.1)
    assert ndm.custom_hamming_distance(pytest_namespace()['point1'],pytest_namespace()['point3']) == pytest.approx(1.05)
    assert ndm.custom_hamming_distance(pytest_namespace()['point1'],pytest_namespace()['point4']) == pytest.approx(.1)
    assert ndm.custom_hamming_distance(pytest_namespace()['point2'],pytest_namespace()['point3']) == pytest.approx(1.05)
    assert ndm.custom_hamming_distance(pytest_namespace()['point2'],pytest_namespace()['point4']) == pytest.approx(.1)
    assert ndm.custom_hamming_distance(pytest_namespace()['point3'],pytest_namespace()['point4']) == pytest.approx(1.05)
    assert ndm.custom_hamming_distance(pytest_namespace()['point3'],pytest_namespace()['point3']) == 0

    assert ndm.custom_hamming_distance(pytest_namespace()['long_arr1'],pytest_namespace()['long_arr1']) == 0
    assert ndm.custom_hamming_distance(pytest_namespace()['long_arr1'],pytest_namespace()['long_arr2']) == pytest.approx(1.4)
    assert ndm.custom_hamming_distance(pytest_namespace()['long_arr1'],pytest_namespace()['long_arr3']) == pytest.approx(2.4)
    assert ndm.custom_hamming_distance(pytest_namespace()['long_arr2'],pytest_namespace()['long_arr3']) == pytest.approx(1.45)

    assert ndm.custom_hamming_distance(pytest_namespace()['hamming_arr1'],pytest_namespace()['hamming_arr2']) == pytest.approx(1.45)
    assert ndm.custom_hamming_distance(pytest_namespace()['hamming_arr1'],pytest_namespace()['hamming_arr3']) == pytest.approx(13.15)
    assert ndm.custom_hamming_distance(pytest_namespace()['hamming_arr1'],pytest_namespace()['hamming_arr4']) == pytest.approx(17)
    assert ndm.custom_hamming_distance(pytest_namespace()['hamming_arr2'],pytest_namespace()['hamming_arr3']) == pytest.approx(12.2)
    assert ndm.custom_hamming_distance(pytest_namespace()['hamming_arr2'],pytest_namespace()['hamming_arr4']) == pytest.approx(16)
    assert ndm.custom_hamming_distance(pytest_namespace()['hamming_arr3'],pytest_namespace()['hamming_arr4']) == pytest.approx(4)

    assert ndm.custom_hamming_distance(pytest_namespace()['ones'],pytest_namespace()['zeroes']) == pytest.approx(2.5)
    assert ndm.custom_hamming_distance(pytest_namespace()['ones'],pytest_namespace()['ones']) == 0
    assert ndm.custom_hamming_distance((pytest_namespace()['ones']+3),pytest_namespace()['zeroes']) == pytest.approx(2.5)
    assert ndm.custom_hamming_distance((pytest_namespace()['ones']-1),pytest_namespace()['zeroes']) == 0
    assert ndm.custom_hamming_distance((pytest_namespace()['ones']*5),pytest_namespace()['zeroes']) == pytest.approx(50)