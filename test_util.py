import util
import pytest

def test_argmax():
    assert util.argmax([1,2,3,4,5]) == 4
    assert util.argmax([1,2,3,2,1,2]) == 2
    assert util.argmax([-0.32, 0.75, 0.2, 0.51, -0.2, 0.002]) == 1
    assert util.argmax([-1.2, -100.23, -32, -0.342, -93.32, -0.233, -2.47]) == 5

def test_distance():
    assert util.distance((0,0),(3,4)) == 5.0
    assert util.distance((1,2,0.5),(17,6.7,2)) == pytest.approx(16.743357)
    assert util.distance((-51,2.4,-100.5),(241,6.7,-22)) == pytest.approx(302.398313)

def test_scale_and_center():
    assert util.scale_and_center(0,1) == 0
    assert util.scale_and_center(0,10) == -1.0
    assert util.scale_and_center(1,10) == pytest.approx(-0.77777777)
    assert util.scale_and_center(2,10) == pytest.approx(-0.55555555)
    assert util.scale_and_center(3,10) == pytest.approx(-0.33333333)
    assert util.scale_and_center(4,10) == pytest.approx(-0.11111111)
    assert util.scale_and_center(5,10) == pytest.approx( 0.11111111)
    assert util.scale_and_center(6,10) == pytest.approx( 0.33333333)
    assert util.scale_and_center(7,10) == pytest.approx( 0.55555555)
    assert util.scale_and_center(8,10) == pytest.approx( 0.77777777)
    assert util.scale_and_center(9,10) ==  1.0
