from itertools import combinations, chain, product, count
from pysat.solvers import Cadical
from pysat.formula import CNF
import numpy as np


def as_DIMACS_CNF(clauses):
    n_var = len({abs(x) for clause in clauses for x in clause})
    n_clause = len(clauses)
    clauses_text = "c Encoding\n" + f"p {n_var} {n_clause}\n"
    clauses_ = [" ".join(str(x) for x in clause) for clause in clauses]
    clauses_text += " 0\n".join(clauses_) + " 0"
    return clauses_text


def list_to_numbers(string_list):
    return [int(x) for x in string_list]


def list_to_string(number_list):
    return " ".join(str(x) for x in number_list)


def get_adjacent_positions(pos, size, remove_pos=True, restricted=None, complement=None, orthogonal=False):
    assert size[0] >= 1 and size[1] >= 1, "Field size can not be smaller than one for any dimension!"
    assert 0 <= pos[0] <= size[0] and 0 <= pos[1] <= size[1], "Position outside field size!"
    size = (size[0] - 1, size[1] - 1)
    adj = {(min(size[0], max(0, pos[0] + i)), min(size[1], max(0, pos[1] + j)))
           for i in range(-1, 2) for j in range(-1, 2)}
    if remove_pos:
        adj.remove(pos)
    if orthogonal:
        adj = set(filter(lambda x: x[0] == pos[0] or x[1] == pos[1], adj))
    if restricted:
        adj = set(filter(lambda x: x in restricted, adj))
    if complement:
        adj = set(filter(lambda x: x not in complement, adj))

    return adj


def exactly_one(variables):
    clauses = [tuple(variables)]  # at least one
    clauses.extend(at_most_one(variables))  # exactly one
    return clauses


def at_most_one(variables):
    # IMPROVEMENT: Combinations is better than permutations
    return [(-x, -y) for x, y in combinations(variables, 2)]


def implies_all(var: int, implied_vars):
    return [(-var, implied_var) for implied_var in implied_vars]


