# MODULE
import pygame, sys
import numpy as np

# initializare pygame
pygame.init()
pygame.font.init()
Arial = pygame.font.SysFont('Arial', 40)

# ---------
# CONSTANTE
# ---------
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
WIDTH = SCREEN_WIDTH
HEIGHT = 600
LINE_WIDTH = 15
WIN_LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 6
SQUARE_SIZE = 200
CROSS_WIDTH = 25
SPACE = 55
# rgb: red green blue
RED = (255, 0, 0)
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CROSS_COLOR_2 = (239, 231, 200)
CROSS_COLOR_1 = (66, 66, 66)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# ------
# ECRAN
# ------
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill(BG_COLOR)

# -------------
# TABLA DE JOC
# -------------
board = np.zeros((BOARD_ROWS, BOARD_COLS))


# ---------
# FUNCTII
# ---------

def set_caption(player):
    pygame.display.set_caption(f'Notatko: Player {player}\'s turn')


def setup_displayer():
    # background
    pygame.draw.rect(screen, WHITE, (0, HEIGHT, WIDTH, SCREEN_HEIGHT - HEIGHT))
    # horizontal top border
    pygame.draw.line(screen, BLACK, (0, HEIGHT), (WIDTH, HEIGHT), LINE_WIDTH)
    # vertical separator
    pygame.draw.line(screen, BLACK, (WIDTH / 2, HEIGHT), (WIDTH / 2, SCREEN_HEIGHT), LINE_WIDTH)

    tabla1 = Arial.render('Tabla 1', False, BLACK)
    screen.blit(tabla1, (LINE_WIDTH, HEIGHT + 2 * LINE_WIDTH))

    tabla2 = Arial.render('Tabla 2', False, BLACK)
    screen.blit(tabla2, (WIDTH - LINE_WIDTH - tabla2.get_width(), HEIGHT + 2 * LINE_WIDTH))


