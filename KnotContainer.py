from math import ceil


class KnotContainer:
    """
    Just a 2D array rn, eventually an array or arrays of length n_strings / 2
    """

    def __init__(self, n_strings, n_primary_rows, row_width, skipped_rows, matrix):
        """ Not meant to be used directly, please use .empty() or .from_dict() """
        self.n_strings = n_strings
        self.n_primary_rows = n_primary_rows
        self.row_width = row_width
        self.skipped_rows = skipped_rows

        self.matrix = matrix

    @classmethod
    def empty(cls, n_strings, n_primary_rows):
        row_width = ceil(n_strings / 2)
        skipped_rows = row_width - 1

        height = n_primary_rows + skipped_rows
        # TODO: store rows of length row_width
        matrix = [[None] * height for i in range(height)]

        return cls(
            n_strings,
            n_primary_rows,
            row_width,
            skipped_rows,
            matrix,
        )

    @classmethod
    def from_dict(cls, d):
        n_strings = d['n_strings']
        matrix = d['matrix']

        row_width = ceil(n_strings / 2)
        skipped_rows = row_width - 1

        n_primary_rows = len(matrix) - skipped_rows

        return cls(
            n_strings,
            n_primary_rows,
            row_width,
            skipped_rows,
            matrix,
        )

    def to_dict(self):
        return {
            "n_strings": self.n_strings,
            "matrix": self.matrix,
        }

    def add_primary_row(self):
        for row in self.matrix:
            row.append(None)

        self.matrix.append([None] * (len(self.matrix) + 1))

        self.n_primary_rows += 1

    def check_valid_position(self, f, b):
        return (
            (0 <= f + b - self.skipped_rows < 2 * self.n_primary_rows - 1)  # TODO: Verify this
            and (abs(f - b) <= self.row_width)
        )

    def check_knot_exists(self, f, b):
        return self.check_valid_position(f, b) and self.matrix[f][b] is not None

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

        f, b = key

        if not self.check_valid_position(f, b):
            raise IndexError(f"({f}, {b}) out of range")

        self.matrix[f][b] = value

    def __iter__(self):
        for f, row in enumerate(self.matrix):
            for b, item in enumerate(row):
                if not self.check_valid_position(f, b):
                    continue

                yield (f, b), item
