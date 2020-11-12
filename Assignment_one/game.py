from itertools import permutations


def list_to_numbers(string_list):
    return [int(x) for x in string_list]


def list_to_string(number_list):
    return " ".join(str(x) for x in number_list)


def get_adjacent_positions(pos, size):
    assert size[0] >= 1 and size[1] >= 1, "Field size can not be smaller than one for any dimension!"
    assert 0 <= pos[0] <= size[0] and 0 <= pos[1] <= size[1], "Position outside field size!"
    size = (size[0] - 1, size[1] - 1)
    adj = {(min(size[0], max(0, pos[0] + i)), min(size[1], max(0, pos[1] + j)))
           for i in range(-1, 2) for j in range(-1, 2)}
    adj.remove(pos)
    return adj


def exactly_one(variables):
    clauses = [" ".join(str(x) for x in variables)]  # at least one
    for x, y in permutations(variables, 2):
        clauses.append(f"-{x} -{y}")
    return "\n".join(clauses)


class TentGameEncoding:
    def __init__(self, size, tree_indices, row_limit, column_limit, verbose=True):
        self.size = size
        self.tree_indices = tree_indices
        self.tent_indices = []
        self.column_limit = column_limit
        self.row_limit = row_limit
        self.position_to_id = {pos: idx for idx, pos in
                               enumerate([(x, y) for x in range(size[0]) for y in range(size[1])])}
        if verbose:
            print("Created Tent with:")
            print(self.__dict__)

    @classmethod
    def from_text(cls, path, verbose=True):
        with open(path, "r") as f:
            size = tuple(list_to_numbers(f.readline().split(" ")))
            lines = [line.replace("\n", "").split(" ") for line in f.readlines()]
            row_limit, column_limit, tree_indices = list_to_numbers(lines.pop()), [], []
            index_row = -1
            for line in lines:
                index_row += 1
                index_column = -1
                column_limit.append(line.pop())
                for symbol in line[0]:
                    index_column += 1
                    if symbol == "T":
                        tree_indices.append((index_row, index_column))

            return cls(size, tree_indices, row_limit, column_limit, verbose=verbose)

    def combine_conditions(self):
        # TODO
        """Combine all conditions."""
        pass

    def condition_zero(self):
        # TODO
        """Tents must be placed in an empty cell."""
        pass

    def condition_one(self):
        # TODO
        """No two tents are adjacent in any of the (up to) 8 directions."""
        pass

    def condition_two(self):
        # TODO
        """The number of tents in each row/column matches the number specified."""
        pass

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
                if (r_index, c_index) in self.tree_indices:
                    row.append("T")
                elif (r_index, c_index) in self.tent_indices:
                    row.append("C")
                else:
                    row.append(".")
            row.append(" " + self.column_limit[r_index])
            encoding.append("".join(row))

        encoding.append(list_to_string(self.row_limit))
        encoding = "\n".join(encoding)
        return encoding
