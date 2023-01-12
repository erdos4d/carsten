from sympy import *


class LLL:
    delta = 3 / 4
    n = 0
    k = 1
    v = []
    v_star = []
    mu = None

    def __init__(self, v: list[Matrix], delta=3 / 4):
        self.delta = delta
        self.v.extend(v)
        self.n = len(v)
        self.set_state()

    def set_state(self):
        self.v_star.clear()
        self.v_star.extend(GramSchmidt(self.v, False))
        self.mu = Matrix([[
            self.v[i].dot(self.v_star[j]) / self.norm_square(self.v_star[j]) for j in range(self.n)
        ] for i in range(self.n)])

    def norm_square(self, x: Matrix):
        return x.dot(x).doit()

    def closest_integer(self, x: int):
        return floor(x + 1 / 2).doit()

    def mu_square(self, i, j):
        return pow(self.mu[i, j], 2)

    def lovasz_condition(self, k):
        assert 0 < k < self.n
        return self.norm_square(self.v_star[k]) >= \
            (self.delta - self.mu_square(k, k - 1)) * self.norm_square(self.v_star[k - 1])

    def mu_small(self, k, j):
        return abs(self.mu[k, j]) < 1 / 2

    def swap(self, k):
        self.v[k], self.v[k - 1] = self.v[k - 1], self.v[k]

    def scale(self, k, j):
        self.v[k] -= self.closest_integer(self.mu[k, j]) * self.v[j]

    def reduce(self):
        while self.k < self.n:
            if abs(self.mu[self.k, self.k - 1]) > 1 / 2:
                self.scale(self.k, self.k - 1)
                self.set_state()
            if self.lovasz_condition(self.k):
                while any([not self.mu_small(self.k, j) for j in range(self.k)]):
                    for l in range(self.k - 1, -1, -1):
                        if not self.mu_small(self.k, l):
                            self.scale(self.k, l)
                            self.set_state()
                            break
                assert all([self.mu_small(self.k, j) for j in range(self.k)])
                self.k += 1
            else:
                self.swap(self.k)
                self.set_state()
                self.k = max(self.k - 1, 1)
        assert all([self.lovasz_condition(k) for k in range(1, self.n)])
        assert all([self.mu_small(k, j) for k in range(self.n) for j in range(k)])
        return self.v
