from itertools import combinations, chain


def list_to_numbers(string_list):
    return [int(x) for x in string_list]


def list_to_string(number_list):
    return " ".join(str(x) for x in number_list)


def get_adjacent_positions(pos, size, remove_pos=True, restricted=None, orthogonal=False):
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
    return adj


def exactly_one(variables):
    clauses = [tuple(variables)]  # at least one
    # IMPROVEMENT: Combinations is better than permutations
    clauses.extend([(-x, -y) for x, y in combinations(variables, 2)])
    return clauses


def implies_all(var: int, implied_vars):
    return [(-var, implied_var) for implied_var in implied_vars]


def implies_all_multiple(var: [int], implied_vars):
    return [c for clause in [implies_all(v, implied_vars) for v in var] for c in clause]


class TentGameEncoding:
    def __init__(self, size, tree_positions, row_limits, column_limits, verbose=True):
        self.size = size
        self.capacity = size[0] * size[1]
        self.tree_positions = tree_positions
        self.tent_positions = []
        self.column_limits = list(map(int, column_limits))
        self.row_limits = list(map(int, row_limits))
        tree_pos_to_id = {pos: idx + self.capacity for idx, pos in
                          enumerate([(x, y) for x in range(size[0]) for y in range(size[1])], 1)}
        # Filter out unnecessary variables.
        self.tree_pos_to_id = {pos: idx for pos, idx in tree_pos_to_id.items() if pos in tree_positions}
        # We now that: if tent => tree must be orthogonally adjacent.
        # Further, also that a tent can not be at the same position as a tree!
        # Thus we can filter out positions that have no orthogonal adjacent tree or
        # are at the same position :)
        tent_pos_to_id = {pos: idx for idx, pos in
                          enumerate([(x, y) for x in range(size[0]) for y in range(size[1])], 1)}
        adjacent_to_trees = {pos for tree_pos in tree_positions
                             for pos in get_adjacent_positions(tree_pos, size, orthogonal=True) if
                             pos not in tree_positions}
        self.tent_pos_to_id = {pos: idx for pos, idx in tent_pos_to_id.items() if pos in adjacent_to_trees}
        if verbose:
            print("Created Tent with:")
            print(self.__dict__)
            print("Number of potential tent field variables:", len(self.tent_pos_to_id))

    @classmethod
    def from_text(cls, path, verbose=True):
        with open(path, "r") as f:
            size = tuple(list_to_numbers(f.readline().split(" ")))
            lines = [line.replace("\n", "").split(" ") for line in f.readlines()]
            row_limits, column_limits, tree_indices = list_to_numbers(lines.pop()), [], []
            index_row = -1
            for line in lines:
                index_row += 1
                index_column = -1
                column_limits.append(line.pop())
                for symbol in line[0]:
                    index_column += 1
                    if symbol == "T":
                        tree_indices.append((index_row, index_column))

            return cls(size, tree_indices, row_limits, column_limits, verbose=verbose)

    def combine_conditions(self):
        # TODO
        """Combine all conditions."""
        # c_zero = self.condition_zero_clauses()
        c_one = self.condition_one_clauses()

    def condition_zero_clauses(self):
        """Tents must be placed in an empty cell.
        In other words, no tent if there is a tree.
        Thus, we iterate over all trees and assure that no tent can be in that field.

        !! Since in __init__ we prefiltered the variables, this is no longer necessary"""
        # return [(-self.tent_pos_to_id[pos], self.tree_pos_to_id[pos]) for pos in self.tree_positions]
        pass

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
        # TODO: This method can scale really poorly (e.g at 25x30)!
        #   Further optimization needed.
        # Idea: (A and B) => C <-> (A => C) and (B => C)
        """The number of tents in each row/column matches the number specified."""

        def extend_clauses(var, limit):
            # print(self.size, limit, len(list(combinations(var, limit))))
            for valid_comb in combinations(var, limit):
                c = implies_all_multiple(valid_comb, [v for v in var if v not in valid_comb])
                clauses.extend(c)

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

    def condition_three(self):
        # TODO
        """It is possible to match tents to trees 1:1,
         such that each tree is orthogonally adjacent to its own tent
        (but may also be adjacent to other tents)."""
        pass

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
            row.append(" " + str(self.column_limits[r_index]))
            encoding.append("".join(row))

        encoding.append(list_to_string(self.row_limits))
        encoding = "\n".join(encoding)
        return encoding
