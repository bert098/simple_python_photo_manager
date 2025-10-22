from image_lib.geometry import point_in_polygon

def test_point_in_polygon_square():
    poly = [(0, 0), (0, 1), (1, 1), (1, 0)]
    assert point_in_polygon(0.5, 0.5, poly) is True
    assert point_in_polygon(1.5, 0.5, poly) is False
