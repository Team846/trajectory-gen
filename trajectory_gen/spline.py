import numpy as np
from scipy import interpolate
from . import Waypoint, Path


def generate(points, spaceApart=3):
    # gap = 10
    input = []
    output = []
    for i in range(len(points)):
        input.append(points[i].x)
        output.append(points[i].y)

    '''input = [0, 4, 8, 13, 10, 6.5, 15, 18, 15, 12, 15, 20]
    output = [4, 4, 6, 4, 0, 3, 10, 16, 24, 20, 18, 25]'''

    N = len(input)
    n = N - 1

    time = [None] * len(input)
    for i in range(0, len(time)):
        time[i] = i

    ax, bx, cx, dx = getSpline(time, input, n, N)

    ay, by, cy, dy = getSpline(time, output, n, N)

    num_to_divide = int(np.sqrt((input[1] - input[0]) ** 2 + (output[1] - output[0]) ** 2) / spaceApart)

    # t_2 = np.linspace(0, 1, num_to_divide)
    t_2 = np.linspace(0, 1, 1000)
    t_vals = []
    x_vals = []
    y_vals = []

    x_prev = 0
    y_prev = 0
    x_net = 0
    y_net = 0

    for i in range(0, n):

        '''if i > 0:
          num_to_divide = int(np.sqrt((input[i] - input[i-1])**2 + (output[i] - output[i-1])**2) / spaceApart)
          t_2 = np.linspace(0, 1, num_to_divide)
          #print(t_2)'''

        for j in range(len(t_2) - 1):
            # print("here")
            t = t_2[j]
            x = ax[i] + bx[i] * t + cx[i] * t ** 2 + dx[i] * t ** 3
            y = ay[i] + by[i] * t + cy[i] * t ** 2 + dy[i] * t ** 3

            x_net += x - x_prev
            y_net += y - y_prev
            if (x_net ** 2 + y_net ** 2) > spaceApart ** 2:
                # print(x_net ** 2 + y_net ** 2)
                x_vals.append(x)
                y_vals.append(y)
                x_net = 0
                y_net = 0
                # print((str)(x) + ", " + (str)(y))

            x_prev = x
            y_prev = y

            t_vals.append(t + time[i])

        if i == n - 1:
            t = t_2[-1]
            x = ax[i] + bx[i] * t + cx[i] * t ** 2 + dx[i] * t ** 3
            x_vals.append(x)

            y = ay[i] + by[i] * t + cy[i] * t ** 2 + dy[i] * t ** 3
            y_vals.append(y)
            # print(str(x) + ", " + str(y))

    waypoints = []
    for i in range(len(x_vals)):
        waypoints.append(Waypoint(x_vals[i], y_vals[i]))
        pass
    plt.plot(x_vals, y_vals)
    for i in range(len(x_vals)):
        # print(str(x_vals[i]) + ", " + str(y_vals[i]))
        pass
    return waypoints


def getSpline(time, values, n, N):
    # a constant of polynomial
    a = [None] * N
    for i in range(0, len(time)):
        a[i] = (values[i])

    # print(len(a) == len(time))

    # b and d constants
    b = [None] * (n)
    d = [None] * (n)

    h = [None] * (n)
    for i in range(0, n):  # [0, n-1]
        h[i] = time[i + 1] - time[i]

    alpha = [None] * (n)
    for i in range(1, n):  # [0, n-1]
        alpha[i] = (3 / h[i]) * (a[i + 1] - a[i]) - (3 / h[i - 1]) * (a[i] - a[i - 1])

    c = [None] * N
    l = [None] * N
    u = [None] * N
    z = [None] * N

    l[0] = 1
    u[0] = 0
    z[0] = 0

    for i in range(1, n):
        l[i] = 2 * (time[i + 1] - time[i - 1]) - h[i - 1] * u[i - 1]
        u[i] = h[i] / l[i]
        z[i] = (alpha[i] - h[i - 1] * z[i - 1]) / l[i]

    l[n] = 1
    z[n] = 0
    c[n] = 0

    for j in range(n - 1, -1, -1):
        c[j] = z[j] - u[j] * c[j + 1]
        b[j] = (a[j + 1] - a[j]) / h[j] - (h[j] * (c[j + 1] + 2 * c[j])) / 3
        d[j] = (c[j + 1] - c[j]) / (3 * h[j])

    '''print(a)
    print(b)
    print(c)
    print(d)'''

    return a, b, c, d
