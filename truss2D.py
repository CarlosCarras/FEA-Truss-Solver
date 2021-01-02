
from __future__ import division
import numpy as np


def check_param(param, integer=False):
    try:
        if integer:
            val = int(param)
        else:
            val = float(param)
    except:
        val = 0
    return val

def closetozeroroundoff(val, tol=1e-7):
    rounded = round(val)
    if abs(val - rounded) < tol:
        return rounded
    else:
        return val


class TrussElement:
    def __init__(self, LN, L, A, E, PHI):
        self.LN1 = check_param(LN[0], integer=True)
        self.LN2 = check_param(LN[1], integer=True)
        self.L = check_param(L)
        self.E = check_param(E)
        self.A = check_param(A)
        self.PHI = check_param(PHI)

        #out_str = "Created Node: LN1: {0:d}, LN2:, {1:d}, L: {2:d}, E: {3:d}, A: {4:d}, PHI: {5:d}"
        #print(out_str.format(self.LN1, self.LN2, self.L, self.E, self.A, self.PHI))

    def compose_stiffness(self):
        l = closetozeroroundoff(np.cos(np.deg2rad(self.PHI)))
        m = closetozeroroundoff(np.sin(np.deg2rad(self.PHI)))
        ke = self.E * self.A / self.L * np.array([[   l ** 2,     l * m,  -l ** 2,    -l * m],
                                                  [    l * m,    m ** 2,   -l * m, -(m ** 2)],
                                                  [-(l ** 2),    -l * m,   l ** 2,     l * m],
                                                  [   -l * m, -(m ** 2),    l * m,    m ** 2]])

        return ke


class TrussNode:
    def __init__(self, n, FX=0, FY=0, M=0, B='F', X=0, Y=0):
        self.n = check_param(n, integer=True)
        self.FX = check_param(FX)
        self.FY = check_param(FY)
        self.M = check_param(M)
        self.B = B
        self.X = check_param(X)
        self.Y = check_param(Y)