import numpy as np


class Projector:
    def __init__(self, knots, cscribe_radius, screen_width):
        self.knots = knots
        self.cscribe_radius = cscribe_radius
        self.screen_width = screen_width

        self.pivot = knots.skipped_rows / 2

        self.rel_to_pivot_translation = np.matrix([
            [1, 0, -self.pivot],
            [0, 1, -self.pivot],
            [0, 0, 1],
        ])

        self.about_pivot_rotation = np.matrix([
            [1, -1, 0],
            [1, 1,  0],
            [0, 0,  1],
        ])

        self.cscribe_scale = np.matrix([
            [cscribe_radius, 0,              0],
            [0,              cscribe_radius, 0],
            [0,              0,              1],
        ])

        self.screen_translation = np.matrix([
            [1, 0,  screen_width / 2],
            [0, 1,  0               ],
            [0, 0,  1               ],
        ])

        self.matrix = (
                self.screen_translation
                * self.cscribe_scale
                * self.about_pivot_rotation
                * self.rel_to_pivot_translation
        )

        self.matrix_inverse = np.linalg.inv(self.matrix)

    def project_points(self, *points):
        homatricized = np.matrix([
            [x, y, 1] for (x, y) in points
        ]).transpose()

        projected_points = [(x / w, y / w) for (x, y, w) in (self.matrix * homatricized).transpose().tolist()]

        return projected_points

    def unproject_points(self, *points):
        homatricized = np.matrix([
            [x, y, 1] for (x, y) in points
        ]).transpose()

        unprojected_points = [(x / w, y / w) for (x, y, w) in (self.matrix_inverse * homatricized).transpose().tolist()]

        return unprojected_points

