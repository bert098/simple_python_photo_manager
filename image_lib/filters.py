import re
from typing import List, Tuple
import pandas as pd
from .geometry import point_in_polygon

OP_REGEX = re.compile(r"\s*(==|!=|>=|<=|>|<|~| in )\s*", re.IGNORECASE)


def normalize_str(s):
    return str(s).strip().lower()


def parse_tag_expression(expr: str):
    if " in " in expr.lower():
        left, right = expr.split(" in ", 1)
        field = left.strip()
        value_part = right.strip()
        if value_part.startswith("[") and value_part.endswith("]"):
            inner = value_part[1:-1]
        else:
            inner = value_part
        items = [normalize_str(x) for x in re.split(r"[,\s]+", inner) if x.strip()]
        return field, "in", items

    parts = OP_REGEX.split(expr, maxsplit=1)
    if len(parts) < 3:
        raise ValueError(f"Could not parse tag expression: {expr}")
    field, op, value = parts[0].strip(), parts[1].strip(), parts[2].strip()
    return field, op, value


def evaluate_expression(series: pd.Series, op: str, value):
    if op in (">", ">=", "<", "<="):
        try:
            numeric_series = pd.to_numeric(series, errors="coerce")
            target = float(value)
            if op == ">":
                return numeric_series > target
            if op == ">=":
                return numeric_series >= target
            if op == "<":
                return numeric_series < target
            if op == "<=":
                return numeric_series <= target
        except Exception:
            return pd.Series([False] * len(series), index=series.index)

    if op == "==":
        return series.astype(str).str.strip().str.lower() == normalize_str(value)
    if op == "!=":
        return series.astype(str).str.strip().str.lower() != normalize_str(value)
    if op == "~":
        return series.astype(str).str.lower().str.contains(str(value).lower(), na=False)
    if op == "in":
        s = series.astype(str).str.strip().str.lower()
        return s.isin(value)
    raise ValueError(f"Unsupported operator: {op}")


def apply_tag_filters(df: pd.DataFrame, tag_exprs: List[str]) -> pd.Series:
    if not tag_exprs:
        return pd.Series([True] * len(df), index=df.index)
    mask = pd.Series([True] * len(df), index=df.index)
    for expr in tag_exprs:
        field, op, value = parse_tag_expression(expr)
        if field not in df.columns:
            if field in ("lat", "lon"):
                series = df[field]
            else:
                mask &= False
                continue
        else:
            series = df[field]
        m = evaluate_expression(series, op, value)
        mask &= m.fillna(False)
    return mask


def apply_polygon_filter(df: pd.DataFrame, polygon: List[Tuple[float, float]]) -> pd.Series:
    if not polygon:
        return pd.Series([True] * len(df), index=df.index)
    poly = [(float(a), float(b)) for a, b in polygon]
    res = []
    for la, lo in zip(df["lat"], df["lon"]):
        if la is None or lo is None or (pd.isna(la) or pd.isna(lo)):
            res.append(False)
        else:
            res.append(point_in_polygon(float(la), float(lo), poly))
    return pd.Series(res, index=df.index)
