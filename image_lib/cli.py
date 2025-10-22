import argparse
import json
import pandas as pd
from .loader import load_metadata
from .filters import apply_tag_filters, apply_polygon_filter


def main():
    ap = argparse.ArgumentParser(description="Image Library Search (Modular)")
    ap.add_argument("--csv", required=True, help="Path to CSV with image metadata")
    ap.add_argument(
        "--tags",
        nargs="*",
        default=[],
        help="Tag expressions, e.g., 'Favorite==Yes' 'DPI>20' 'User Tags~Dusk' 'Type in [jpeg,tiff]'",
    )
    ap.add_argument(
        "--polygon",
        type=str,
        default="",
        help="JSON-like list of [lat, lon] pairs. Example: '[(51.0,-114.2),(51.0,-113.9),(51.2,-113.9),(51.2,-114.2)]'",
    )
    ap.add_argument("--limit", type=int, default=1000, help="Max rows to display")
    args = ap.parse_args()

    df = load_metadata(args.csv)
    mask_tags = apply_tag_filters(df, args.tags)

    mask_poly = pd.Series([True] * len(df), index=df.index)
    if args.polygon.strip():
        poly_text = args.polygon.strip().replace("(", "[").replace(")", "]")
        polygon = json.loads(poly_text)
        if isinstance(polygon, list) and all(
            isinstance(p, (list, tuple)) and len(p) == 2 for p in polygon
        ):
            mask_poly = apply_polygon_filter(
                df, [(float(p[0]), float(p[1])) for p in polygon]
            )
        else:
            raise ValueError("Polygon must be a list of [lat, lon] pairs")

    final_mask = mask_tags & mask_poly
    out = df[final_mask].copy()

    print(f"\nMatched {len(out)} of {len(df)} rows.\n")
    pd.set_option("display.max_columns", None)
    print(out.head(args.limit).to_string(index=False))
    out.to_csv("results.csv", index=False)
    print("\nSaved results to results.csv")
