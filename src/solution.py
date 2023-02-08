import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad


def E(x):
    if 0 <= x <= 1:
        return 3
    elif 1 < x <= 2:
        return 5
    return 0


class Solution:
    def __init__(self, n):
        self.n = n
        self.h = 2 / n

    def __xi(self, i):
        return self.h * i

    def __base_func(self, i, x):
        if self.__xi(i - 1) <= x <= self.__xi(i):
            return (x - self.__xi(i - 1)) / self.h
        elif self.__xi(i) < x <= self.__xi(i + 1):
            return (self.__xi(i + 1) - x) / self.h
        return 0

    def __derivative(self, i, x):
        if self.__xi(i - 1) <= x <= self.__xi(i):
            return 1/self.h
        elif self.__xi(i) < x <= self.__xi(i + 1):
            return -1/self.h
        return 0

    def __compute_b(self, i, j):
        integrate_from = max(0, self.h * (max(i, j) - 1))
        integrate_to = min(2, self.h * (min(i, j) + 1))

        return quad(
            lambda x: E(x) * self.__derivative(i, x) * self.__derivative(j, x),
            integrate_from,
            integrate_to)[0] - 3 * self.__base_func(i, 0) * self.__base_func(j, 0)

    def __compute_l(self, i):
        return -30 * self.__base_func(i, 0)

    def solve(self):
        matrix_b = np.zeros((self.n + 1, self.n + 1))
        vector_l = np.zeros(self.n + 1)
        # Dirichlet u(2) = 0
        matrix_b[self.n][self.n] = 1
        for i in range(self.n):
            # main diagonal
            matrix_b[i][i] = self.__compute_b(i, i)
            # lower diagonal
            if i + 1 <= self.n:
                matrix_b[i][i + 1] = self.__compute_b(i, i + 1)
            # upper diagonal
            if i - 1 >= 0:
                matrix_b[i][i - 1] = self.__compute_b(i, i - 1)
            vector_l[i] = self.__compute_l(i)

        result = np.linalg.solve(matrix_b, vector_l)
        x = np.arange(0, 2 + self.h, self.h)
        y = np.zeros(self.n + 1)
        for i in range(self.n + 1):
            for j in range(self.n + 1):
                y[i] += result[j] * self.__base_func(j, x[i])

        plt.plot(x, y)
        plt.show()
