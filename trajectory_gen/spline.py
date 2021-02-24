import numpy as np
from scipy import interpolate
from . import Waypoint, Path


def generate(points: Path) -> Path:
    """Generate spline curves going through a set of points."""

    # TODO dont do this!
    total_points = 250

    tck = interpolate.splprep([[p.x for p in points], [p.y for p in points]], s=0)[0]
    x, y = interpolate.splev(np.linspace(0, 1, total_points), tck)

    return list(map(lambda a: Waypoint(a[0], a[1]), zip(x, y)))
