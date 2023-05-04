from collections import Counter
from math import ceil


class KnotContainer:
    """
    Just a 2D array rn, eventually an array or arrays of length n_strings / 2
    """

    def __init__(self, n_strings, n_primary_rows, row_width, skipped_rows, matrix, colors):
        """ Not meant to be used directly, please use .empty() or .from_dict() """
        self.n_strings = n_strings
        self.n_primary_rows = n_primary_rows
        self.row_width = row_width
        self.skipped_rows = skipped_rows

        self.matrix = matrix
        self.colors = colors

    @classmethod
    def empty(cls, n_strings, n_primary_rows):
        row_width = ceil(n_strings / 2)
        skipped_rows = row_width - 1

        height = n_primary_rows + skipped_rows + 1
        # TODO: store rows of length row_width
        matrix = [[None] * height for i in range(height)]
        colors = Counter()

        return cls(
            n_strings,
            n_primary_rows,
            row_width,
            skipped_rows,
            matrix,
            colors,
        )

    @classmethod
    def from_dict(cls, d):
        n_strings = d['n_strings']
        colors = Counter({tuple(c): 0 for c in d['colors']})
        matrix = []
        for row in d['matrix']:
            new_row = []
            for c in row:
                if c is None:
                    new_row.append(None)
                    continue

                color = tuple(d['colors'][c])

                colors[color] += 1
                new_row.append(color)

            matrix.append(new_row)

        row_width = ceil(n_strings / 2)
        skipped_rows = row_width - 1

        n_primary_rows = len(matrix) - skipped_rows - 1

        return cls(
            n_strings,
            n_primary_rows,
            row_width,
            skipped_rows,
            matrix,
            colors,
        )

    def to_dict(self):
        color_id = {}
        matrix = []
        for row in self.matrix:
            new_row = []
            for color in row:
                if color is None:
                    new_row.append(None)
                    continue

                t_color = tuple(color)
                if t_color not in color_id:
                    color_id[t_color] = len(color_id)

                new_row.append(color_id[t_color])

            matrix.append(new_row)

        colors = list(color_id)

        return {
            "n_strings": self.n_strings,
            "colors": colors,
            "matrix": matrix,
        }

    def add_primary_row(self):
        for row in self.matrix:
            row.append(None)

        self.matrix.append([None] * (len(self.matrix) + 1))

        self.n_primary_rows += 1

    def check_valid_position(self, f, b):
        # TODO: Right edges of odd-stringed patterns
        return (
            (0 <= f + b - self.skipped_rows < 2 * self.n_primary_rows)
            and (abs(f - b) <= self.row_width)
        )

    def check_knot_exists(self, f, b):
        return self.check_valid_position(f, b) and self.matrix[f][b] is not None

    def __getitem__(self, key):
        if not isinstance(key, tuple) or not len(key) == 2:
            raise ValueError(f"Expected a tuple of the form (f, b)")

        f, b = key

        if not self.check_valid_position(f, b):
            raise IndexError(f"({f}, {b}) out of range")

        return self.matrix[f][b]

    def __setitem__(self, key, value):
        if not isinstance(key, tuple) or not len(key) == 2:
            raise ValueError(f"Expected a tuple of the form (f, b)")

        f, b = key

        if not self.check_valid_position(f, b):
            raise IndexError(f"({f}, {b}) out of range")

        self.colors[self.matrix[f][b]] -= 1
        self.colors[value] += 1
        self.matrix[f][b] = value

    def __iter__(self):
        for f, row in enumerate(self.matrix):
            for b, item in enumerate(row):
                if not self.check_valid_position(f, b):
                    continue

                yield (f, b), item

    def get_active_colors(self):
        return tuple(c for (c, v) in self.colors.items() if v > 0)
