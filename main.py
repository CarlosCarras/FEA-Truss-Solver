import startupProcess as start
import assembler
import constructor
import solver
import output

if __name__ == '__main__':
    filename = "simple_truss2"  + start.EXT
    #filename = start.handle_startup()
    element_type, units = start.get_filedata(filename)
    solver = solver.Solver()

    if element_type == start.ELEMENT_TRUSS:
        assembler = assembler.Assembler(filename)
        assembler.handle_truss()
        constructor = constructor.Constructor(elements=assembler.elements, nodes=assembler.nodes)
        k, f = constructor.get_simplified_system()
        u = constructor.get_final(solver.solve_all(k, f))

    output.gen_output(filename, element_type, units, u)
    output.disp_output(filename, element_type, units, u)
