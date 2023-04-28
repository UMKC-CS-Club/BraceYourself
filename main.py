import pygame
from Projector import Projector
from terminal_interface import get_knot_container, prompt_save


def main():
    pygame.init()

    knots = get_knot_container()

    cscribe_radius = 25

    screen_width = knots.row_width * 2 * cscribe_radius
    screen_height = knots.n_primary_rows * 2 * cscribe_radius

    projector = Projector(knots, cscribe_radius, screen_width)

    screen = pygame.display.set_mode((screen_width, screen_height))

    pallete = [
        (0, 0, 0),
        (200, 200, 200),
        (255, 127, 178),
        (0, 0, 255),
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
                    coord, = projector.unproject_points(event.pos)
                    (b, f) = map(int, coord)
                    curr_brush = pallete.index(knots[f, b])

                elif pressed[pygame.K_RIGHT]:
                    curr_brush = (curr_brush + 1) % len(pallete)

                elif pressed[pygame.K_LEFT]:
                    curr_brush = (curr_brush - 1) % len(pallete)

                elif pressed[pygame.K_d]:
                    coord, = projector.unproject_points(pygame.mouse.get_pos())
                    (b, f) = map(int, coord)
                    color = knots[f, b]
                    print(f"({f}, {b}), {color}")

            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
                pressed = pygame.mouse.get_pressed()

                coord, = projector.unproject_points(pygame.mouse.get_pos())
                (b, f) = map(int, coord)

                event_used, color = False, None

                if pressed[0]:  # brush
                    event_used, color = True, pallete[curr_brush]
                elif pressed[2]:  # eraser
                    event_used, color = True, None

                if event_used:
                    try:
                        knots[f, b] = color
                    except IndexError as e:
                        pass

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
                width=1,
            )

        pygame.draw.circle(screen, pallete[curr_brush], pygame.mouse.get_pos(), 0.1 * cscribe_radius)

        pygame.display.flip()

    pygame.quit()

    # TODO: Store pallet and indices rather than duplicated RGBs

    prompt_save(knots)


if __name__ == '__main__':
    main()
