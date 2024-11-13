import pygame, sys

pygame.init()

size = 800 # screen size

pygame.display.set_caption("Tic Tac Toe")
screen = pygame.display.set_mode((size, size))

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)

fields = []
for y in range(3):
    for x in range(3):
        fields.append(pygame.Rect((1 + x) / 5 * size, (1 + y) / 5 * size, 1 / 5 * size, 1 / 5 * size))

dx = int(1 / 25 * size)
dy = int(1 / 35 * size)
font = pygame.font.SysFont("Lemon Milk", int(1 / 4 * size))
X = font.render('X', False, red)
O = font.render('O', False, blue)

win_font = pygame.font.SysFont("Lemon Milk", int(1 / 8 * size))
Xwins = win_font.render('X WINS!', False, red)
Owins = win_font.render('O WINS!', False, blue)
Draw = win_font.render('DRAW!', False, green)

wins = ((0, 1, 2), (0, 3, 6), (2, 5, 8), (6, 7, 8), (3, 4, 5), (1, 4, 7), (0, 4, 8), (2, 4, 6))

turn = True
markedX = []
markedO = []
finished = False

board = [None] * 9

def reset_game():
    global turn, markedX, markedO, finished, board
    turn = True
    markedX = []
    markedO = []
    finished = False
    board = [None] * 9
    screen.fill(black)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                reset_game()

    screen.fill(black)
    pygame.draw.line(screen, white, (1 / 5 * size, 2 / 5 * size), (4 / 5 * size, 2 / 5 * size), width=10)
    pygame.draw.line(screen, white, (1 / 5 * size, 3 / 5 * size), (4 / 5 * size, 3 / 5 * size), width=10)
    pygame.draw.line(screen, white, (2 / 5 * size, 1 / 5 * size), (2 / 5 * size, 4 / 5 * size), width=10)
    pygame.draw.line(screen, white, (3 / 5 * size, 1 / 5 * size), (3 / 5 * size, 4 / 5 * size), width=10)

    for i in range(9):
        if board[i] == 'X':
            screen.blit(X, ((1 + i % 3) / 5 * size + dx, (1 + i // 3) / 5 * size + dy))
        elif board[i] == 'O':
            screen.blit(O, ((1 + i % 3) / 5 * size + dx, (1 + i // 3) / 5 * size + dy))

    if not finished:
        mouse = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            for i in range(9):
                if fields[i].collidepoint(mouse) and board[i] is None:
                    if turn:
                        board[i] = 'X'
                        markedX.append(i)
                        turn = False
                    else:
                        board[i] = 'O'
                        markedO.append(i)
                        turn = True

                    screen.fill(black)
                    pygame.draw.line(screen, white, (1 / 5 * size, 2 / 5 * size), (4 / 5 * size, 2 / 5 * size), width=10)
                    pygame.draw.line(screen, white, (1 / 5 * size, 3 / 5 * size), (4 / 5 * size, 3 / 5 * size), width=10)
                    pygame.draw.line(screen, white, (2 / 5 * size, 1 / 5 * size), (2 / 5 * size, 4 / 5 * size), width=10)
                    pygame.draw.line(screen, white, (3 / 5 * size, 1 / 5 * size), (3 / 5 * size, 4 / 5 * size), width=10)

                    for j in range(9):
                        if board[j] == 'X':
                            screen.blit(X, ((1 + j % 3) / 5 * size + dx, (1 + j // 3) / 5 * size + dy))
                        elif board[j] == 'O':
                            screen.blit(O, ((1 + j % 3) / 5 * size + dx, (1 + j // 3) / 5 * size + dy))

                    pygame.display.update()

            # Sprawdzanie zwycięstwa lub remisu
            for win in wins:
                if all(pos in markedX for pos in win):
                    screen.blit(Xwins, (size / 3, size / 16))
                    finished = True
                if all(pos in markedO for pos in win):
                    screen.blit(Owins, (size / 3, size / 16))
                    finished = True

            if not finished and all(space is not None for space in board):
                screen.blit(Draw, (size / 3, size / 16))
                finished = True

    if finished:
        pygame.display.update()  # Wyświetlenie komunikatu o wyniku
        while finished:  # Czekanie na wciśnięcie Enter
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    reset_game()
                    finished = False  # Pozwala na kontynuowanie gry

    pygame.display.update()