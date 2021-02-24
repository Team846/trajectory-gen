"""Trajectory calculations (copied from Kapuchin)."""

import copy
import math
from typing import Callable, List, Tuple
from . import Path, Waypoint, Trajectory, distance, coterminal_minus


def trajectory_time(traj: Trajectory) -> float:
    """Get total time of a trajectory."""

    return traj[-1][1]


def path_to_trajectory(
    path: Path,
    max_velocity: float, max_omega: float, max_accel: float
) -> Trajectory:
    """Get the theoretical time it takes to follow a path."""

    forward_path = list(copy.deepcopy(path))
    forward_segments = _one_way_accel_cap(
        forward_path, max_velocity, max_omega, lambda v: max_accel -
        (v / max_velocity) * max_accel)

    reverse_path = list(reversed(copy.deepcopy(path)))
    reverse_segments = list(
        reversed(
            _one_way_accel_cap(
                reverse_path, max_velocity, max_omega, lambda v: max_accel +
                (v / max_velocity) * max_accel)))

    merged_traj = [(path[0], 0.0)]
    total_t = 0.0
    prev_v = 0.0
    for i in range(1, len(path)):
        f = forward_segments[i]
        r = reverse_segments[i]
        better_segment = f if f[1] <= r[1] else r

        if better_segment[1] == 0:
            total_t += distance(path[i], path[i - 1]) / prev_v
        else:
            total_t += distance(path[i], path[i - 1]) / better_segment[1]

        prev_v = better_segment[1]
        merged_traj.append((better_segment[0], total_t))

    return merged_traj


def _one_way_accel_cap(
    path: Path,
    max_velocity: float, max_omega: float,
    f: Callable[[float], float]
) -> List[Tuple[Waypoint, float]]:

    velocities = [0, max_velocity]
    for i in range(2, len(path)):
        p1 = path[i - 2]
        p2 = path[i - 1]
        p3 = path[i]

        dx = distance(p2, p3)
        dtheta = -(coterminal_minus((p2 - p1).bearing(), (p3 - p2).bearing()))
        dt = abs(dtheta / max_omega) + dx / max_velocity

        velocities.append(dx / dt)

    for i in range(1, len(path)):
        dx = distance(path[i], path[i - 1])
        min_velocity = 0.0
        if i != len(path) - 1:
            min_velocity = min(velocities[i], velocities[i + 1])
        dt = dx / (velocities[i - 1] + (min_velocity - velocities[i - 1]) / 2)

        velocities[i] = dx / dt
        max_accel = f(velocities[i - 1])
        if (velocities[i] - velocities[i - 1]) / dt > max_accel:
            if max_accel == 0:
                dt = dx / velocities[i - 1]
            else:
                dt = (-velocities[i - 1] +
                      math.sqrt(velocities[i - 1]**2 +
                                2 * max_accel * dx)) / max_accel

            velocities[i] = velocities[i - 1] + max_accel * dt

    return list(zip(path, velocities))
