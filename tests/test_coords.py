from image_lib.coords import parse_coordinate

def test_parse_coordinate_decimal():
    assert parse_coordinate("51.05011, -114.08529") == (51.05011, -114.08529)

def test_parse_coordinate_dms():
    latlon = parse_coordinate("36° 00' N, 138° 00' E")
    assert latlon is not None
    lat, lon = latlon
    assert 35.9 < lat < 36.1
    assert 137.9 < lon < 138.1
