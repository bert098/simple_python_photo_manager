import pandas as pd
from .coords import parse_coordinate


def load_metadata(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    lats, lons = [], []
    coords = df.get("(Center) Coordinate", [])
    for v in coords:
        parsed = (
            parse_coordinate(v)
            if isinstance(v, str)
            or (v is not None and not (isinstance(v, float) and pd.isna(v)))
            else None
        )
        if parsed:
            la, lo = parsed
        else:
            la, lo = (None, None)
        lats.append(la)
        lons.append(lo)
    df["lat"] = lats
    df["lon"] = lons
    return df
