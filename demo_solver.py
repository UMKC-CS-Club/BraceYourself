from functools import partial

import networkx as nx
from constraint import Problem
from matplotlib import pyplot


def get_neighbors(r, c):
    """
    For   4
        3 X 1
          2

    return (X, 1), (X, 2), (X, 3), (X, 4)
    """
    edges = []
    dr, dc = (0, 1)

    for i in range(4):
        edges.append((r + dr, c + dc))
        dr, dc = dc, -dr

    return edges


def node_exists(matrix, width, height, row, column):
    return 0 <= row < height and 0 <= column < width and matrix[row][column]


def display_solution(solution, knots):
    string_colors = {}
    edge_strings = {}
    nodes = []

    for variable, value in solution.items():
        if isinstance(variable, int):
            string_colors[variable] = value
        else:
            nodes.extend(variable)
            edge_strings[variable] = value

    graph = nx.Graph()
    for node in nodes:
        (r, c) = node
        graph.add_node(node, pos=(c, -r), color=knots[r][c])

    for (start, end), string in edge_strings.items():
        graph.add_edge(start, end, color=string_colors[string])

    nx.draw(
        graph,
        pos=nx.get_node_attributes(graph, 'pos'),
        node_color=list(nx.get_node_attributes(graph, 'color').values()),
        edge_color=nx.get_edge_attributes(graph, 'color').values()
    )
    pyplot.show()


def main():
    BLUE = (0, 0, 1)
    PINK = (1, 0.5, 0.7)
    ORNG = (1, 0.5, 0)

    colors = [BLUE, PINK, ORNG]

    knots = [[None, BLUE, BLUE],
             [PINK, PINK, PINK],
             [BLUE, ORNG, None]]

    num_strings = 4

    problem = Problem()

    strings = list(range(num_strings))

    # Which color is each string?
    problem.addVariables(strings, colors)

    c_validator = partial(node_exists, knots, len(knots), len(knots))

    for f, row in enumerate(knots):
        for b, knot_color in enumerate(row):
            if knot_color is None:
                continue

            neighbors = get_neighbors(f, b)
            downstream_edges = [((f, b), n) for n in neighbors[:2] if c_validator(*n)]
            upstream_edges = [(n, (f, b)) for n in neighbors[2:] if c_validator(*n)]

            for edge in downstream_edges:
                # Which string passes along each edge?
                problem.addVariable(edge, strings)
                # print(f"{edge} may be one of {strings}")

            # Type 1: The set of strings on one side of any knot must be the same as the set on the other.
            if len(upstream_edges) * len(downstream_edges) > 0:
                if len(upstream_edges) == 1:
                    problem.addConstraint(
                        lambda u, d: u == d,
                        (upstream_edges[0], downstream_edges[0])
                    )
                else:  # len() == 2
                    problem.addConstraint(
                        lambda uf, ub, df, db: (uf == df and ub == db) or (uf == db and ub == df),  # || or ><
                        (*upstream_edges, *downstream_edges)
                    )

            # Type 2: One of the strings on both sides of a knot must be the same color as the knot.
            for side in [upstream_edges, downstream_edges]:
                if len(side) == 0:
                    continue

                if len(side) == 1:
                    problem.addConstraint(
                        lambda e, *s_color, knot_color=knot_color: s_color[e] == knot_color,
                        (side[0], *strings)
                    )
                else:  # len() == 2
                    problem.addConstraint(
                        lambda fe, be, *s_color, knot_color=knot_color: s_color[fe] == knot_color or s_color[be] == knot_color,
                        (*side, *strings)
                    )

    solution = problem.getSolution()
    display_solution(solution, knots)


if __name__ == '__main__':
    main()