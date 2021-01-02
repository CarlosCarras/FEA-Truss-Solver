'''
This implementation of LU Factorization was inspired by Steven C. Chapra's
"Applied Numerical Methods with MATLAB for Engineers and Scientists" textbook.
'''

import numpy as np

class Solver:
    def __init__(self):
        self.LU = None


    def lu_fact(self, A):
        n = A.shape[0]
        piv = np.arange(0,n)

        for k in range(n-1):
            # pivotting
            max_row_index = np.argmax(abs(A[k:n,k])) + k
            piv[[k,max_row_index]] = piv[[max_row_index,k]]
            A[[k,max_row_index]] = A[[max_row_index,k]]

            # LU factorization
            for i in range(k+1, n):
                A[i,k] = A[i,k] / A[k,k]
                for j in range(k+1, n):
                    A[i,j] -= A[i,k] * A[k,j]
        return A


    def forward_sub(self, L, b):
        n = L.shape[0]
        for i in range(n):
            for j in range(i):
                b[i] -= L[i,j]*b[j]
        return b


    def back_sub(self, U, y):
        n = U.shape[0]
        m = U.shape[1]
        for i in range(n-1, -1, -1):
            for j in range(i+1, m):
                y[i] -= U[i,j] * y[j]
            y[i] = y[i] / U[i,i]
        return y


    def set_lu_decomp(self, k):
        self.LU = self.lu_fact(k)


    def solve_all(self, k, f):
        self.set_lu_decomp(k)
        y = self.forward_sub(self.LU, f)
        x = self.back_sub(self.LU, y)
        return x


    def solve_force(self, f):
        y = self.forward_sub(self.LU, f)
        x = self.back_sub(self.LU, y)
        return x