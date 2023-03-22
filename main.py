import pygame
import json

from KnotContainer import KnotContainer
from Projector import Projector


def main():
    pygame.init()

    n_strings = 12
    n_primary_rows = 12
    knots = KnotContainer(n_strings, n_primary_rows)

    cscribe_radius = 25

    screen_width = knots.row_width * 2 * cscribe_radius
    screen_height = knots.n_rows * 2 * cscribe_radius

    projector = Projector(knots, cscribe_radius, screen_width)

    screen = pygame.display.set_mode((screen_width, screen_height))

    pallete = [
        (0, 0, 0),
        (255, 128, 0),
        (0, 255, 0),
        (200, 130, 0),
    ]

    curr_brush = 1

    flag = True
    while flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag = False

            elif event.type == pygame.KEYDOWN:
                pressed = pygame.key.get_pressed()

                if pressed[pygame.K_SPACE]:
                    (b, f), = projector.unproject_points(event.pos)
                    curr_brush = pallete.index(knots[f, b])

                elif pressed[pygame.K_RIGHT]:
                    curr_brush = (curr_brush + 1) % len(pallete)

                elif pressed[pygame.K_LEFT]:
                    curr_brush = (curr_brush - 1) % len(pallete)

            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
                pressed = pygame.mouse.get_pressed()

                (b, f), = projector.unproject_points(event.pos)

                if pressed[0]:  # brush
                    knots[f, b] = pallete[curr_brush]
                elif pressed[2]:  # eraser
                    knots[f, b] = None

        screen.fill((0, 0, 0))

        for (f, b), knot_color in knots:
            projected_square = projector.project_points(
                (b,     f    ),
                (b + 1, f    ),
                (b + 1, f + 1),
                (b,     f + 1),
            )

            if knot_color is not None:
                pygame.draw.polygon(
                    screen,
                    knot_color,
                    projected_square,
                )
            pygame.draw.polygon(
                screen,
                (255, 255, 255),
                projected_square,
                width=1
            )

        pygame.draw.circle(screen, pallete[curr_brush], pygame.mouse.get_pos(), 0.1 * cscribe_radius)

        pygame.display.flip()

    pygame.quit()

    # TODO: fix autosave

    # with open('autosave.json', 'w') as f:
    #     json.dump(cell_matrix, f)


if __name__ == '__main__':
    main()
