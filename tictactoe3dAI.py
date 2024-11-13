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
CUBE = pygame.transform.scale(CUBE, (int(3/13 * SCREEN_SIZE), int(3/13 * SCREEN_SIZE)))

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
LINE = ['X', 'O', 'Δ']

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
for z in (0, 9, 18):
    WINNING_COMBINATIONS.append((z, z + 4, z + 8))
    WINNING_COMBINATIONS.append((z + 2, z + 4, z + 6))

for y in range(0, 9, 3):
    WINNING_COMBINATIONS.append((y, y + 10, y + 20))
    WINNING_COMBINATIONS.append((y + 2, y + 10, y + 18))

for x in range(3):
    WINNING_COMBINATIONS.append((x, x + 12, x + 24))
    WINNING_COMBINATIONS.append((x + 6, x + 12, x + 18))

# Cross-plane diagonals
WINNING_COMBINATIONS.append((0, 13, 26))
WINNING_COMBINATIONS.append((2, 13, 24))
WINNING_COMBINATIONS.append((18, 13, 8))
WINNING_COMBINATIONS.append((20, 13, 6))

# Zmienna określająca kolejność gracza
player_turn = None

# Globalne zmienne gry
turn = 0  # Zaczyna od gracza X
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
    font = pygame.font.SysFont("Lemon Milk", int(SCREEN_SIZE / 10))
    text = font.render("Choose your turn in game:", True, FONT_COLOR)
    screen.blit(text, (SCREEN_SIZE / 12, SCREEN_SIZE / 4))

    text1 = font.render("Press 1 for X", True, RED)
    text2 = font.render("Press 2 for O", True, BLUE)
    text3 = font.render("Press 3 for Δ", True, YELLOW)
    screen.blit(text1, (SCREEN_SIZE / 6, SCREEN_SIZE / 2 - 100))
    screen.blit(text2, (SCREEN_SIZE / 6, SCREEN_SIZE / 2))
    screen.blit(text3, (SCREEN_SIZE / 6, SCREEN_SIZE / 2 + 100))

    pygame.display.update()

    while player_turn is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    player_turn = 0  # Gracz gra jako pierwszy
                elif event.key == pygame.K_2:
                    player_turn = 1  # Gracz gra jako drugi
                elif event.key == pygame.K_3:
                    player_turn = 2  # Gracz gra jako trzeci


def draw_board():
    """Rysuje planszę i elementy X, O oraz Δ."""
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


def evaluate(board):
    """Ocena stanu planszy. Zwraca +10 dla X, -10 dla O oraz Δ, 0 dla remisu."""
    for combo in WINNING_COMBINATIONS:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] and board[combo[0]] is not None:
            if board[combo[0]] == 'X':
                return 10
            elif board[combo[0]] == 'O' or board[combo[0]] == 'Δ':
                return -10
    return 0

def is_moves_left(board):
    """Sprawdza, czy są jeszcze możliwe ruchy."""
    return any(spot is None for spot in board)


def minimax(board, depth, turn, max_depth=4, alpha=-float('inf'), beta=float('inf')):
    """Algorytm Minimax z optymalizacją alfa-beta pruning i ograniczeniem głębokości."""
    score = evaluate(board)

    # Jeśli ktoś wygrał
    if score == 10 or score == -10:
        return score - depth if score > 0 else score + depth

    # Remis lub osiągnięcie maksymalnej głębokości
    if not is_moves_left(board) or depth >= max_depth:
        return score

    if turn == 0:  # Maksymalizujący gracz ('X')
        best = -1000
        for i in range(27):
            if board[i] is None:
                board[i] = 'X'
                value = minimax(board, depth + 1, (turn + 1) % 3, max_depth, alpha, beta)
                best = max(best, value)
                board[i] = None
                alpha = max(alpha, best)
                if beta <= alpha:
                    break  # Pruning
        return best
    else:  # Minimalizujący gracze ('O' lub 'Δ')
        best = 1000
        for i in range(27):
            if board[i] is None:
                board[i] = LINE[turn]
                value = minimax(board, depth + 1, (turn + 1) % 3, max_depth, alpha, beta)
                best = min(best, value)
                board[i] = None
                beta = min(beta, best)
                if beta <= alpha:
                    break  # Pruning
        return best

def find_best_move(board, turn, max_depth=4):
    """Znajduje najlepszy możliwy ruch dla aktualnego gracza z ograniczeniem głębokości."""
    best_value = -1000 if turn == 0 else 1000
    best_move = -1
    for i in range(27):
        if board[i] is None:
            board[i] = LINE[turn]
            move_value = minimax(board, 0, (turn + 1) % 3, max_depth)
            board[i] = None
            if (turn == 0 and move_value > best_value) or (turn != 0 and move_value < best_value):
                best_move = i
                best_value = move_value
    return best_move


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
    """Główna pętla gry."""
    global turn, finished, winner_displayed
    start_screen()
    draw_board()

    winner_displayed = False

    while True:
        # Obsługa zdarzeń wewnątrz pętli for
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Resetowanie gry po jej zakończeniu
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                reset_game()
                winner_displayed = False  # Wyłącza wyświetlanie wyniku
                continue  # Przechodzi do następnego obiegu pętli po resetowaniu

            # Ruch gracza tylko jeśli gra się nie skończyła
            if player_turn == turn and not finished:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    for i, field in enumerate(fields):
                        if field.collidepoint(mouse_x, mouse_y) and board[i] is None:
                            board[i] = LINE[turn]
                            draw_board()
                            turn = (turn + 1) % 3
                            break

        # Ruch komputera
        if not finished and player_turn != turn:
            move = find_best_move(board, turn)
            if move != -1:
                board[move] = LINE[turn]
                draw_board()
                turn = (turn + 1) % 3

        # Sprawdzenie wyniku gry
        check_for_winner()

        # Wyświetlanie wyniku po zakończeniu gry
        if finished and not winner_displayed:
            winner_displayed = True

        pygame.display.update()

fields = create_board_fields()
main()