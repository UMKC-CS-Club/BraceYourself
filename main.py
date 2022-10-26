import pygame
import json


def get_selected_knot_center(mouse_x, mouse_y, cell_radius):
    column, intracell_x = divmod(mouse_x, cell_radius)
    row, intracell_y = divmod(mouse_y, cell_radius)

    if (row + column) % 2 == 0:
        if (intracell_x + intracell_y) < cell_radius:
            return row, column

        return row + 1, column + 1

    # else odd case

    if intracell_x > intracell_y:
        return row, column + 1

    return row + 1, column


def main():
    pygame.init()

    n_strings = 12
    n_cols = n_strings + 1
    n_rows = 2 * n_strings + 1

    cell_radius = 25

    screen = pygame.display.set_mode((n_strings * cell_radius, (n_rows - 1) * cell_radius))

    pallete = [
        (0, 0, 0),
        (255, 128, 0),
        (0, 255, 0),
        (200, 130, 0),
    ]

    curr_brush = 1

    try:
        with open('autosave.json') as f:
            cell_matrix = json.load(f)
    except FileNotFoundError:
        cell_matrix = [
            [pallete[0] for knot in range((n_cols // 2) + (1 - (r % 2)))]
            for r in range(n_rows)
        ]

    flag = True
    while flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag = False

            elif event.type == pygame.KEYDOWN:
                pressed = pygame.key.get_pressed()
                if pressed[pygame.K_SPACE]:
                    r, c = get_selected_knot_center(*pygame.mouse.get_pos(), cell_radius)
                    k = c // 2

                    curr_brush = pallete.index(tuple(cell_matrix[r][k]))

                elif pressed[pygame.K_DOWN]:
                    cell_matrix.append(cell_matrix.pop(0))
                    cell_matrix.append(cell_matrix.pop(0))

            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
                pressed = pygame.mouse.get_pressed()

                r, c = get_selected_knot_center(*event.pos, cell_radius)
                k = c // 2

                if pressed[0]:  # brush
                    cell_matrix[r][k] = pallete[curr_brush]
                elif pressed[2]:  # eraser
                    cell_matrix[r][k] = pallete[0]

            elif event.type == pygame.KEYDOWN:
                pressed = pygame.key.get_pressed()
                if pressed[pygame.K_RIGHT]:
                    curr_brush = (curr_brush + 1) % len(pallete)
                elif pressed[pygame.K_LEFT]:
                    curr_brush = (curr_brush - 1) % len(pallete)

        screen.fill((0, 0, 0))

        for r, row in enumerate(cell_matrix):
            for k, color in enumerate(row):
                c = 2 * k + (r % 2)

                points = (
                    (c + 1, r),
                    (c, r - 1),
                    (c - 1, r),
                    (c, r + 1),
                )

                scaled_points = [[cell_radius * scalar for scalar in point] for point in points]

                pygame.draw.polygon(screen, color, scaled_points)
                pygame.draw.polygon(screen, (255, 255, 255), scaled_points, width=1)

        pygame.draw.circle(screen, pallete[curr_brush], pygame.mouse.get_pos(), 0.1 * cell_radius)

        pygame.display.flip()

    pygame.quit()

    with open('autosave.json', 'w') as f:
        json.dump(cell_matrix, f)


if __name__ == '__main__':
    main()
