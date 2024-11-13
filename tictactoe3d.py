import pygame
import sys

pygame.init()

# Stałe
SCREEN_SIZE = 800
LINE_WIDTH = int(1 / 100 * SCREEN_SIZE)  # Szerokość linii jako proporcja ekranowego rozmiaru
FIELD_SIZE = SCREEN_SIZE // 13  # Rozmiar pola jako proporcja ekranowego rozmiaru
FONT_SIZE = int(SCREEN_SIZE / 10)
FONT_COLOR = (255, 255, 255)
CUBE = pygame.image.load("szescian.png")
CUBE = pygame.transform.scale(CUBE, (3/13 * SCREEN_SIZE, 3/13 * SCREEN_SIZE))

# Kolory
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Ustawienia gry
pygame.display.set_caption("Tic Tac Toe 3D")
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))

# Ustawienia czcionki
main_font = pygame.font.SysFont("Lemon Milk", FONT_SIZE)
win_font = pygame.font.SysFont("Lemon Milk", int(SCREEN_SIZE / 8))

# Rysunki dla X, O, Δ oraz komunikaty końcowe
X_SURFACE = main_font.render('X', True, RED)
O_SURFACE = main_font.render('O', True, BLUE)
Δ_SURFACE = main_font.render('Δ', True, YELLOW)
X_WINS_TEXT = win_font.render('X WINS!', True, RED)
O_WINS_TEXT = win_font.render('O WINS!', True, BLUE)
Y_WINS_TEXT = win_font.render('Δ WINS!', True, YELLOW)
DRAW_TEXT = win_font.render('DRAW!', True, GREEN)

# Linie zwycięstwa
WINNING_COMBINATIONS = []

# Straight lines
for i in range(0, 27, 3):
    WINNING_COMBINATIONS.append((i, i+1, i+2))
for i in (0, 1, 2, 9, 10, 11, 18, 19, 20):
    WINNING_COMBINATIONS.append((i, i+3, i+6))
for i in range(0, 9):
    WINNING_COMBINATIONS.append((i, i+9, i+18))

# Plane diagonals
# XY plane diagonals
for z in (0, 9, 18):
    WINNING_COMBINATIONS.append((z, z + 4, z + 8))  # \ diagonal
    WINNING_COMBINATIONS.append((z + 2, z + 4, z + 6))  # / diagonal

# XZ plane diagonals
for y in range(0, 9, 3):
    WINNING_COMBINATIONS.append((y, y + 10, y + 20))  # \ diagonal
    WINNING_COMBINATIONS.append((y + 2, y + 10, y + 18))  # / diagonal

# YZ plane diagonals
for x in range(3):
    WINNING_COMBINATIONS.append((x, x + 12, x + 24))  # \ diagonal
    WINNING_COMBINATIONS.append((x + 6, x + 12, x + 18))  # / diagonal

# Cross-plane diagonals
WINNING_COMBINATIONS.append((0, 13, 26))
WINNING_COMBINATIONS.append((2, 13, 24))
WINNING_COMBINATIONS.append((18, 13, 8))
WINNING_COMBINATIONS.append((20, 13, 6))


# Globalne zmienne gry
turn = 0  # True dla gracza, False dla komputera
finished = False
board = [None] * 27

# Offsety dla wyśrodkowania symboli
dx = int(1 / 80 * SCREEN_SIZE)
dy = int(1 / 110 * SCREEN_SIZE)


def create_board_fields():
    """Tworzy pola na planszy."""
    fields = []
    for y in range(1, 12):
        for x in range(1, 12):
            if x % 4 != 0 and y in range(3, 6):
                field = pygame.Rect(
                    x / 13 * SCREEN_SIZE,
                    y / 13 * SCREEN_SIZE,
                    FIELD_SIZE,
                    FIELD_SIZE)
                fields.append(field)
    return fields


def reset_game():
    """Resetuje stan gry do początkowych wartości."""
    global board, finished, turn
    turn = 0
    finished = False
    board = [None] * 27
    draw_board()


