import numpy as np
import truss2D


class Assembler:

    def __init__(self, filename):
        self.file = open(filename, "r")
        next(self.file)
        next(self.file)
        self.global_params = self.get_global_params(self.file.readline())
        next(self.file)

        self.elements = []
        self.nodes = {}


    def find_param(self, var, element):
        start_pos = element.find(var + ':')
        if start_pos == -1: return ""
        end_pos = element.find(',', start_pos)
        if end_pos == -1: return element[start_pos + len(var) + 1:].strip('\n')
        return element[start_pos + len(var) + 1:end_pos]


    def get_global_params(self, global_header):
        global_params = {}
        global_params["L"] = self.find_param('L', global_header)
        global_params["A"] = self.find_param('A', global_header)
        global_params["E"] = self.find_param('E', global_header)
        global_params["PHI"] = self.find_param('PHI', global_header)
        return global_params


    def get_element(self, element):
        LN1 = self.find_param('LN1', element)
        LN2 = self.find_param('LN2', element)
        L = self.find_param('L', element)
        A = self.find_param('A', element)
        E = self.find_param('E', element)
        PHI = self.find_param('PHI', element)

        if L == '': L = self.global_params["L"]
        if A == '': A = self.global_params["A"]
        if E == '': E = self.global_params["E"]
        if PHI == '': PHI = self.global_params["PHI"]

        return truss2D.TrussElement(LN=[LN1, LN2], L=L, A=A, E=E, PHI=PHI)


    def get_elements(self):
        while 1:
            buffer = self.file.readline()
            if buffer == '\n': break
            self.elements.append(self.get_element(buffer))


    def get_node(self, node):
        n = node.split(': ', 1)[0]
        n = n[1:]

        FX = self.find_param('FX', node)
        FY = self.find_param('FY', node)
        M = self.find_param('M', node)
        B = self.find_param('B', node)
        XC = self.find_param('XC', node)
        YC = self.find_param('YC', node)

        if FX == '': FX = 0
        if FY == '': FY = 0
        if M == '': M = 0
        if B == '': B = 'F'
        if XC == '': XC = 0
        if YC == '': YC = 0

        return truss2D.TrussNode(n=n, FX=FX, FY=FY, M=M, B=B, X=XC, Y=YC)


    def get_nodes(self):
        while 1:
            buffer = self.file.readline()
            if buffer == '\n': break
            node = self.get_node(buffer)
            self.nodes[node.n] = node


    def get_element_props(self):
        for element in self.elements:
            if element.L == 0 or element.PHI == 0:
                LN1X = self.nodes[element.LN1].X
                LN1Y = self.nodes[element.LN1].Y
                LN2X = self.nodes[element.LN2].X
                LN2Y = self.nodes[element.LN2].Y

                element.L = abs(np.sqrt((LN2X-LN1X)**2 + (LN2Y-LN1Y)**2))
                element.PHI = np.degrees(np.arctan2(LN2Y-LN1Y, LN2X - LN1X))


    def handle_truss(self):
        self.get_elements()
        self.get_nodes()
        self.get_element_props()
