from math import ceil


class KnotContainer:
    """
    Just a 2D array rn, eventually an array or arrays of length n_strings / 2
    """

    def __init__(self, n_strings, n_primary_rows):
        self.n_strings = n_strings
        self.n_rows = n_primary_rows
        self.row_width = ceil(n_strings / 2)
        self.skipped_rows = self.row_width - 1

        height = self.n_rows + self.skipped_rows
        # TODO: store rows of length row_width
        self.matrix = [[None] * height for i in range(height)]

    def add_primary_row(self):
        for row in self.matrix:
            row.append(None)

        self.matrix.append([None] * (len(self.matrix) + 1))

    def check_valid_position(self, f, b):
        # TODO: Lower bound check
        return (f + b >= self.skipped_rows) and (abs(f - b) <= self.row_width)

    def __getitem__(self, key):
        if not isinstance(key, tuple) or not len(key) == 2:
            raise ValueError(f"(f, b)")  # TODO: better error message

        f, b = key

        if not self.check_valid_position(f, b):
            raise IndexError(f"({f}, {b}) out of range")

        return self.matrix[f][b]

    def __setitem__(self, key, value):
        if not isinstance(key, tuple) or not len(key) == 2:
            raise ValueError(f"(f, b)")  # TODO: better error message

        f, b = map(int, key)

        if not self.check_valid_position(f, b):
            raise IndexError(f"({f}, {b}) out of range")

        self.matrix[f][b] = value

    def __iter__(self):
        for f, row in enumerate(self.matrix):
            for b, item in enumerate(row):
                if not self.check_valid_position(f, b):
                    continue

                yield (f, b), item
