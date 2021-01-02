
import math
import numpy as np


class Constructor:
    def __init__(self, elements, nodes):
        self.elements = elements
        self.nodes = nodes
        self.n = len(self.nodes)
        self.rows = self.get_reduced_global_rows()


    def get_reduced_global_rows(self):
        rows = []

        for i in range(self.n):
            index = i*2
            bc = self.nodes[i+1].B
            if bc == 'F':
                rows.append(index)
                rows.append(index + 1)
            if bc == 'HS':
                rows.append(index)
            if bc == 'VS':
                rows.append(index + 1)

        return rows


    def get_global_stiffness(self):
        global_k = np.zeros([self.n*2, self.n*2])

        for i in range(len(self.elements)):
            element = self.elements[i]
            LN1 = self.nodes[element.LN1]
            LN2 = self.nodes[element.LN2]
            ke = element.compose_stiffness()

            LN1i_u = (LN1.n-1)*2
            LN1i_v = LN1i_u + 2
            LN2i_u = (LN2.n-1)*2
            LN2i_v = LN2i_u + 2

            global_k[LN1i_u:LN1i_v, LN1i_u:LN1i_v] += ke[:2, :2]
            global_k[LN1i_u:LN1i_v, LN2i_u:LN2i_v] += ke[:1, 2:]
            global_k[LN2i_u:LN2i_v, LN1i_u:LN1i_v] += ke[2:, :1]
            global_k[LN2i_u:LN2i_v, LN2i_u:LN2i_v] += ke[2:, 2:]

        return global_k


    def get_global_force(self):
        global_f = np.zeros([self.n*2, 1])

        for i in range(self.n):
            global_f[i*2] = self.nodes[i+1].FX
            global_f[i*2+1] = self.nodes[i+1].FY

        return global_f


    def get_simplified_system(self):
        global_k = self.get_global_stiffness()
        global_f = self.get_global_force()

        simplified_rows = self.rows
        n = len(simplified_rows)

        temp_simplified_k = np.zeros([n, len(global_k[0])])
        simplified_k = np.zeros([n, n])
        simplified_f = np.zeros([n, 1])

        for i in range(n):
            temp_simplified_k[i,:] = global_k[simplified_rows[i], :]
        for i in range(n):
            simplified_k[i, :] = temp_simplified_k[:,simplified_rows[i]]
            simplified_f[i] = global_f[simplified_rows[i]]

        return simplified_k, simplified_f

    def get_final(self, u):
        displacement = np.zeros([self.n*2, 1])

        cnt = 0
        for i in range(self.n*2):
            if not i in self.rows:
                displacement[i] = 0
            else:
                displacement[i] = u[cnt]
                cnt += 1
        return displacement



