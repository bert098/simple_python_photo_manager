import re
from typing import Optional, Tuple

dms_pattern = re.compile(
    r"^\s*(\d{1,3})[°:\s]\s*(\d{1,2})?'?\s*(\d{1,2})?\"?\s*([NSEW])\s*,\s*"
    r"(\d{1,3})[°:\s]\s*(\d{1,2})?'?\s*(\d{1,2})?\"?\s*([NSEW])\s*$",
    re.IGNORECASE,
)


def dms_to_decimal(deg: int, minutes: int = 0, seconds: int = 0, hemi: str = "N") -> float:
    sign = -1 if hemi.upper() in ("S", "W") else 1
    return sign * (float(deg) + float(minutes) / 60.0 + float(seconds) / 3600.0)


def parse_coordinate(coord: str) -> Optional[Tuple[float, float]]:
    if not isinstance(coord, str) or not coord.strip():
        return None
    s = coord.strip()
    # Try decimal
    try:
        if "," in s:
            a, b = s.split(",", 1)
            lat = float(a.strip().replace("°", ""))
            lon = float(b.strip().replace("°", ""))
            if -90 <= lat <= 90 and -180 <= lon <= 180:
                return (lat, lon)
    except Exception:
        pass
    # Try DMS
    m = dms_pattern.match(s)
    if m:
        d1, m1, s1, h1, d2, m2, s2, h2 = m.groups()
        lat = dms_to_decimal(int(d1), int(m1 or 0), int(s1 or 0), h1)
        lon = dms_to_decimal(int(d2), int(m2 or 0), int(s2 or 0), h2)
        if -90 <= lat <= 90 and -180 <= lon <= 180:
            return (lat, lon)
    return None