def draw_lines():
    # 1 orizontal
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    # 2 orizontal
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)

    # 1 vertical
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    # 2 vertical
    pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    # 3 vertical
    pygame.draw.line(screen, BLACK, (3 * SQUARE_SIZE, 0), (3 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    # 4 vertical
    pygame.draw.line(screen, LINE_COLOR, (4 * SQUARE_SIZE, 0), (4 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    # 5 vertical
    pygame.draw.line(screen, LINE_COLOR, (5 * SQUARE_SIZE, 0), (5 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

    setup_displayer()


def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                pygame.draw.line(screen, CROSS_COLOR_2,
                                 (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR_2, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 CROSS_WIDTH)

            elif board[row][col] == 2:
                pygame.draw.line(screen, CROSS_COLOR_1,
                                 (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR_1, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 CROSS_WIDTH)


def mark_square(row, col, player):
    board[row][col] = player


def available_square(row, col):
    if row >= BOARD_ROWS or col >= BOARD_COLS:
        return False
    return board[row][col] == 0


def is_table_full(table):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS // 2):
            if board[row][col + table * (BOARD_COLS // 2)] == 0:
                return False
    return True


def check_win():
    # CONSTRUIRE LEGATURA DINTRE TABLA 1 CATRE TABLA 2 PENTRU LINIILE VERTICALE ALE TABLEI 1
    # vertical win check_1
    for col in range(BOARD_COLS - 3):
        if (board[0][col] == 1 or board[0][col] == 2) and (board[1][col] == 1 or board[1][col] == 2) and (
                board[2][col] == 1 or board[2][col] == 2):
            draw_vertical_winning_line(col)
            if col == 0:
                board[0][1] = board[0][2] = board[1][1] = board[1][2] = board[2][1] = board[2][2] = 3
            elif col == 1:
                board[0][0] = board[0][2] = board[1][0] = board[1][2] = board[2][0] = board[2][2] = 3
            elif col == 2:
                board[0][0] = board[0][1] = board[1][0] = board[1][1] = board[2][0] = board[2][1] = 3
            # vertical win check_2
            for col in range(3, BOARD_COLS):
                if (board[0][col] == 1 or board[0][col] == 2) and (board[1][col] == 1 or board[1][col] == 2) and (
                        board[2][col] == 1 or board[2][col] == 2):
                    draw_vertical_winning_line(col)
                    return True

            # horizontal win check_2
            for row in range(BOARD_ROWS):
                if (board[row][3] == 1 or board[row][3] == 2) and (board[row][4] == 1 or board[row][4] == 2) and (
                        board[row][5] == 1 or board[row][5] == 2):
                    draw_horizontal_winning_line_2(row)
                    return True

            # asc diagonal win check_2
            if (board[2][3] == 1 or board[2][3] == 2) and (board[1][4] == 1 or board[1][4] == 2) and (
                    board[0][5] == 1 or board[0][5] == 2):
                draw_asc_diagonal_2()
                return True

            # desc diagonal win chek_2
            if (board[0][3] == 1 or board[0][3] == 2) and (board[1][4] == 1 or board[1][4] == 2) and (
                    board[2][5] == 1 or board[2][5] == 2):
                draw_desc_diagonal_2()
                return True

        # //////////////////////////////////////////////////////////////////////////////////////////////////////////////
        # CONSTRUIRE LEGATURA DINTRE TABLA 1 CATRE TABLA 2 PENTRU LINIILE ORIZONTALE ALE TABLEI 1
        # horizontal win check_1
        for row in range(BOARD_ROWS):
            if (board[row][0] == 1 or board[row][0] == 2) and (board[row][1] == 1 or board[row][1] == 2) and (
                    board[row][2] == 1 or board[row][2] == 2):
                draw_horizontal_winning_line_1(row)
                if row == 0:
                    board[1][0] = board[1][1] = board[1][2] = board[2][0] = board[2][1] = board[2][2] = 3
                elif row == 1:
                    board[0][0] = board[0][1] = board[0][2] = board[2][0] = board[2][1] = board[2][2] = 3
                elif row == 2:
                    board[0][0] = board[0][1] = board[0][2] = board[1][0] = board[1][1] = board[1][2] = 3
                # vertical win check_2
                for col in range(3, BOARD_COLS):
                    if (board[0][col] == 1 or board[0][col] == 2) and (board[1][col] == 1 or board[1][col] == 2) and (
                            board[2][col] == 1 or board[2][col] == 2):
                        draw_vertical_winning_line(col)
                        return True

                # horizontal win check_2
                for row in range(BOARD_ROWS):
                    if (board[row][3] == 1 or board[row][3] == 2) and (board[row][4] == 1 or board[row][4] == 2) and (
                            board[row][5] == 1 or board[row][5] == 2):
                        draw_horizontal_winning_line_2(row)
                        return True

                # asc diagonal win check_2
                if (board[2][3] == 1 or board[2][3] == 2) and (board[1][4] == 1 or board[1][4] == 2) and (
                        board[0][5] == 1 or board[0][5] == 2):
                    draw_asc_diagonal_2()
                    return True

                # desc diagonal win chek_2
                if (board[0][3] == 1 or board[0][3] == 2) and (board[1][4] == 1 or board[1][4] == 2) and (
                        board[2][5] == 1 or board[2][5] == 2):
                    draw_desc_diagonal_2()
                    return True

        # //////////////////////////////////////////////////////////////////////////////////////////////////////////////
        # STRUIRE LEGATURA DINTRE TABLA 1 CATRE TABLA 2 PENTRU DIAGONALA ASCENDENTA A TABLEI 1
        # asc diagonal win check_1
        if (board[2][0] == 1 or board[2][0] == 2) and (board[1][1] == 1 or board[1][1] == 2) and (
                board[0][2] == 1 or board[0][2] == 2):
            draw_asc_diagonal_1()
            board[0][0] = board[0][1] = board[1][0] = board[1][2] = board[2][1] = board[2][2] = 3
            # vertical win check_2
            for col in range(3, BOARD_COLS):
                if (board[0][col] == 1 or board[0][col] == 2) and (board[1][col] == 1 or board[1][col] == 2) and (
                        board[2][col] == 1 or board[2][col] == 2):
                    draw_vertical_winning_line(col)
                    return True

            # horizontal win check_2
            for row in range(BOARD_ROWS):
                if (board[row][3] == 1 or board[row][3] == 2) and (board[row][4] == 1 or board[row][4] == 2) and (
                        board[row][5] == 1 or board[row][5] == 2):
                    draw_horizontal_winning_line_2(row)
                    return True

            # asc diagonal win check_2
            if (board[2][3] == 1 or board[2][3] == 2) and (board[1][4] == 1 or board[1][4] == 2) and (
                    board[0][5] == 1 or board[0][5] == 2):
                draw_asc_diagonal_2()
                return True

            # desc diagonal win chek_2
            if (board[0][3] == 1 or board[0][3] == 2) and (board[1][4] == 1 or board[1][4] == 2) and (
                    board[2][5] == 1 or board[2][5] == 2):
                draw_desc_diagonal_2()
                return True

        # //////////////////////////////////////////////////////////////////////////////////////////////////////////////
        # CONSTRUIRE LEGATURA DINTRE TABLA 1 CATRE TABLA 2 PENTRU DIAGONALA DESCENDENTA A TABLEI 1
        # desc diagonal win chek_1
        if (board[0][0] == 1 or board[0][0] == 2) and (board[1][1] == 1 or board[1][1] == 2) and (
                board[2][2] == 1 or board[2][2] == 2):
            draw_desc_diagonal_1()
            board[0][1] = board[0][2] = board[1][0] = board[1][2] = board[2][0] = board[2][1] = 3
            # vertical win check_2
            for col in range(3, BOARD_COLS):
                if (board[0][col] == 1 or board[0][col] == 2) and (board[1][col] == 1 or board[1][col] == 2) and (
                        board[2][col] == 1 or board[2][col] == 2):
                    draw_vertical_winning_line(col)
                    return True

            # horizontal win check_2
            for row in range(BOARD_ROWS):
                if (board[row][3] == 1 or board[row][3] == 2) and (board[row][4] == 1 or board[row][4] == 2) and (
                        board[row][5] == 1 or board[row][5] == 2):
                    draw_horizontal_winning_line_2(row)
                    return True

                # asc diagonal win check_2
                if (board[2][3] == 1 or board[2][3] == 2) and (board[1][4] == 1 or board[1][4] == 2) and (
                        board[0][5] == 1 or board[0][5] == 2):
                    draw_asc_diagonal_2()
                    return True

                # desc diagonal win chek_2
                if (board[0][3] == 1 or board[0][3] == 2) and (board[1][4] == 1 or board[1][4] == 2) and (
                        board[2][5] == 1 or board[2][5] == 2):
                    draw_desc_diagonal_2()
                    return True

        # //////////////////////////////////////////////////////////////////////////////////////////////////////
        # CONSTRUIRE LEGATURA DINTRE TABLA 2 CATRE TABLA 1 PENTRU LINIILE VERTICALE ALE TABLEI 2
        # vertical win check_2
        for col in range(3, BOARD_COLS):
            if (board[0][col] == 1 or board[0][col] == 2) and (board[1][col] == 1 or board[1][col] == 2) and (
                    board[2][col] == 1 or board[2][col] == 2):
                draw_vertical_winning_line(col)
                if col == 3:
                    board[0][4] = board[0][5] = board[1][4] = board[1][5] = board[2][4] = board[2][5] = 3
                elif col == 4:
                    board[0][3] = board[0][5] = board[1][3] = board[1][5] = board[2][3] = board[2][5] = 3
                elif col == 5:
                    board[0][3] = board[0][4] = board[1][3] = board[1][4] = board[2][3] = board[2][4] = 3
                # vertical win check_1
                for col in range(BOARD_COLS - 3):
                    if (board[0][col] == 1 or board[0][col] == 2) and (
                            board[1][col] == 1 or board[1][col] == 2) and (
                            board[2][col] == 1 or board[2][col] == 2):
                        draw_vertical_winning_line(col)
                        return True

                # horizontal win check_1
                for row in range(BOARD_ROWS):
                    if (board[row][0] == 1 or board[row][0] == 2) and (
                            board[row][1] == 1 or board[row][1] == 2) and (
                            board[row][2] == 1 or board[row][2] == 2):
                        draw_horizontal_winning_line_1(row)
                        return True

                # asc diagonal win check_1
                if (board[2][0] == 1 or board[2][0] == 2) and (board[1][1] == 1 or board[1][1] == 2) and (
                        board[0][2] == 1 or board[0][2] == 2):
                    draw_asc_diagonal_1()
                    return True
        # //////////////////////////////////////////////////////////////////////////////////////////////////////////////
        # CONSTRUIRE LEGATURA DINTRE TABLA 2 CATRE TABLA 1 PENTRU LINIILE ORIZONTALE ALE TABLEI 2
        # horizontal win check_2
        for row in range(BOARD_ROWS):
            if (board[row][3] == 1 or board[row][3] == 2) and (board[row][4] == 1 or board[row][4] == 2) and (
                    board[row][5] == 1 or board[row][5] == 2):
                draw_horizontal_winning_line_2(row)
                if row == 0:
                    board[1][3] = board[1][4] = board[1][5] = board[2][3] = board[2][4] = board[2][5] = 3
                elif row == 1:
                    board[0][3] = board[0][4] = board[0][5] = board[2][3] = board[2][4] = board[2][5] = 3
                elif row == 2:
                    board[0][3] = board[0][4] = board[0][5] = board[1][3] = board[1][4] = board[1][5] = 3

                # vertical win check_1
                for col in range(BOARD_COLS - 3):
                    if (board[0][col] == 1 or board[0][col] == 2) and (board[1][col] == 1 or board[1][col] == 2) and (
                            board[2][col] == 1 or board[2][col] == 2):
                        draw_vertical_winning_line(col)
                        return True

                # horizontal win check_1
                for row in range(BOARD_ROWS):
                    if (board[row][0] == 1 or board[row][0] == 2) and (board[row][1] == 1 or board[row][1] == 2) and (
                            board[row][2] == 1 or board[row][2] == 2):
                        draw_horizontal_winning_line_1(row)
                        return True

                # asc diagonal win check_1
                if (board[2][0] == 1 or board[2][0] == 2) and (board[1][1] == 1 or board[1][1] == 2) and (
                        board[0][2] == 1 or board[0][2] == 2):
                    draw_asc_diagonal_1()
                    return True

                # desc diagonal win chek_1
                if (board[0][0] == 1 or board[0][0] == 2) and (board[1][1] == 1 or board[1][1] == 2) and (
                        board[2][2] == 1 or board[2][2] == 2):
                    draw_desc_diagonal_1()
                    return True
                # vertical win check_2
                for col in range(3, BOARD_COLS):
                    if (board[0][col] == 1 or board[0][col] == 2) and (board[1][col] == 1 or board[1][col] == 2) and (
                            board[2][col] == 1 or board[2][col] == 2):
                        draw_vertical_winning_line(col)
                        return True
        # //////////////////////////////////////////////////////////////////////////////////////////////////////////////
        # CONSTRUIRE LEGATURA DINTRE TABLA 2 CATRE TABLA 2 PENTRU DIAGONALA ASCENDENTA A TABLEI 2
        # asc diagonal win check_2
        if (board[2][3] == 1 or board[2][3] == 2) and (board[1][4] == 1 or board[1][4] == 2) and (
                board[0][5] == 1 or board[0][5] == 2):
            draw_asc_diagonal_2()
            board[0][3] = board[0][4] = board[1][3] = board[1][5] = board[2][4] = board[2][5] = 3

            # vertical win check_1
            for col in range(BOARD_COLS - 3):
                if (board[0][col] == 1 or board[0][col] == 2) and (board[1][col] == 1 or board[1][col] == 2) and (
                        board[2][col] == 1 or board[2][col] == 2):
                    draw_vertical_winning_line(col)
                    return True

            # horizontal win check_2
            for row in range(BOARD_ROWS):
                if (board[row][0] == 1 or board[row][0] == 2) and (board[row][1] == 1 or board[row][1] == 2) and (
                        board[row][2] == 1 or board[row][2] == 2):
                    draw_horizontal_winning_line_2(row)
                    return True

            # asc diagonal win check_1
            if (board[2][0] == 1 or board[2][0] == 2) and (board[1][1] == 1 or board[1][1] == 2) and (
                    board[0][2] == 1 or board[0][2] == 2):
                draw_asc_diagonal_1()
                return True

            # desc diagonal win chek_1
            if (board[0][0] == 1 or board[0][0] == 2) and (board[1][1] == 1 or board[1][1] == 2) and (
                    board[2][2] == 1 or board[2][2] == 2):
                draw_desc_diagonal_1()
                return True

        # //////////////////////////////////////////////////////////////////////////////////////////////////////////////
        # CONSTRUIRE LEGATURA DINTRE TABLA 2 CATRE TABLA 1 PENTRU DIAGONALA DESCENDENTA A TABLEI 2
        # desc diagonal win chek_2
        if (board[0][3] == 1 or board[0][3] == 2) and (board[1][4] == 1 or board[1][4] == 2) and (
                board[2][5] == 1 or board[2][5] == 2):
            draw_desc_diagonal_2()
            board[0][4] = board[0][5] = board[1][3] = board[1][5] = board[2][3] = board[2][4] = 3
            # vertical win check_1
            for col in range(BOARD_COLS - 3):
                if (board[0][col] == 1 or board[0][col] == 2) and (
                        board[1][col] == 1 or board[1][col] == 2) and (
                        board[2][col] == 1 or board[2][col] == 2):
                    draw_vertical_winning_line(col)
                    return True

            # horizontal win check_1
            for row in range(BOARD_ROWS):
                if (board[row][0] == 1 or board[row][0] == 2) and (
                        board[row][1] == 1 or board[row][1] == 2) and (
                        board[row][2] == 1 or board[row][2] == 2):
                    draw_horizontal_winning_line_1(row)
                    return True

            # asc diagonal win check_1
            if (board[2][0] == 1 or board[2][0] == 2) and (board[1][1] == 1 or board[1][1] == 2) and (
                    board[0][2] == 1 or board[0][2] == 2):
                draw_asc_diagonal_1()
                return True

            # desc diagonal win chek_1
            if (board[0][0] == 1 or board[0][0] == 2) and (board[1][1] == 1 or board[1][1] == 2) and (
                    board[2][2] == 1 or board[2][2] == 2):
                draw_desc_diagonal_1()
                return True

    return False


def draw_vertical_winning_line(col):
    posX = col * SQUARE_SIZE + SQUARE_SIZE // 2

    pygame.draw.line(screen, RED, (posX, 15), (posX, HEIGHT - 15), LINE_WIDTH)


def draw_horizontal_winning_line_1(row):
    posY = row * SQUARE_SIZE + SQUARE_SIZE // 2

    pygame.draw.line(screen, RED, (15, posY), (WIDTH / 2 - 15, posY), WIN_LINE_WIDTH)


def draw_horizontal_winning_line_2(row):
    posY = row * SQUARE_SIZE + SQUARE_SIZE // 2

    pygame.draw.line(screen, RED, (WIDTH / 2 + 15, posY), (WIDTH - 15, posY), WIN_LINE_WIDTH)


def draw_asc_diagonal_1():
    pygame.draw.line(screen, RED, (15, HEIGHT - 15), (WIDTH / 2 - 15, 15), WIN_LINE_WIDTH)


def draw_desc_diagonal_1():
    pygame.draw.line(screen, RED, (15, 15), (WIDTH / 2 - 15, HEIGHT - 15), WIN_LINE_WIDTH)


def draw_asc_diagonal_2():
    pygame.draw.line(screen, RED, (WIDTH / 2 + 15, HEIGHT - 15), (WIDTH - 15, 15), WIN_LINE_WIDTH)


def draw_desc_diagonal_2():
    pygame.draw.line(screen, RED, (15 + 3 * SQUARE_SIZE, 15), (WIDTH - 15, HEIGHT - 15), WIN_LINE_WIDTH)


def restart():
    screen.fill(BG_COLOR)
    draw_lines()

    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = 0


def displayWinner(player):
    for table in (0, 1):
        if table_winner_displayed[table] is not True and (game_over or is_table_full(table)):
            table_winner_displayed[table] = True

            mesaj = Arial.render(f'Player {player % 2 + 1} won', False, BLACK)
            coords = [
                (WIDTH / 2 - mesaj.get_width() - LINE_WIDTH * 2, HEIGHT + 2 * LINE_WIDTH),
                (WIDTH / 2 + LINE_WIDTH * 2, HEIGHT + 2 * LINE_WIDTH)
            ]
            screen.blit(mesaj, coords[table])


draw_lines()

# ---------
# VARIABILE
# ---------
player = 1
game_over = False

# Niciun jucator nu a castigat inca
table_winner_displayed = [False, False]

set_caption(player)

# --------
# PROGRAMUL PRINCIPAL
# --------
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:

            mouseX = event.pos[0]  # x
            mouseY = event.pos[1]  # y

            clicked_row = int(mouseY // SQUARE_SIZE)
            clicked_col = int(mouseX // SQUARE_SIZE)

            if available_square(clicked_row, clicked_col):

                mark_square(clicked_row, clicked_col, player)

                if check_win():
                    game_over = True

                displayWinner(player)

                player = player % 2 + 1

                set_caption(player)

                draw_figures()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart()
                player = 1
                set_caption(player)
                table_winner_displayed = [False, False]
                game_over = False

    pygame.display.update()