class TentGameEncoding:
    def __init__(self, size, tree_positions, row_limits, column_limits, efficient=True, verbose=True,
                 algo_name="Default"):
        self.algo_name = algo_name
        self.size = size
        self.capacity = size[0] * size[1]
        self.tree_positions = tree_positions
        self.tent_positions = []
        self.column_limits = list(map(int, column_limits))
        self.row_limits = list(map(int, row_limits))
        self.cnf_solution = None
        tree_pos_to_id = {pos: idx + self.capacity for idx, pos in
                          enumerate([(x, y) for x in range(size[0]) for y in range(size[1])], 1)}
        if efficient:
            # Filter out unnecessary variables.
            self.tree_pos_to_id = {pos: idx for pos, idx in tree_pos_to_id.items() if pos in tree_positions}
            # We now that: if tent => tree must be orthogonally adjacent.
            # Further, also that a tent can not be at the same position as a tree!
            # Thus we can filter out positions that have no orthogonal adjacent tree or
            # are at the same position :)
            self.tent_pos_to_id = self.filter_tent_positions()

        else:
            # This is the unfiltered (inefficient) version
            self.tree_pos_to_id = {pos: idx for pos, idx in tree_pos_to_id.items() if pos in tree_positions}
            self.tent_pos_to_id = {pos: idx for idx, pos in
                                   enumerate([(x, y) for x in range(size[0]) for y in range(size[1])], 1)}
        self.counter = count(self.capacity * 2)

        if verbose:
            print("Created Tent with:")
            print("Efficient:", efficient)
            print(self.__dict__)
            print("Number of potential tent field variables:", len(self.tent_pos_to_id))

    @classmethod
    def from_randomness(cls, size=(8, 8), tree_density=0.5, algo_name="Default"):
        d = int(tree_density * size[0] * size[1])
        tree_indices = list(set((np.random.randint(size[0]), np.random.randint(size[1])) for _ in range(d)))
        game = cls(size, tree_indices, row_limits=[], column_limits=[], verbose=False, algo_name=algo_name)
        game.reduce_to_possible_solution()
        return game

    @classmethod
    def from_game_id(cls, game_id, verbose=True, efficient=True, algo_name="Default"):
        from Assignment_one import parse_gameid
        game_text = parse_gameid.parse_id(game_id)
        path = 'data\\game_file.txt'
        with open(path, 'w') as f:
            f.write(game_text)
        return cls.from_text_file(path, verbose, efficient, algo_name=algo_name)

    @classmethod
    def from_text_file(cls, path, verbose=True, efficient=True, algo_name="Default"):
        with open(path, "r") as f:
            size = tuple(list_to_numbers(f.readline().split(" ")))
            lines = [line.replace("\n", "").split(" ") for line in f.readlines()]
            row_limits, column_limits, tree_indices = [], list_to_numbers(lines.pop()), []
            index_row = -1
            for line in lines:
                index_row += 1
                index_column = -1
                row_limits.append(line.pop())
                for symbol in line[0]:
                    index_column += 1
                    if symbol == "T":
                        tree_indices.append((index_row, index_column))

            return cls(size, tree_indices, row_limits, column_limits, verbose=verbose, efficient=efficient,
                       algo_name=algo_name)

    def filter_tent_positions(self):
        tent_pos_to_id = {pos: idx for idx, pos in
                          enumerate([(x, y) for x in range(self.size[0]) for y in range(self.size[1])], 1)}
        adjacent_to_trees = {pos for tree_pos in self.tree_positions for pos in
                             get_adjacent_positions(tree_pos, self.size, orthogonal=True,
                                                    complement=self.tree_positions)}
        return {pos: idx for pos, idx in tent_pos_to_id.items() if pos in adjacent_to_trees}

    @staticmethod
    def get_solution(conditions):
        cnf_string = as_DIMACS_CNF(conditions)
        solver = Cadical(CNF(from_string=cnf_string))
        solved, solution = solver.solve(), solver.get_model()
        return solved, solution

    def check_solution(self, solution):
        """ Input: Positions (x,y) of tents.
            Output: Whether it is valid?"""
        tent_ids = [self.tent_pos_to_id.get(tent_pos, None) for tent_pos in solution]
        if not solution or None in tent_ids:
            return False
        cnf = self.get_cnf_solution() + [[tent_id] for tent_id in tent_ids]
        valid_solution, _ = self.get_solution(cnf)
        return valid_solution

    def reduce_to_possible_solution(self):
        solved, solution = False, None
        while not solved and self.tree_positions:
            v = self.tree_positions.pop()
            del self.tree_pos_to_id[v]
            self.tent_pos_to_id = self.filter_tent_positions()
            conditions = self.condition_one_clauses() + self.condition_three_clauses()
            solved, solution = self.get_solution(conditions)
        # Assign row and column limits
        self.row_limits = [0] * self.size[0]
        self.column_limits = [0] * self.size[1]
        for tent_pos, tent_id in self.tent_pos_to_id.items():
            r, c = tent_pos
            if tent_id in solution:
                self.row_limits[r] += 1
                self.column_limits[c] += 1
        self.solve_sat_problem()

    def solve_sat_problem(self):
        solved, solution = self.get_solution(self.get_cnf_solution())
        assert solved
        for tent_pos, tent_id in self.tent_pos_to_id.items():
            if tent_id in solution:
                self.tent_positions.append(tent_pos)

    def get_cnf_solution(self):
        if not self.cnf_solution:
            """Combine all conditions."""
            # c_zero = self.condition_zero_clauses()
            c_one = self.condition_one_clauses()
            c_two = self.condition_two_clauses()
            c_three = self.condition_three_clauses()
            clauses = c_one + c_two + c_three
            # Remove duplicates.
            self.cnf_solution = [list(c) for c in set(frozenset(c) for c in clauses)]
        return self.cnf_solution

    def condition_zero_clauses(self):
        """Tents must be placed in an empty cell.
        In other words, no tent if there is a tree.
        Thus, we iterate over all trees and assure that no tent can be in that field.

        !! Since in __init__ we prefiltered the variables, this is no longer necessary"""
        s = set(self.tree_positions).intersection(self.tent_pos_to_id.keys())
        return [(-self.tent_pos_to_id[pos], self.tree_pos_to_id[pos]) for pos in s]

    def condition_one_clauses(self):
        """No two tents are adjacent in any of the (up to) 8 directions.
        Thus, if tent there must not exist any further tent in adjacent positions.
        A => -B, where B is any adjacent field."""
        adj_pairs = [(pos, get_adjacent_positions(pos, self.size, restricted=self.tent_pos_to_id.keys())) for pos in
                     self.tent_pos_to_id.keys()]
        return list(chain(*[implies_all(self.tent_pos_to_id[pos],
                                        map(lambda x: -self.tent_pos_to_id.get(x), adj))
                            for pos, adj in adj_pairs]))

    def condition_two_clauses(self):
        # TODO: This method can scale really poorly! Further optimization needed.
        """The number of tents in each row/column matches the number specified."""

        def extend_clauses(var, limit):
            """Binomial Encoding:
            See: SAT Encodings of the At-Most-k Constraint, Some Old, Some New, Some Fast, Some Slow"""
            # print(len(var), limit)
            for comb in combinations(var, limit + 1):
                c_less_than = [-v for v in comb]
                clauses.append(c_less_than)
            for comb in combinations(var, len(var) - limit + 1):
                c_greater_than = [v for v in comb]
                clauses.append(c_greater_than)

        clauses = []
        # Get possible valid combinations regarding rows.
        for index, row_limit in enumerate(self.row_limits):
            positions = [var for pos, var in self.tent_pos_to_id.items() if pos[0] == index]
            extend_clauses(positions, row_limit)

        # Get possible valid combinations regarding columns.
        for index, column_limit in enumerate(self.column_limits):
            positions = [var for pos, var in self.tent_pos_to_id.items() if pos[1] == index]
            extend_clauses(positions, column_limit)
        return clauses

    def condition_three_clauses(self):
        # TODO

        """It is possible to match tents to trees 1:1,
         such that each tree is orthogonally adjacent to its own tent
        (but may also be adjacent to other tents).

        NOTE: Due to pre-filtering we already ensured there exists at least one tree
        orthogonally. Thus, it suffices to only further constrain 1:1 mappings."""
        # Get links from adjacent trees to tent.
        tents_to_trees = list(chain(*[
            product([pos], get_adjacent_positions(pos, self.size, orthogonal=True, restricted=self.tree_positions))
            for pos in self.tent_pos_to_id.keys()]))
        # Get links from adjacent tents to tree.
        trees_to_tents = list(chain(*[
            product([pos],
                    get_adjacent_positions(pos, self.size, orthogonal=True, restricted=self.tent_pos_to_id.keys()))
            for pos in self.tree_positions]))

        # Order matters, i.e (Tree,Tent)!
        trees_to_tents = {(self.tree_pos_to_id[tree_pos], self.tent_pos_to_id[tent_pos])
                          for tree_pos, tent_pos in trees_to_tents}
        tents_to_trees = {(self.tree_pos_to_id[tree_pos], self.tent_pos_to_id[tent_pos])
                          for tent_pos, tree_pos in tents_to_trees}

        link_pairs = trees_to_tents.union(tents_to_trees)

        # Create new link "variables"
        links = {(tree_id, tent_id): next(self.counter) for tree_id, tent_id in link_pairs}
        # If Link(Tree,Tent) => Tree and Tent
        clauses_link = [implies_all(link, [tree, tent]) for (tree, tent), link in links.items()]

        def links_to(token):
            r = [v for k, v in links.items() if token in k]
            if not r:
                r = [1, 1]  # Force falsification.
            return r

        tree_unique = [exactly_one(links_to(tree)) for tree in self.tree_pos_to_id.values()]
        tent_unique = [at_most_one(links_to(tent)) for tent in self.tent_pos_to_id.values()]

        # Concatenate
        clauses = list(chain(*(clauses_link + tree_unique + tent_unique)))

        return clauses

    def output_field(self):
        encoding = [list_to_string(self.size)]
        for r_index in range(self.size[0]):
            row = []
            for c_index in range(self.size[1]):
                if (r_index, c_index) in self.tree_positions:
                    row.append("T")
                elif (r_index, c_index) in self.tent_positions:
                    row.append("C")
                else:
                    row.append(".")
            row.append(" " + str(self.row_limits[r_index]))
            encoding.append("".join(row))

        encoding.append(list_to_string(self.column_limits))
        encoding = "\n".join(encoding)
        return encoding
