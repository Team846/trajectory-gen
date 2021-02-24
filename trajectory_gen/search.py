from typing import Tuple, List
from matplotlib import pyplot as plt
from .spline import generate
from .trajectory import path_to_trajectory, trajectory_time
from . import Line, Trajectory


def find_optimal_trajectory(
    lines: List[Line], increment: float,
    max_velocity: float, max_omega: float, max_accel: float
) -> Tuple[Trajectory, float]:
    """Binary search to refine path points to find best trajectory given line ranges."""

    print("\n******New Cycle*****")
    best_time = float('inf')
    best_trajectory = []
    best_binary = ""

    runs = 2 ** len(lines)
    for i in range(runs):
        print(f"{i}/{runs} [{int(i/runs * 100)}%]", end='\r')

        path = []
        binary = format(i, f"0{len(lines)}b")
        for j, bit in enumerate(binary):
            path.append(lines[j].top_half_waypoint() if int(bit) else lines[j].bot_half_waypoint())

        spline = generate(path)
        trajectory = path_to_trajectory(spline, max_velocity, max_omega, max_accel)
        time = trajectory_time(trajectory)

        if time < best_time:
            best_time = time
            best_trajectory = trajectory
            best_binary = binary

    print(f"First line length: {lines[0].length()} in")
    print(f"Best: {best_time} sec [{best_binary}]")

    plt.scatter([p[0].x for p in best_trajectory], [p[0].y for p in best_trajectory],
                label=f"{lines[0].length()}", s=2)

    refined_lines = []
    for i, bit in enumerate(best_binary):
        refined_lines.append(lines[i].top_half_line() if int(bit) else lines[i].bot_half_line())

    if lines[0].length() < increment:
        return best_trajectory, best_time

    return find_optimal_trajectory(refined_lines, increment, max_velocity, max_omega, max_accel)
