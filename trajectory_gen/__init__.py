from __future__ import annotations
import math
from typing import List, Tuple


class Waypoint:
    """An x and y Location."""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __sub__(self, other):
        return Waypoint(self.x - other.x, self.y - other.y)

    def __str__(self):
        return f"{self.x},{self.y}"

    def bearing(self) -> float:
        return math.atan2(self.x, self.y) / math.pi * 180


class Line:
    """Two waypoints forming a line."""

    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def __str__(self):
        return f"{self.p1} - {self.p2}"

    def length(self) -> float:
        return math.sqrt((self.p2.x - self.p1.x)**2 +
                         (self.p2.y - self.p1.y)**2)

    def top_half_line(self) -> Line:
        """The line from p1 to the midpoint."""
        return Line(
            self.p1,
            Waypoint(
                (self.p1.x + self.p2.x) / 2,
                (self.p1.y + self.p2.y) / 2
            )
        )

    def bot_half_line(self) -> Line:
        """The line from midpoint to p2."""
        return Line(
            Waypoint(
                (self.p1.x + self.p2.x) / 2,
                (self.p1.y + self.p2.y) / 2
            ),
            self.p2,
        )

    def top_half_waypoint(self) -> Waypoint:
        """The line a quarter from p1 to p2."""
        return Waypoint(
            self.p1.x + 0.25 * (self.p2.x - self.p1.x),
            self.p1.y + 0.25 * (self.p2.y - self.p1.y)
        )

    def bot_half_waypoint(self) -> Waypoint:
        """The line three quarters from p1 to p2."""
        return Waypoint(
            self.p1.x + 0.75 * (self.p2.x - self.p1.x),
            self.p1.y + 0.75 * (self.p2.y - self.p1.y)
        )


Path = List[Waypoint]
"""A list of Waypoints for a robot to follow, with no information about speed/omega/timestmaps."""

Trajectory = List[Tuple[Waypoint, float]]
"""a Path with timestamps at each Waypoint (seconds)."""


def distance(a: Waypoint, b: Waypoint) -> float:
    """Distance between two waypoints."""
    return ((a.x - b.x)**2 + (a.y - b.y)**2)**0.5


def coterminal_minus(a: float, b: float) -> float:
    """Calculates the difference between two angles."""
    difference = _rem(_rem(a, 360) - _rem(b, 360), 360)
    if difference > 180:
        return difference - 360
    if difference < -180:
        return difference + 360
    return difference


def _rem(a, b):
    return (abs(a) % b) * (-1 if a < 0 else 1)
