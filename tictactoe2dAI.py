import pygame
import sys

# Inicjalizacja Pygame
pygame.init()

# Stałe
SCREEN_SIZE = 800
LINE_WIDTH = int(1 / 50 * SCREEN_SIZE)  # Szerokość linii jako proporcja ekranowego rozmiaru
FIELD_SIZE = SCREEN_SIZE // 5  # Rozmiar pola jako proporcja ekranowego rozmiaru
FONT_SIZE = int(SCREEN_SIZE / 4)
FONT_COLOR = (255, 255, 255)

# Kolory
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Ustawienia gry
pygame.display.set_caption("Tic Tac Toe")
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))

# Ustawienia czcionki
main_font = pygame.font.SysFont("Lemon Milk", FONT_SIZE)
win_font = pygame.font.SysFont("Lemon Milk", int(SCREEN_SIZE / 8))

# Rysunki dla X, O oraz komunikaty końcowe
X_SURFACE = main_font.render('X', True, RED)
O_SURFACE = main_font.render('O', True, BLUE)
X_WINS_TEXT = win_font.render('X WINS!', True, RED)
O_WINS_TEXT = win_font.render('O WINS!', True, BLUE)
DRAW_TEXT = win_font.render('DRAW!', True, GREEN)

# Linie zwycięstwa
WINNING_COMBINATIONS = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Wiersze
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Kolumny
    (0, 4, 8), (2, 4, 6)              # Przekątne
)

# Zmienna określająca kto zaczyna grę
player_starts = None

# Globalne zmienne gry
turn = True  # True dla gracza, False dla komputera
finished = False
board = [None] * 9

# Offsety dla wyśrodkowania X i O
dx = int(1 / 25 * SCREEN_SIZE)
dy = int(1 / 35 * SCREEN_SIZE)


def create_board_fields():
    """Tworzy pola na planszy."""
    fields = []
    for y in range(3):
        for x in range(3):
            field = pygame.Rect(
                (1 + x) / 5 * SCREEN_SIZE,
                (1 + y) / 5 * SCREEN_SIZE,
                FIELD_SIZE,
                FIELD_SIZE)
            fields.append(field)
    return fields


def reset_game():
    """Resetuje stan gry do początkowych wartości."""
    global board, finished, turn
    turn = True if player_starts else False
    finished = False
    board = [None] * 9
    draw_board()


def start_screen():
    """Wyświetla ekran początkowy z opcją wyboru, kto zaczyna grę."""
    global player_starts
    screen.fill(BLACK)
    font = pygame.font.SysFont("Lemon Milk", int(SCREEN_SIZE / 10))
    text = font.render("Choose who starts:", True, FONT_COLOR)
    screen.blit(text, (SCREEN_SIZE / 6, SCREEN_SIZE / 3))

    text_X = font.render("Press X for Player", True, RED)
    text_O = font.render("Press O for Computer", True, BLUE)
    screen.blit(text_X, (SCREEN_SIZE / 6, SCREEN_SIZE / 2))
    screen.blit(text_O, (SCREEN_SIZE / 6, SCREEN_SIZE / 2 + 100))

    pygame.display.update()

    while player_starts is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    player_starts = True  # Gracz zaczyna jako X
                elif event.key == pygame.K_o:
                    player_starts = False  # Komputer zaczyna jako O


def evaluate(board):
    """Ocena stanu planszy. Zwraca +10 dla X, -10 dla O, 0 dla remisu."""
    for combo in WINNING_COMBINATIONS:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] and board[combo[0]] is not None:
            if board[combo[0]] == 'X':
                return 10
            elif board[combo[0]] == 'O':
                return -10
    return 0


def is_moves_left(board):
    """Sprawdza, czy są jeszcze możliwe ruchy."""
    return any(spot is None for spot in board)


def minimax(board, depth, is_maximizing):
    """Algorytm Minimax do oceny ruchów."""
    score = evaluate(board)

    # Jeśli ktoś wygrał
    if score == 10 or score == -10:
        return score - depth if score > 0 else score + depth

    # Remis
    if not is_moves_left(board):
        return 0

    if is_maximizing:
        best = -1000
        for i in range(9):
            if board[i] is None:
                board[i] = 'X'
                best = max(best, minimax(board, depth + 1, False))
                board[i] = None
        return best
    else:
        best = 1000
        for i in range(9):
            if board[i] is None:
                board[i] = 'O'
                current_score = evaluate(board)
                if current_score == -10:
                    board[i] = None
                    return current_score
                best = min(best, minimax(board, depth + 1, True))
                board[i] = None
        return best


def find_best_move(board):
    """Znajduje najlepszy możliwy ruch dla gracza O."""
    best_value = 1000
    best_move = -1
    for i in range(9):
        if board[i] is None:
            board[i] = 'O'
            move_value = minimax(board, 0, True)
            board[i] = None
            if move_value < best_value:
                best_move = i
                best_value = move_value
    return best_move


def draw_board():
    """Rysuje planszę i elementy X i O."""
    screen.fill(BLACK)

    # Linie planszy
    pygame.draw.line(screen, WHITE, (1 / 5 * SCREEN_SIZE, 2 / 5 * SCREEN_SIZE),
                     (4 / 5 * SCREEN_SIZE, 2 / 5 * SCREEN_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, WHITE, (1 / 5 * SCREEN_SIZE, 3 / 5 * SCREEN_SIZE),
                     (4 / 5 * SCREEN_SIZE, 3 / 5 * SCREEN_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, WHITE, (2 / 5 * SCREEN_SIZE, 1 / 5 * SCREEN_SIZE),
                     (2 / 5 * SCREEN_SIZE, 4 / 5 * SCREEN_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, WHITE, (3 / 5 * SCREEN_SIZE, 1 / 5 * SCREEN_SIZE),
                     (3 / 5 * SCREEN_SIZE, 4 / 5 * SCREEN_SIZE), LINE_WIDTH)

    # Wyświetlanie X i O
    for i in range(9):
        if board[i] == 'X':
            screen.blit(X_SURFACE, (fields[i].x + dx, fields[i].y + dy))
        elif board[i] == 'O':
            screen.blit(O_SURFACE, (fields[i].x + dx, fields[i].y + dy))

    pygame.display.update()


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
            finished = True
            return

    # Sprawdzanie remisu
    if not is_moves_left(board):
        screen.blit(DRAW_TEXT, (SCREEN_SIZE / 3, SCREEN_SIZE / 16))
        finished = True


def main():
    global fields, finished, turn, player_starts

    # Przygotowanie planszy
    fields = create_board_fields()
    start_screen()
    reset_game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not finished and turn:
                x, y = event.pos
                for i, field in enumerate(fields):
                    if field.collidepoint(x, y) and board[i] is None:
                        board[i] = 'X'
                        turn = False
                        draw_board()
                        check_for_winner()
                        break

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if finished:
                    reset_game()

        if not finished and not turn:  # Komputer robi ruch
            pygame.time.delay(500)  # Krótka przerwa dla lepszej widoczności
            move = find_best_move(board)
            if move != -1:
                board[move] = 'O'
                turn = True
                draw_board()
                check_for_winner()

        pygame.display.update()


if __name__ == "__main__":
    main()