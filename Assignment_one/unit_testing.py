import unittest
from Assignment_one import game
import glob

from Assignment_one.game import exactly_one


class TestGame(unittest.TestCase):

    def check_valid_matching(self, expressions, matching):
        valid_term = True
        for expression in expressions:
            clause = [not matching[abs(int(i)) - 1] if int(i) < 0 else matching[abs(int(i)) - 1]
                      for i in expression.split(" ")]
            self.assertLessEqual(len(clause), len(matching))
            valid_clause = any(clause)
            valid_term = valid_term and valid_clause
        return valid_term

    def setUp(self) -> None:
        self.paths = glob.glob("tent-inputs\\*.txt")
        self.games = [game.TentGameEncoding.from_text(path, verbose=False) for path in self.paths]

    def test_adjacent(self):
        adj_1 = game.get_adjacent_positions((0, 0), (8, 8))
        sol_1 = {(0, 1), (1, 0), (1, 1)}

        adj_2 = game.get_adjacent_positions((17, 3), (23, 4))
        sol_2 = {(16, 3), (18, 3), (16, 2), (17, 2), (18, 3), (18, 2)}

        adj_3 = game.get_adjacent_positions((4, 4), (7, 7))
        sol_3 = {(3, 3), (3, 4), (3, 5), (4, 3), (4, 5), (5, 3), (5, 4), (5, 5)}

        self.assertSetEqual(adj_1, sol_1)
        self.assertSetEqual(adj_2, sol_2)
        self.assertSetEqual(adj_3, sol_3)

    def test_reproduce_field(self):
        # Test does not check if tents are modeled correctly.
        # but if we can reproduce the original field encoding based on internal data.
        for index, g in enumerate(self.games):
            with open(self.paths[index], "r") as f:
                original_field = f.read()
            self.assertEqual(g.output_field(), original_field)

    def test_exactly_one(self):
        variable_length = 10
        sat_cnf = exactly_one(list(range(1, variable_length + 1)))
        expressions = sat_cnf.split("\n")
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


if __name__ == "__main__":
    unittest.main()
