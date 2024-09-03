import numpy as np
import matplotlib.pyplot as plt

"""Implementation of natural cubic spline using matrix formula and thomas algorithm
This implementation is based on the scientific work of Joseph M. Mahaffy,
Department of Mathematics and Statistics, San Diego State University

Cubic spline formula:
S_i(x) = a_i + b_i (x-x_i) + c_i (x-x_i)^2 + d_i (x-x_i)^3, where:
- S_i(x_i) = y_i
- S_i(x_(i+1)) = y_(i+1)
- S_i'(x_(i+1)) = S_(i+1)'(x_(i+1))
- S_i''(x_(i+1)) = S_(i+1)''(x_(i+1))
- S_0''(x_0) = 0
- S_(n-2)''(x_(n-1)) = 0

Additional variables:
h_i = x_(i+1) - x_i, i = 0,1..., n-2
m_i = (y_(i+1)-y_i)/h_i, i= 0,1..., n-1

The coefficients are found by solving the system of linear equations Ac = B, where:
A = [[1, 0, 0, 0, ... 0]
    [h_0, 2(h_0 + h_1), h1, 0 ... 0]
    [0,  h_1, 2(h_1 + h_2), h_2, ... 0]
    [..., ..., ..., ...]
    [0, 0, 0, 0, ..., 1]]

c = [c_0, c_1, c_2, ..., c_(n-1)]^T
    
B = [0, 3(m_1-m_0)/h_0, 3(m_2-m_1)/h_1, ..., 0]^T

After obtaining the coefficients c_i, the values of a_i, b_i, and d_i are calculated:
a_i = y_i

b_i = m_i - h_i(2c_i+c_(i+1))/3

d_i = (c_(i+1)-c_i)/(3h_i)
"""


def natural_spline(points):
    n = len(points)
    x = np.array([p[0] for p in points])
    y = np.array([p[1] for p in points])

    h = np.diff(x)
    A = np.zeros((n, n))
    B = np.zeros(n)

    A[0, 0] = 1
    A[-1, -1] = 1

    for i in range(1, n - 1):
        A[i, i - 1] = h[i - 1]
        A[i, i] = 2 * (h[i - 1] + h[i])
        A[i, i + 1] = h[i]
        B[i] = 3 * ((y[i + 1] - y[i]) / h[i] - (y[i] - y[i - 1]) / h[i - 1])

    c = np.linalg.solve(A, B)

    a = y[:-1]
    b = np.zeros(n - 1)
    d = np.zeros(n - 1)

    for i in range(n - 1):
        b[i] = (y[i + 1] - y[i]) / h[i] - h[i] * (2 * c[i] + c[i + 1]) / 3
        d[i] = (c[i + 1] - c[i]) / (3 * h[i])
    return list(zip(a, b, c[:-1], d))


# Example:

points = [[-1, -5], [0, 0], [4, 2], [5, -1], [5.5, -1.5], [10, -1.5], [11, 0], [11.5, 10]]
coefficients = natural_spline(points)

x_vals = np.array([p[0] for p in points])
y_vals = np.array([p[1] for p in points])
x_new = np.linspace(x_vals.min(), x_vals.max(), 1000)
y_new = np.zeros_like(x_new)

for i in range(len(coefficients)):
    xi = x_vals[i]
    a, b, c, d = coefficients[i]
    temp = (x_new >= xi) & (x_new <= x_vals[i + 1])
    y_new[temp] = a + b * (x_new[temp] - xi) + c * (x_new[temp] - xi) ** 2 + d * (x_new[temp] - xi) ** 3


plt.scatter(x_vals, y_vals, color='red', label='Original Points')
plt.plot(x_new, y_new, label='Natural Cubic Spline')
plt.title('Natural Cubic Spline Interpolation')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.grid(True)
plt.show()
