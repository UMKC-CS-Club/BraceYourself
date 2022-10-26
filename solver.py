import functools


@functools.lru_cache()
def get_tt_rows(n):
    if n == 0:
        return [[]]

    n_minus_1_rows = list(get_tt_rows(n - 1))

    result = []

    for row in n_minus_1_rows:
        result.append([True] + row)

    for row in n_minus_1_rows:
        result.append([False] + row)

    return result


# pls no odd-numbered string counts
def get_odd_possibilities(strings, knot_colors):
    for i, color in enumerate(knot_colors):
        left = strings[2 * i]
        right = strings[2 * i + 1]

        if left != color and right != color:
            return []

    possibilities = []
    for swaps in get_tt_rows(len(knot_colors)):
        new_strings = []
        for i, swap in enumerate(swaps):
            left = strings[2 * i]
            right = strings[2 * i + 1]

            if swap:
                new_strings.append(right)
                new_strings.append(left)
            else:
                new_strings.append(left)
                new_strings.append(right)

        possibilities.append(new_strings)

    return possibilities


def get_even_possibilities(strings, knot_colors):
    if strings[0] != knot_colors[0] or strings[-1] != knot_colors[-1]:
        return []

    for i in range(1, len(knot_colors) - 1):
        color = knot_colors[i]
        left = strings[2 * i - 1]
        right = strings[2 * i]

        if left != color and right != color:
            return []

    possibilities = []
    for swaps in get_tt_rows(len(knot_colors) - 2):
        new_strings = [strings[0]]
        for swap_i, i in enumerate(range(1, len(knot_colors) - 1)):
            swap = swaps[swap_i]
            left = strings[2 * i - 1]
            right = strings[2 * i]

            if swap:
                new_strings.append(right)
                new_strings.append(left)
            else:
                new_strings.append(left)
                new_strings.append(right)

        new_strings.append(strings[-1])

        possibilities.append(new_strings)

    return possibilities


def dfs_odd(strings, row_knots):
    if len(row_knots) == 0:
        return [strings]

    first, *rest = row_knots
    for possibility in get_odd_possibilities(strings, first):
        tail = dfs_even(possibility, rest)
        if len(tail) > 0:
            return [possibility] + tail

    return []


def dfs_even(strings, row_knots):
    if len(row_knots) == 0:
        return [strings]

    first, *rest = row_knots
    for possibility in get_even_possibilities(strings, first):
        tail = dfs_odd(possibility, rest)
        if len(tail) > 0:
            return [possibility] + tail

    return []


sol = dfs_odd(
    ['B', 'o', 'b', 'B', 'b', 'B', 'b', 'B', 'o', 'b', 'g', 'o'],
    [
        ['o', 'b', 'b', 'b', 'b', 'g'],
        ['B', 'b', 'B', 'B', 'B', 'b', 'o'],
        ['b', 'B', 'B', 'B', 'B', 'b'],
        # ['b', 'B', 'o', 'o', 'o', 'B', 'b'],
        # ['B', 'o', 'B', 'B', 'o', 'b'],
        # ['b', 'o', 'B', 'B', 'B', 'B', 'g'],
        # ['B', 'B', 'o', 'o', 'o', 'g'],
        # ['b', 'o', 'o', 'o', 'B', 'B', 'g'],
        # ['B', 'B', 'o', 'o', 'o', 'g'],
        # ['b', 'o', 'B', 'B', 'B', 'B', 'b'],
        # ['B', 'o', 'B', 'B', 'o', 'b'],
        # ['b', 'B', 'o', 'o', 'o', 'B', 'b'],
        # ['b', 'B', 'B', 'B', 'B', 'b'],
        # ['B', 'b', 'B', 'B', 'B', 'b', 'o'],
        # ['o', 'b', 'b', 'b', 'b', 'g'],
        # ['B', 'b', 'b', 'b', 'b', 'b', 'B'],
    ]
)

print(sol)
