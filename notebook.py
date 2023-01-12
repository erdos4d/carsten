import numpy as np
from sympy import *

from lll import LLL

n = 6
print('n:', n)

beta = (1 - Pow(10, -4)) / 100
print('beta:', beta)

q = 45 / 32
print(q)

Q = floor(pow(n, beta)).doit()
print('Q:', Q)

Tau = (1 + Q) / 3
print('Tau:', Tau)

m = [primepi(n / Tau).doit(), primepi(3 * n).doit()]
print('m:', m)

W0 = set(k * prime(j) for j in range(m[0] + 1, m[1] + 1) for k in range(1, Q + 1))
print('W0:', W0)

W1 = set(j for j in range(ceiling(q * n).doit(), 3 * n + 1)).difference(W0)
print('W1:', W1)

A = list(W1)
print('A:', A)

N = len(A)
print('N:', N)

u, h, z = symbols('n h z')


def t(_n: int):
    return (integrate(u * product(h - u, (h, 1, _n - 2)).doit(), (u, 0, 1)).doit() / factorial(_n - 1).doit()).doit()


B = [t(z + 2) for z in range(n + 1)]
print('B:', B)

C = [
    Sum(t(z + 2) / (A[b] * binomial(A[b] + z, z)), (z, 0, n)).doit() +
    Sum(1 / z, (z, 1, A[b] - 1)).doit()
    for b in range(N)
]
print('C:', C)

E = [c.q for c in C]
print('E:', E)

V = np.lcm.reduce(E)
print('V:', V)

L = [-V]
L.extend([V * c for c in C])
print('L:', L)

F = [
    [1 if i == j else 0 if i < N + 1 else L[j] for i in range(N + 2)] for j in range(N + 1)
]
print('F:', F)

lll = LLL([Matrix(f) for f in F], delta=0.75)
G = lll.reduce()
print('G:')
pprint(G)

Z = L
Z.append(-1)
print('Z:', Z)

print('check:', [np.sum([G[u][j] * Z[j] for j in range(len(Z))]) for u in range(len(G))])

