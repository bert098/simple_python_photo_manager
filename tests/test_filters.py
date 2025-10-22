import pandas as pd
from image_lib.filters import apply_tag_filters, apply_polygon_filter

def test_apply_tag_filters():
    df = pd.DataFrame({
        "Favorite": ["Yes", "No", "Yes"],
        "DPI": [72, 300, 15],
        "Type": ["jpeg", "tiff", "png"],
        "User Tags": ["Urban, Dusk", "Portrait", "Landscape"]
    })
    mask = apply_tag_filters(df, ["Favorite==Yes", "DPI>20"])
    assert mask.tolist() == [True, False, False]
    mask2 = apply_tag_filters(df, ["Type in [jpeg, tiff]", "User Tags~dusk"])
    assert mask2.tolist() == [True, False, False]

def test_apply_polygon_filter():
    df = pd.DataFrame({"lat": [0.5, 1.5], "lon": [0.5, 0.5]})
    poly = [(0, 0), (0, 1), (1, 1), (1, 0)]
    mask = apply_polygon_filter(df, poly)
    assert mask.tolist() == [True, False]
