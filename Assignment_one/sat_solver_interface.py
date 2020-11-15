from pysat.solvers import Cadical
from pysat.formula import CNF

""" Interface to the SAT solver."""


def load_cnf_from_string(string):
    return CNF(from_string=string)


def solve_cnf_with_CaDiCaL(cnf):
    return solve_cnf(Cadical(cnf))


def solve_cnf(solver):
    return solver.solve(), solver.get_model()
