import unittest

from pysat.formula import CNF
from pysat.solvers import Cadical

from game import *
import glob

from Assignment_one.game import exactly_one, implies_all, as_DIMACS_CNF


class TestGame(unittest.TestCase):

    def check_valid_matching(self, expressions, matching):
        valid_term = True
        for expression in expressions:
            clause = [not matching[abs(i) - 1] if int(i) < 0 else matching[abs(i) - 1]
                      for i in expression]
            self.assertLessEqual(len(clause), len(matching))
            valid_clause = any(clause)
            valid_term = valid_term and valid_clause
        return valid_term

    def setUp(self) -> None:
        self.paths = glob.glob("tent-inputs\\*.txt")
        self.paths = [p for p in self.paths if "gamefield" not in p]
        # self.games = [game.GameEncoderBinomial.from_text_file(path, verbose=False) for path in self.paths]
        self.games = [GameEncoderSequential.from_text_file(path, verbose=False) for path in self.paths]
        # self.games = [game.GameEncoderBinary.from_text_file(path, verbose=False) for path in self.paths]

    def test_randomness(self):
        g1 = GameEncoderSequential.from_randomness((10, 10), tree_density=0.25)
        g1.solve_sat_problem()
        solved, _ = g1.get_solution(g1.get_cnf_solution())
        self.assertTrue(solved)

    def test_adjacent(self):
        adj_1 = get_adjacent_positions((0, 0), (8, 8))
        sol_1 = {(0, 1), (1, 0), (1, 1)}

        adj_2 = get_adjacent_positions((17, 3), (23, 4))
        sol_2 = {(16, 3), (18, 3), (16, 2), (17, 2), (18, 3), (18, 2)}

        adj_3 = get_adjacent_positions((4, 4), (7, 7))
        sol_3 = {(3, 3), (3, 4), (3, 5), (4, 3), (4, 5), (5, 3), (5, 4), (5, 5)}

        adj_4 = get_adjacent_positions((4, 4), (7, 7), orthogonal=True)
        sol_4 = {(3, 4), (4, 3), (4, 5), (5, 4)}

        adj_5 = get_adjacent_positions((4, 4), (7, 7), orthogonal=True)
        sol_5 = {(3, 3), (3, 4), (3, 5), (4, 3), (4, 5), (5, 3), (5, 4), (5, 5)}

        self.assertSetEqual(adj_1, sol_1)
        self.assertSetEqual(adj_2, sol_2)
        self.assertSetEqual(adj_3, sol_3)
        self.assertSetEqual(adj_4, sol_4)
        self.assertNotEqual(adj_5, sol_5)

    def test_reproduce_field(self):
        # Test does not check if tents are modeled correctly.
        # but if we can reproduce the original field encoding based on internal data.
        games = [GameEncoderSequential.from_text_file(path, verbose=False) for path in self.paths]
        for index, g in enumerate(games):
            with open(self.paths[index], "r") as f:
                original_field = f.read()
                self.assertEqual(g.output_field(), original_field)

    def test_implies_all(self):
        variable_length = 10
        expression = implies_all(1, [2, 3, 4, 5, 6])
        variables = [False] * variable_length
        variables[:6] = [True] * 6
        valid_check_one = self.check_valid_matching(expression, variables)
        self.assertTrue(valid_check_one)

        variables2 = [False] * variable_length
        variables2[:6] = [True] * 3
        valid_check_two = self.check_valid_matching(expression, variables2)
        self.assertFalse(valid_check_two)

        variables3 = [False] * variable_length
        valid_check_three = self.check_valid_matching(expression, variables3)
        self.assertTrue(valid_check_three)

    def test_exactly_one(self):
        variable_length = 10
        expressions = exactly_one(list(range(1, variable_length + 1)))
        for index_true in range(variable_length):
            variables = [False] * variable_length
            variables[index_true] = True
            valid_check_one = self.check_valid_matching(expressions, variables)
            self.assertTrue(valid_check_one)
        variables_two = [False] * variable_length
        valid_check_two = self.check_valid_matching(expressions, variables_two)
        self.assertFalse(valid_check_two)
        variables_three = [False] * variable_length
        variables_three[:3] = [True] * 3
        valid_check_two_three = self.check_valid_matching(expressions, variables_three)
        self.assertFalse(valid_check_two_three)

    def test_pos_to_index(self):
        for index, g in enumerate(self.games):
            self.assertLessEqual(len(g.tent_pos_to_id), g.capacity)
            self.assertEqual(len(g.tree_pos_to_id), len(g.tree_positions))

            self.assertLessEqual(max(g.tent_pos_to_id.values()), g.capacity)
            self.assertLessEqual(max(g.tree_pos_to_id.values()), g.capacity * 2)
            self.assertGreater(min(g.tent_pos_to_id.values()), 0)
            self.assertGreater(min(g.tree_pos_to_id.values()), g.capacity)

    def test_condition_zero_clauses(self):
        for index, g in enumerate(self.games):
            cond = g.condition_zero_clauses()
            if cond:
                solver = Cadical(CNF(from_string=as_DIMACS_CNF(cond)))
                self.assertTrue(solver.solve())

    def test_condition_one_clauses(self):
        for index, g in enumerate(self.games):
            cond = g.condition_one_clauses()
            self.assertLessEqual(len(cond), 8 * g.capacity)
            solver = Cadical(CNF(from_string=as_DIMACS_CNF(cond)))
            self.assertTrue(solver.solve())

    def test_condition_two_clauses(self):
        for index, g in enumerate(self.games):
            cond = g.condition_two_clauses()
            solver = Cadical(CNF(from_string=as_DIMACS_CNF(cond)))
            self.assertTrue(solver.solve())

    def test_condition_three_clauses(self):
        for index, g in enumerate(self.games):
            cond = g.condition_three_clauses()
            solver = Cadical(CNF(from_string=as_DIMACS_CNF(cond)))
            self.assertTrue(solver.solve())

    def test_as_DIMACS_CNF(self):
        for index, g in enumerate(self.games):
            cond = g.get_cnf_solution()
            solver = Cadical(CNF(from_string=as_DIMACS_CNF(cond)))
            self.assertTrue(solver.solve())

    def test_check_solution(self):
        for index, g in enumerate(self.games):
            g.solve_sat_problem()
            self.assertTrue(g.check_solution(g.tent_positions))

    def test_check_equal_solution(self):
        games1 = [GameEncoderBinomial.from_text_file(path, verbose=False) for path in self.paths]
        games2 = [GameEncoderSequential.from_text_file(path, verbose=False) for path in self.paths]
        games3 = [GameEncoderBinary.from_text_file(path, verbose=False) for path in self.paths]
        for g1, g2, g3 in zip(games1, games2, games3):
            g1.solve_sat_problem()
            g2.solve_sat_problem()
            g3.solve_sat_problem()
            self.assertTrue(g1.tent_positions == g2.tent_positions == g3.tent_positions)


if __name__ == "__main__":
    unittest.main()
