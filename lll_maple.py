from sympy.core import Rational
from sympy.functions.elementary.integers import floor
from sympy.matrices.dense import Matrix, zeros


class LLL:

    def __init__(self, v: Matrix, delta=Rational(3, 4)):
        assert Rational(1, 4) <= delta <= Rational(1, 1)
        assert v.shape[0] <= v.shape[1]
        self._m = v.shape[0]
        self._n = v.shape[1]
        self._k = 1
        self._delta = delta
        self._Y = v.copy()
        self._Y_star = zeros(self._m, self._n)
        self._mu = zeros(self._m, self._m)
        self._g_star = [Rational(0, 1) for _ in range(self._m)]
        self._set_initial_state()
        self._reduce()

    @property
    def basis(self) -> Matrix:
        return self._Y

    def _set_initial_state(self) -> None:
        for i in range(self._m):
            self._Y_star[i, :] = self._Y[i, :]
            for j in range(i):
                self._mu[i, j] = self._Y[i, :].dot(self._Y_star[j, :]) / self._g_star[j]
                self._Y_star[i, :] -= self._mu[i, j] * self._Y_star[j, :]
            self._g_star[i] = self._Y_star[i, :].dot(self._Y_star[i, :])

    @staticmethod
    def _closest_integer(x: Rational) -> Rational:
        return floor(x + Rational(1, 2)).doit()

    def _mu_square(self, i: int, j: int) -> int:
        return pow(self._mu[i, j], 2)

    def _lovasz_condition(self, k: int) -> bool:
        return self._g_star[k] >= (self._delta - self._mu_square(k, k - 1)) * self._g_star[k - 1]

    def _mu_small(self, k: int, j: int) -> bool:
        return abs(self._mu[k, j]) <= Rational(1, 2)

    def _reduce(self) -> None:
        while self._k < self._m:
            if not self._mu_small(self._k, self._k - 1):
                r = self._closest_integer(self._mu[self._k, self._k - 1])
                self._Y[self._k, :] -= r * self._Y[self._k - 1, :]
                for j in range(self._k - 1):
                    self._mu[self._k, j] -= r * self._mu[self._k - 1, j]
                self._mu[self._k, self._k - 1] -= r
            if self._lovasz_condition(self._k):
                for l in range(self._k - 2, -1, -1):
                    if not self._mu_small(self._k, l):
                        r = self._closest_integer(self._mu[self._k, l])
                        self._Y[self._k, :] -= r * self._Y[l, :]
                        for j in range(l):
                            self._mu[self._k, j] -= r * self._mu[l, j]
                        self._mu[self._k, l] -= r
                assert all([self._mu_small(self._k, j) for j in range(self._k)])
                self._k += 1
            else:
                nu = self._mu[self._k, self._k - 1]
                alpha = self._g_star[self._k] + pow(nu, 2) * self._g_star[self._k - 1]
                self._mu[self._k, self._k - 1] *= self._g_star[self._k - 1] / alpha
                self._g_star[self._k] *= self._g_star[self._k - 1] / alpha
                self._g_star[self._k - 1] = alpha
                self._Y[self._k, :], self._Y[self._k - 1, :] = self._Y[self._k - 1, :], self._Y[self._k, :]
                for j in range(self._k - 1):
                    self._mu[self._k - 1, j], self._mu[self._k, j] = self._mu[self._k, j], self._mu[self._k - 1, j]
                for i in range(self._k + 1, self._m):
                    xi = self._mu[i, self._k]
                    self._mu[i, self._k] = self._mu[i, self._k - 1] - nu * self._mu[i, self._k]
                    self._mu[i, self._k - 1] = self._mu[self._k, self._k - 1] * self._mu[i, self._k] + xi
                self._k = max(self._k - 1, 1)
        assert all([self._lovasz_condition(k) for k in range(1, self._m)])
        assert all([self._mu_small(k, j) for k in range(self._m) for j in range(k)])
