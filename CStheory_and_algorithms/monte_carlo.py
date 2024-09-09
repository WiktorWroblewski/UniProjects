import math
import random
import matplotlib.pyplot as plt
import numpy as np

def plot_mc(points, f, func_string):
    x_vals_green = [point[0] for point in points if point[2] == 'green']
    y_vals_green = [point[1] for point in points if point[2] == 'green']

    x_vals_red = [point[0] for point in points if point[2] == 'red']
    y_vals_red = [point[1] for point in points if point[2] == 'red']

    x_vals_grey = [point[0] for point in points if point[2] == 'grey']
    y_vals_grey = [point[1] for point in points if point[2] == 'grey']

    x_func = np.linspace(0, 1, 1000)
    y_func = [f(x) for x in x_func]

    plt.figure(figsize=(10, 6))

    plt.scatter(x_vals_green, y_vals_green, color='green', s=3, label='Under curve (green)')
    plt.scatter(x_vals_red, y_vals_red, color='red', s=3, label='Below curve (red)')
    plt.scatter(x_vals_grey, y_vals_grey, color='grey', s=3, label='Other (grey)')

    plt.plot(x_func, y_func, color='blue', linewidth=2, label=func_string)

    plt.title('Monte Carlo Simulation')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.grid(True)
    plt.show()

def f(x):
    return math.exp(-2 * x) - 0.5

def riemann_integral(n, f):
    area = 0
    for i in range(n):
        area += f(i * (1 / n)) * (1 / n)
    return area

def monte_carlo(n, f, maxv, minv):
    shoot = 0
    hit = 0
    points = []
    for i in range(n):
        rx = random.uniform(0, 1)
        ry = random.uniform(minv, maxv)
        fv = f(rx)
        if fv >= ry and ry >= 0:
            hit += 1
            points.append((rx, ry, 'green'))
        elif fv < ry and ry < 0:
            hit -= 1
            points.append((rx, ry, 'red'))
        else:
            points.append((rx, ry, 'grey'))
        shoot += 1
    area = (hit / shoot) * (maxv - minv)
    return area, points

n = 100000
print(riemann_integral(n, f))
area, points = monte_carlo(n, f, 0.5, -0.5)
print(area)
plot_mc(points, f, 'f(x) = exp(-2x) - 0.5')
