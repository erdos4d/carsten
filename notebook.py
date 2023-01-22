from datetime import datetime as dt

import numpy as np
from sympy import *

from lll_maple import LLL


def run(n: int):
    start_time = dt.now().timestamp()
    output = {}
    output.update({'n': n})

    beta = (1 - Pow(10, -4)) / 100
    output.update({'beta': str(beta)})

    q = 45 / 32
    output.update({'q': str(q)})

    Q = floor(pow(n, beta)).doit()
    output.update({'Q': str(Q)})

    Tau = (1 + Q) / 3
    output.update({'Tau': str(Tau)})

    m = [primepi(n / Tau).doit(), primepi(3 * n).doit()]
    output.update({'m': str(m)})

    W0 = set(k * prime(j) for j in range(m[0] + 1, m[1] + 1) for k in range(1, Q + 1))
    output.update({'W0': str(W0)})

    W1 = set(j for j in range(ceiling(q * n).doit(), 3 * n + 1)).difference(W0)
    output.update({'W1': str(W1)})

    A = list(W1)
    output.update({'A': str(A)})

    N = len(A)
    output.update({'N': str(N)})

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
    output.update({'B': str(B)})
    output.update({'B_seconds': int(dt.now().timestamp() - time)})

    C = [
        sum([t(l + 2) / (A[b] * binom(A[b] + l, l)) for l in range(n + 1)]) +
        sum([Rational(1, l) for l in range(1, A[b])])
        for b in range(N)
    ]
    output.update({'C': str(C)})

    E = [c.q for c in C]
    output.update({'E': str(E)})

    V = np.lcm.reduce(E)
    output.update({'V': str(V)})

    L = [-V]
    L.extend([V * c for c in C])
    output.update({'L': str(L)})

    F = [
        [1 if i == j else 0 if i < N + 1 else L[j] for i in range(N + 2)] for j in range(N + 1)
    ]
    output.update({'F': str(F)})

    time = dt.now().timestamp()
    lll = LLL(Matrix(F), delta=Rational(3, 4))
    G = lll.basis
    G_list = [[int(G[u, j]) for j in range(G.shape[1])] for u in range(G.shape[0])]
    output.update({'G': str(G_list)})
    output.update({'lll_seconds': int(dt.now().timestamp() - time)})

    Z = L
    Z.append(-1)

    basis_check = all([np.sum([G[u, j] * Z[j] for j in range(G.shape[1])]) == 0 for u in range(G.shape[0])])
    output.update({'basis_check': basis_check})

    rank_check = np.linalg.matrix_rank(G_list) == N + 1
    output.update({'rank_check': bool(rank_check)})

    S = [max([abs(G[j, i]) for i in range(G.shape[1])]) for j in range(G.shape[0])]
    S.sort()
    output.update({'S': str(S)})

    T = [(log(S[k + 1]) / log(S[k])).doit().evalf() for k in range(N)]
    output.update({'T': str(T)})

    psi = 1 / max(T)
    output.update({'psi': str(psi)})

    H = L
    H.append(-1)

    D = [
        prod([
            max(abs(max(G[j, :])), abs(min(G[j, :]))) for j in range(G.shape[0])
        ]),
        floor(sqrt(abs(sum(pow(h, 2) for h in H))))
    ]
    output.update({'D': str(D)})

    t1 = (log(D[0]) / log(D[1])).evalf()

    output.update({'t1': str(t1)})

    t2 = N * (1 - psi) / (1 - pow(psi, N + 1))
    output.update({'t2': str(t2)})

    beta3 = max(t1, t2)
    output.update({'beta3': str(beta3)})

    output.update({'total_seconds': int(dt.now().timestamp() - start_time)})

    return output
