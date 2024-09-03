import numpy as np
from random import choice, random, randint, uniform, sample, choices
import matplotlib.pyplot as plt
import matplotlib.animation as animation


# Converts a binary representation of a chromosome to its decimal equivalent.
# The range of the function is (-8, 8). The chromosome is represented as:
# c = [c_0, c_1, ..., c_(r-1)]
# The decimal value is calculated as:
# (-1)^(c_0) * (c_1 * 2^2 + c_2 * 2^1 + ... + c_(r-2) * 2^(3-(r-2)) + c_(r-1) * 2^(3-(r-1)))
def binary_to_decimal(c):
    sum_val = 0
    j = 2
    for i in c.copy()[1:]:
        sum_val += i * (2 ** j)
        j -= 1
    return ((-1) ** c[0]) * sum_val


# Creates a population of n individuals (creatures), each with r chromosomes.
def create_population(n, r):
    p = []
    for _ in range(n):
        c = []
        for _ in range(r):
            c.append(choice([0, 1]))
        p.append(c)
    return p


# Evaluates the population p using the fitness function f.
def rate_population(p, f):
    rating = [f(binary_to_decimal(i)) for i in p.copy()]
    return rating


# Selects with replacement n individuals from population p based on their fitness ratings.
# Implements roulette wheel selection method.
def select(rating, p, n):
    weight = [(max(rating) + 1 - i) for i in rating.copy()]  # +1 ensures no zero probability
    w = [list(item) for item in zip(weight, p)]
    w.sort(key=lambda x: x[0], reverse=True)

    # Calculate cumulative weights for rws
    temp = 0
    for i in range(len(w)):
        temp += w[i][0]
        w[i][0] = temp

    popsum = w[-1][0]
    new_candidates = []

    # Selecting n new candidates using rws with binary search
    for _ in range(n):
        rand = uniform(0, popsum)
        low, high = 0, len(w) - 1
        while low < high:
            mid = (low + high) // 2
            if rand > w[mid][0]:
                low = mid + 1
            else:
                high = mid
        new_candidates.append(w[low][1])

    return new_candidates


# Implements crossover between selected individuals based on crossover probability - cp
def crossing(p, n, r, cp=0.5):
    indexes = [i for i in range(len(p))]
    new_population = p.copy()
    for i in range(n // 2):
        c1, c2 = sample(indexes, k=2)
        indexes.remove(c1)
        indexes.remove(c2)
        if random() <= cp:
            r1 = randint(2, r - 2)
            r2 = randint(r1, r)
            for i in range(r1, r2):
                new_population[c1][i], new_population[c2][i] = new_population[c2][i], new_population[c1][i]
    return new_population


# Implements mutation of the population based on mutation probability - mp
def mutate(p, mp=0.01):
    new_population = p.copy()
    for c in new_population:
        for i in range(len(c)):
            if random() <= mp:
                c[i] = 1 - c[i]
    return new_population


# Main evolutionary algorithm function
# n - number of individuals in the population
# r - number of chromosomes per individual
# f - fitness function
# e - stopping criterion, based on the difference between the best solutions in the last two generations
# cp - crossover probability
# mp - mutation probability
def evolutionary_algorithm(n, r, f, e=0.001, cp=0.5, mp=0.01):
    stop = False
    iter = 0

    p = create_population(n, r)  # Initial population
    iterbest = []  # List of best solutions over iterations, for visualization
    iterpopul = []  # List of populations over iterations, for visualization

    while not stop:
        iterpopul.append(p.copy())

        rating = rate_population(p, f)  # Evaluate population

        # Save the best solution of the current generation
        indbest = rating.index(min(rating))
        ratingbest = min(rating)
        iterbest.append((binary_to_decimal(p[indbest]), ratingbest))

        # Stopping condition
        if iter > 50:
            if abs(ratingbest - ratingbest_prev) <= e:
                stop = True
        if iter > 500:  # Max iteration safeguard
            stop = True

        if stop:  # Return the best solution found
            return p[indbest], iterbest, iterpopul

        p_prime = select(rating, p, n)  # Selection
        p_dprime = crossing(p_prime, n, r, cp)  # Crossover
        p_new = mutate(p_dprime, mp)  # Mutation
        ratingbest_prev = ratingbest

        iter += 1
        p = [i.copy() for i in p_new]


# Plots an animation of the best solutions over time
def plot_animation(iterbest, function, interval=100):
    fig, ax = plt.subplots()
    x_vals = np.linspace(-8, 8, 100000)
    y_vals = function(x_vals)

    best_points_x = []
    best_points_y = []

    def update(frame):
        ax.clear()
        ax.plot(x_vals, y_vals, label='Function')

        best_x, best_y = iterbest[frame]
        best_points_x.append(best_x)
        best_points_y.append(best_y)

        ax.scatter(best_points_x, best_points_y, color='gray', label='Previous best points')
        ax.scatter([best_x], [best_y], color='red', label='Current best point')

        for i in range(1, len(best_points_x)):
            ax.plot(best_points_x[i - 1:i + 1], best_points_y[i - 1:i + 1], color='gray', linestyle='--', linewidth=1)

        ax.set_title(f'Iteration {frame}, Best point: ({best_x:.2f}, {best_y:.2f})')
        ax.legend()
        ax.grid(True)

    ani = animation.FuncAnimation(fig, update, frames=len(iterbest), repeat=False, interval=interval)
    plt.show()


# Plots an animation showing the population distribution over time
def plot_animation2(iterpopul, function, interval=100):
    fig, ax = plt.subplots()
    x_vals = np.linspace(-8, 8, 100000)
    y_vals = function(x_vals)

    def update(frame):
        ax.clear()
        ax.plot(x_vals, y_vals, label='Function')

        for population in iterpopul[frame]:
            x_values = binary_to_decimal(population)
            y_values = function(x_values)
            ax.scatter(x_values, y_values, color='blue')

        ax.set_title(f'Population in iteration {frame}')
        ax.grid(True)

    ani = animation.FuncAnimation(fig, update, frames=len(iterpopul), repeat=False, interval=interval)
    plt.show()


# Example functions used as fitness functions in the evolutionary algorithm
def funcf(x):  # Rastrigin function
    A = 10
    n = 1
    return A * n + x ** 2 - A * np.cos(2 * np.pi * x)


def func1(x):
    return -20 + (x + 2) ** 2


def func2(x):
    return np.exp(-x / 4) + np.sin(8 * x)


def func3(x):
    return np.exp(np.abs(x) ** (1 / 99))


# Example usage:

for f in (funcf, func1, func2, func3):
    best, iterbest, iterpop = evolutionary_algorithm(60, 25, f)
    plot_animation(iterbest, f)
    plot_animation2(iterpop, f)
