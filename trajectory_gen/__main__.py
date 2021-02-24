import math
import time
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection
from .search import find_optimal_trajectory
from . import Line, Waypoint

MAX_V = 15.86 * 12  # 15.86 ft/s
MAX_OMEGA = MAX_V / (2.13 * 12) / 2 / math.pi * 180 # 2.13 ft track length
MAX_A = 14 * 12  # 14 ft/s^2


def main():
    # Setup plot
    f, ax = plt.subplots(1, 1)

    # Plot slalom markers
    markers = [
        # x y
        [60, 30],
        [60, 60],
        [60, 120],
        [60, 150],
        [60, 180],
        [60, 210],
        [60, 240],
        [60, 300],
    ]
    ax.scatter([p[0] for p in markers], [p[1] for p in markers], label="markers", s=20)

    # Input lines
    m = 16 # robot margin
    m_diag = m * math.sqrt(2) / 2 # m when at a diagonal
    d2 = 10 # D2 extra margin
    d8 = 10 # D8 extra margin
    d10 = 10 # D10 extra margin
    lines = list(map(lambda i: Line(Waypoint(i[0], i[1]), Waypoint(i[2], i[3])), [
        # x1 y1 x2 y2
        [60 - m - d2, 50, 0 + m, 50],
        [60 + m_diag, 120 - m_diag, 120 - m_diag, 60 + m_diag],
        [60 + m, 180, 120 - m, 180],
        [60, 240 + m + d8, 60, 300 - m],
        [60 - m - d10, 300, 0 + m, 300],
        [60, 300 + m, 60, 360 - m],
        [60 + m + d10, 300, 120 - m, 300],
        [60, 240 + m + d8, 60, 300 - m],
        [60 - m, 180, 0 + m, 180],
        [60 - m_diag, 120 - m_diag, 0 + m_diag, 60 + m_diag],
        [60 + m + d2, 60, 120 - m, 60],
    ]))

    # Plot input lines
    lines_x = []
    lines_y = []
    for line in lines:
        lines_x.append([line.p1.x, line.p2.x])
        lines_y.append([line.p1.y, line.p2.y])
    ax.add_collection(LineCollection([list(zip(x, y))
                                      for x, y in zip(lines_x, lines_y)], label="input lines"))

    # Get optimal
    start_t = time.time()
    trajectory = find_optimal_trajectory(lines, 5, MAX_V, MAX_OMEGA, MAX_A)[0]
    end_t = time.time()
    print(f"Calculation time: {end_t - start_t} s")

    # Plot optimal
    path_x = np.array([p[0].x for p in trajectory])
    path_y = np.array([p[0].y for p in trajectory])
    ax.scatter(path_x, path_y, label="optimal", s=12)

    # Write optimal traj to file
    with open("gen.csv", "w") as file:
        file.write("x,y,t\n")
        for i in trajectory:
            file.write(f"{str(i[0])},{i[1]}\n")
    print("Trajectory written to gen.csv")

    # Display plot
    ax.legend(loc="upper left")
    plt.gca().set_aspect("equal", adjustable="box")
    plt.gca().invert_xaxis()
    plt.show()


if __name__ == '__main__':
    main()
