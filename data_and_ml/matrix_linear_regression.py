import numpy as np
import matplotlib.pyplot as plt

"""Implementation of linear regression that can solve any n-degree polynomial, such as:
y(x) = sum(a_i * x^i) where i = 0, 1,..., n

This equation can be written in matrix form as:
Y = XA

And it can be solved using the following equation:
A = (X^T * X)^(-1) * X^T * Y

This formula ensures that the given data will lead to a solution, even if the matrix is not square
"""


def linreg(x, y, n=1):
    if n == 1:
        x = np.column_stack([x, np.ones((x.shape[0], 1))])
        coeff = np.transpose(np.linalg.inv((np.transpose(x) @ x)) @ np.transpose(x) @ y)
        return coeff[0]

    temp = x.copy()
    for i in range(2, n + 1):
        x = np.column_stack([temp ** i, x])
    x = np.column_stack([x, np.ones((x.shape[0], 1))])
    coeff = np.transpose(np.linalg.inv((np.transpose(x) @ x)) @ np.transpose(x) @ y)
    return coeff[0]


# Example:

x = np.random.uniform(-5, 5, size=200)
y = 0.5 * (x ** 3) + 3 * (x ** 2) - 2 * x - 10 + np.random.normal(scale=2, size=200)

x = x.reshape(-1, 1)
y = y.reshape(-1, 1)

a, b, c, d, e = linreg(x, y, 4)
print(f'\npredicted a = {a}\npredicted b = {b}\npredicted c = {c}\npredicted d = {d}\npredicted e = {e}')

x_temp = np.linspace(-5,5,200)
y_temp = a * (x_temp ** 4) + b * (x_temp ** 3) + c * (x_temp ** 2) + d * x_temp + e
plt.scatter(x, y)
plt.plot(x_temp, y_temp, color='r')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.show()


a, b, c, d = linreg(x, y, 3)
print(f'\npredicted a = {a}\npredicted b = {b}\npredicted c = {c}\npredicted d = {d}')

y_temp = a * (x_temp ** 3) + b * (x_temp ** 2) + c * x_temp + d
plt.scatter(x, y)
plt.plot(x_temp, y_temp, color='r')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.show()


a, b, c = linreg(x, y, 2)
print(f'\npredicted a = {a}\npredicted b = {b}\npredicted c = {c}')

y_temp = a * (x_temp ** 2) + b * x_temp + c
plt.scatter(x, y)
plt.plot(x_temp, y_temp, color='r')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.show()

a, b = linreg(x, y)
print(f'\npredicted a = {a}\npredicted b = {b}')

y_temp = a * x_temp + b
plt.scatter(x, y)
plt.plot(x_temp, y_temp, color='r')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.show()
