import decimal
import math
import zlib
from datetime import datetime as dt

import numpy as np
from flint import fmpz_mat
from sympy import Pow, floor, primepi, prime, symbols, integrate, Rational, ceiling, product, factorial, binomial, \
    Matrix, log


def to_blob(x):
    return zlib.compress(str.encode(str(x).replace(' ', '')), level=9)


def to_string(x):
    return str(x).replace(' ', '')


def run(n: int):
    start_time = dt.now().timestamp()
    output = {}
    output.update({'n': n})

    beta = (1 - Pow(10, -4)) / 100
    output.update({'beta': to_string(beta)})

    q = 45 / 32
    output.update({'q': to_string(q)})

    Q = floor(pow(n, beta)).doit()
    output.update({'Q': to_string(Q)})

    Tau = (1 + Q) / 3
    output.update({'Tau': to_string(Tau)})

    m = [primepi(n / Tau).doit(), primepi(3 * n).doit()]
    output.update({'m': to_string(m)})

    W0 = set(k * prime(j) for j in range(m[0] + 1, m[1] + 1) for k in range(1, Q + 1))
    output.update({'W0': to_blob(W0)})

    W1 = set(j for j in range(ceiling(q * n).doit(), 3 * n + 1)).difference(W0)
    output.update({'W1': to_blob(W1)})

    A = list(W1)
    output.update({'A': to_blob(A)})

    N = len(A)
    output.update({'N': to_string(N)})

    u, h = symbols('n h')

    t_cache = {}

    def t(_n: int):
        val = t_cache.get(_n)
        if val is None:
            val = (integrate(u * product(h - u, (h, 1, _n - 2)).doit(), (u, 0, 1)).doit() / factorial(
                _n - 1).doit()).doit()
            t_cache.update({_n: val})
        return val

    binom_cache = {}

    def binom(a, b):
        val = binom_cache.get((a, b))
        if val is None:
            val = binomial(a, b)
            binom_cache.update({(a, b): val})
        return val

    time = dt.now().timestamp()
    B = [t(z + 2) for z in range(n + 1)]
    output.update({'B': to_blob(B)})
    output.update({'B_seconds': int(dt.now().timestamp() - time)})

    C = [
        sum([t(l + 2) / (A[b] * binom(A[b] + l, l)) for l in range(n + 1)]) +
        sum([Rational(1, l) for l in range(1, A[b])])
        for b in range(N)
    ]
    output.update({'C': to_blob(C)})

    E = [c.q for c in C]
    output.update({'E': to_blob(E)})

    V = np.lcm.reduce(E)
    output.update({'V': to_string(V)})

    L = [-V]
    L.extend([V * c for c in C])
    output.update({'L': to_blob(L)})

    F = [
        [1 if i == j else 0 if i < N + 1 else int(L[j]) for i in range(N + 2)] for j in range(N + 1)
    ]

    time = dt.now().timestamp()
    fM = fmpz_mat(F)
    lll = fM.lll().tolist()
    G_list = [[int(lll[i][j]) for j in range(N + 2)] for i in range(N + 1)]
    G = Matrix(G_list)
    output.update({'G': to_blob(G_list)})
    output.update({'lll_seconds': int(dt.now().timestamp() - time)})

    Z = [int(l) for l in L]
    Z.append(-1)

    basis_check = all([np.sum([G[u, j] * Z[j] for j in range(G.shape[1])]) == 0 for u in range(G.shape[0])])
    output.update({'basis_check': basis_check})

    rank_check = fM.rank() == N + 1
    output.update({'rank_check': bool(rank_check)})

    S = [max([abs(G[j, i]) for i in range(G.shape[1])]) for j in range(G.shape[0])]
    S.sort()
    output.update({'S': to_blob(S)})

    T = [(log(S[k + 1]) / log(S[k])).doit().evalf() for k in range(N)]
    output.update({'T': to_blob(T)})

    psi = 1 / max(T)
    output.update({'psi': to_string(psi)})

    D = [
        math.prod([
            max(abs(max(G[j, :])), abs(min(G[j, :]))) for j in range(G.shape[0])
        ]),
        math.floor(decimal.Decimal(sum([pow(z, 2) for z in Z])).sqrt())
    ]
    output.update({'D': to_string(D)})

    t1 = math.log(int(D[0])) / math.log(int(D[1]))
    output.update({'t1': to_string(t1)})

    t2 = N * (1 - psi) / (1 - pow(psi, N + 1))
    output.update({'t2': to_string(t2)})

    beta3 = max(t1, t2)
    output.update({'beta3': to_string(beta3)})

    output.update({'total_seconds': int(dt.now().timestamp() - start_time)})

    return output


#
# G = Matrix([
#     [-18, 56, -90, 25, 4, -7, 12, -6, -11],
#     [-39, 70, -6, -67, -39, 29, 12, -6, -126],
#     [-101, -8, 9, 4, -59, 25, -9, 6, 11],
#     [-55, 55, 3, -85, 2, -21, 37, -5, -13],
#     [69, 28, 42, 3, -39, 28, -18, -13, -20],
#     [-2, -33, -9, -37, -10, -10, 67, 20, -17],
#     [-16, -32, 32, -9, 24, 10, 11, -40, 80],
#     [-48, -7, 12, 74, 4, -33, 0, -56, -26]
# ])