def start_screen():
    """Wyświetla ekran początkowy z opcją wyboru, kto zaczyna grę."""
    global player_turn
    screen.fill(BLACK)
    font = pygame.font.SysFont("Lemon Milk", int(SCREEN_SIZE / 12))
    name = font.render("Welcome in TIC TAC TOE 3D", True, FONT_COLOR)
    screen.blit(name, (SCREEN_SIZE / 10, SCREEN_SIZE / 3))

    text = font.render("Press 1 to start", True, RED)
    screen.blit(text, (SCREEN_SIZE / 4, SCREEN_SIZE / 2))

    pygame.display.update()

    start = False
    while start is False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    start = True


def draw_board():
    """Rysuje planszę i elementy X i O."""
    screen.fill(BLACK)

    # Linie planszy
    for x in (2, 3, 6, 7, 10, 11):
        pygame.draw.line(screen, WHITE, (x/13 * SCREEN_SIZE, 3/13 * SCREEN_SIZE),
                         (x/13 * SCREEN_SIZE, 6/13 * SCREEN_SIZE), LINE_WIDTH)

    for y in (4, 5):
        for x in (1, 5, 9):
            pygame.draw.line(screen, WHITE, (x / 13 * SCREEN_SIZE, y / 13 * SCREEN_SIZE),
                             ((x+3) / 13 * SCREEN_SIZE, y / 13 * SCREEN_SIZE), LINE_WIDTH)

    # Numery pod planszami
    one = main_font.render("1", True, FONT_COLOR)
    two = main_font.render("2", True, FONT_COLOR)
    three = main_font.render("3", True, FONT_COLOR)
    screen.blit(one, (2/13 * SCREEN_SIZE + 2*dx, 6/13 * SCREEN_SIZE))
    screen.blit(two, (6/13 * SCREEN_SIZE + 2*dx, 6/13 * SCREEN_SIZE))
    screen.blit(three, (10/13 * SCREEN_SIZE + 2*dx, 6/13 * SCREEN_SIZE))

    # Rysunek kostki
    screen.blit(CUBE, [5/13 * SCREEN_SIZE, 8/13 * SCREEN_SIZE])

    # Wyświetlanie symboli
    for i in range(27):
        if board[i] == 'X':
            screen.blit(X_SURFACE, (fields[i].x + dx, fields[i].y + dy))
        elif board[i] == 'O':
            screen.blit(O_SURFACE, (fields[i].x + dx, fields[i].y + dy))
        elif board[i] == 'Δ':
            screen.blit(Δ_SURFACE, (fields[i].x + dx, fields[i].y + dy))

    pygame.display.update()


def is_moves_left(board):
    """Sprawdza, czy są jeszcze możliwe ruchy."""
    return any(spot is None for spot in board)


def check_for_winner():
    """Sprawdza, czy ktoś wygrał lub czy jest remis."""
    global finished

    # Sprawdzanie zwycięstwa
    for combo in WINNING_COMBINATIONS:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] and board[combo[0]] is not None:
            if board[combo[0]] == 'X':
                screen.blit(X_WINS_TEXT, (SCREEN_SIZE / 3, SCREEN_SIZE / 16))
            elif board[combo[0]] == 'O':
                screen.blit(O_WINS_TEXT, (SCREEN_SIZE / 3, SCREEN_SIZE / 16))
            else:
                screen.blit(Y_WINS_TEXT, (SCREEN_SIZE / 3, SCREEN_SIZE / 16))
            finished = True
            return

    # Sprawdzanie remisu
    if not is_moves_left(board):
        screen.blit(DRAW_TEXT, (SCREEN_SIZE / 3, SCREEN_SIZE / 16))
        finished = True


def main():
    global fields, finished, turn

    # Przygotowanie planszy
    fields = create_board_fields()
    start_screen()
    reset_game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not finished:
                x, y = event.pos
                for i, field in enumerate(fields):
                    if field.collidepoint(x, y) and board[i] is None:
                        if turn == 0:
                            board[i] = 'X'
                        if turn == 1:
                            board[i] = 'O'
                        if turn == 2:
                            board[i] = 'Δ'
                        turn = (turn+1)%3
                        draw_board()
                        check_for_winner()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if finished:
                    reset_game()

        pygame.display.update()


if __name__ == "__main__":
    main()
