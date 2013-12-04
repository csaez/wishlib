import math


def add(u, v):
    return [u[i] + v[i] for i in range(len(u))]


def sub(u, v):
    return [u[i] - v[i] for i in range(len(u))]


def magnitude(v):
    return math.sqrt(sum(v[i] * v[i] for i in range(len(v))))


def normalize(v):
    vmag = magnitude(v)
    return [v[i] / vmag for i in range(len(v))]


def negate(v):
    return [v[i] * -1 for i in range(len(v))]


def dot(u, v):
    return sum(u[i] * v[i] for i in range(len(u)))


def cross(u, v):
    return [u[1] * v[2] - u[2] * v[1],
            u[2] * v[0] - u[0] * v[2],
            u[0] * v[1] - u[1] * v[0]]


def determinant(a):
    return (a[0][0] * (a[1][1] * a[2][2] - a[2][1] * a[1][2])
            - a[1][0] * (a[0][1] * a[2][2] - a[2][1] * a[0][2])
            + a[2][0] * (a[0][1] * a[1][2] - a[1][1] * a[0][2]))
