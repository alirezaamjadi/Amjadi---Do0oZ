import pygame
import sys
import random

pygame.init()

# Colors
RED = (230, 57, 70)
BLUE = (29, 78, 137)
JADE = (0, 168, 107)
BLACK = (0, 0, 0)
WHITE = (245, 245, 245)
DARK_GRAY = (50, 50, 50)
GRAY = (200, 200, 200)

# Settings
DEFAULT_SIZE = 720
screen = pygame.display.set_mode((DEFAULT_SIZE, DEFAULT_SIZE), pygame.RESIZABLE)
pygame.display.set_caption("AMJADI DO0OZ")

clock = pygame.time.Clock()

# States
MENU, ABOUT, GAME, END = 0, 1, 2, 3
state = MENU
menu_options = ["Start Game", "About Game", "Toggle Fullscreen", "Exit"]
selected = 0

fullscreen = False

class SmallBoard:
    def __init__(self):
        self.cells = [['' for _ in range(3)] for _ in range(3)]
        self.winner = None
        self.finished = False

    def check_winner(self):
        lines = []

        for i in range(3):
            lines.append(self.cells[i])  # rows
            lines.append([self.cells[r][i] for r in range(3)])  # cols

        lines.append([self.cells[i][i] for i in range(3)])
        lines.append([self.cells[i][2 - i] for i in range(3)])

        for line in lines:
            if line[0] != '' and all(cell == line[0] for cell in line):
                self.winner = line[0]
                self.finished = True
                return self.winner

        if all(self.cells[r][c] != '' for r in range(3) for c in range(3)):
            # Randomly assign a winner color (X or O) for draw boards
            self.winner = random.choice(['X', 'O'])
            self.finished = True
            return self.winner

        return None

    def reset(self):
        self.cells = [['' for _ in range(3)] for _ in range(3)]
        self.winner = None
        self.finished = False

class BigBoard:
    def __init__(self):
        self.boards = [[SmallBoard() for _ in range(3)] for _ in range(3)]
        self.winner = None
        self.finished = False

    def check_winner(self):
        lines = []

        for i in range(3):
            lines.append([self.boards[i][j].winner for j in range(3)])
            lines.append([self.boards[j][i].winner for j in range(3)])

        lines.append([self.boards[i][i].winner for i in range(3)])
        lines.append([self.boards[i][2 - i].winner for i in range(3)])

        for line in lines:
            if None in line or 'Draw' in line:
                continue
            if line[0] != '' and all(w == line[0] for w in line):
                self.winner = line[0]
                self.finished = True
                return self.winner

        if all(b.finished for row in self.boards for b in row):
            self.winner = 'Draw'
            self.finished = True
            return 'Draw'

        return None

    def reset(self):
        for row in self.boards:
            for b in row:
                b.reset()
        self.winner = None
        self.finished = False

def draw_text_center(surface, text, font, color, x, y):
    txt_surf = font.render(text, True, color)
    rect = txt_surf.get_rect(center=(x, y))
    surface.blit(txt_surf, rect)

def draw_small_board(surface, board: SmallBoard, x, y, size, fullscreen):
    cell_size = size / 3
    pygame.draw.rect(surface, GRAY, (x, y, size, size))

    # Internal lines
    for i in range(1, 3):
        pygame.draw.line(surface, DARK_GRAY, (x + i * cell_size, y), (x + i * cell_size, y + size), 2)
        pygame.draw.line(surface, DARK_GRAY, (x, y + i * cell_size), (x + size, y + i * cell_size), 2)

    font_size = int(cell_size * 0.6)
    font = pygame.font.SysFont("Segoe UI", font_size, bold=True)
    font_x = pygame.font.SysFont("Segoe UI", font_size, bold=True)
    font_o = pygame.font.SysFont("Segoe UI", font_size, bold=True)

    for r in range(3):
        for c in range(3):
            cell = board.cells[r][c]
            cx = x + c * cell_size + cell_size / 2
            cy = y + r * cell_size + cell_size / 2
            if cell == 'X':
                # Player X black text
                text = font_x.render("X", True, BLACK)
                rect = text.get_rect(center=(cx, cy))
                surface.blit(text, rect)
            elif cell == 'O':
                if fullscreen:
                    # Draw circle centered in the cell for fullscreen mode
                    radius = int(cell_size * 0.3)
                    pygame.draw.circle(surface, RED, (int(cx), int(cy)), radius, 5)
                else:
                    # Player O red text
                    text = font_o.render("O", True, RED)
                    rect = text.get_rect(center=(cx, cy))
                    surface.blit(text, rect)

    # If board finished, draw border in winner color
    if board.finished:
        color = BLACK if board.winner == 'X' else RED if board.winner == 'O' else DARK_GRAY
        pygame.draw.rect(surface, color, (x, y, size, size), 4)

def draw_big_board(surface, big_board: BigBoard, size, fullscreen):
    surface.fill(WHITE)
    width, height = surface.get_size()
    big_cell = size / 3

    # محاسبه مختصات شروع برای وسط‌چین کردن
    start_x = (width - size) / 2
    start_y = (height - size) / 2

    # Draw big lines
    line_width = max(4, int(size * 0.008))
    for i in range(1, 3):
        pygame.draw.line(surface, BLACK, (start_x + i * big_cell, start_y), (start_x + i * big_cell, start_y + size), line_width)
        pygame.draw.line(surface, BLACK, (start_x, start_y + i * big_cell), (start_x + size, start_y + i * big_cell), line_width)

    for r in range(3):
        for c in range(3):
            draw_small_board(surface, big_board.boards[r][c], start_x + c * big_cell, start_y + r * big_cell, big_cell, fullscreen)


def draw_menu(surface, width, height, selected):
    surface.fill(WHITE)
    font_big = pygame.font.SysFont("Segoe UI", 48)
    font_med = pygame.font.SysFont("Segoe UI", 28)
    draw_text_center(surface, "Amjadi Game Doz(Doz)", font_big, BLACK, width // 2, height // 6)
    for i, option in enumerate(menu_options):
        color = RED if i == selected else DARK_GRAY
        draw_text_center(surface, option, font_med, color, width // 2, height // 3 + i * 50)

def draw_about(surface, width, height):
    surface.fill(WHITE)
    # Title with simple colored text, official font (Arial)
    font_title = pygame.font.SysFont("Arial", 48, bold=True)
    title_text1 = ": Builder Game :"
    title_text2 = "Alireza - Amjadi"
    
    # Colors for each word
    colors_line1 = [RED, JADE, BLUE]
    colors_line2 = [JADE, BLUE, RED]
    
    # Draw first line word by word with color
    words1 = title_text1.split()
    x_offset = width // 2 - (font_title.size(title_text1)[0] // 2)
    y_start = 40
    for i, word in enumerate(words1):
        text_surf = font_title.render(word, True, colors_line1[i % len(colors_line1)])
        surface.blit(text_surf, (x_offset, y_start))
        x_offset += text_surf.get_width() + font_title.size(" ")[0]

    # Draw second line word by word with color
    words2 = title_text2.split()
    x_offset = width // 2 - (font_title.size(title_text2)[0] // 2)
    y_start += 60
    for i, word in enumerate(words2):
        text_surf = font_title.render(word, True, colors_line2[i % len(colors_line2)])
        surface.blit(text_surf, (x_offset, y_start))
        x_offset += text_surf.get_width() + font_title.size(" ")[0]

    font_med = pygame.font.SysFont("Segoe UI", 24)
    lines = [
        "Date Build : 2025",
        "",
        "Ultimate Tic Tac Toe - How to play:",
        "1. The game consists of a 3x3 grid of smaller 3x3 Tic Tac Toe boards.",
        "2. Players take turns placing their marks (X or O) in the small cells.",
        "3. To win a small board, get three of your marks in a row (horizontally,",
        "   vertically, or diagonally) inside that board.",
        "4. Winning a small board claims that board for the player on the big board.",
        "5. The goal is to win three small boards in a row on the big board.",
        "6. If a small board ends in a draw, the game randomly assigns a winner",
        "   color (X or O) for display purposes.",
        "7. Player X uses black marks, Player O uses red marks.",
        "8. You can toggle fullscreen from the menu.",
        "",
        "Press ESC to return to menu."
    ]
    # Move all the lines 50px lower for better visibility
    for i, line in enumerate(lines):
        draw_text_center(surface, line, font_med, DARK_GRAY, width // 2, 150 + i * 30 + 50)

def handle_click(pos, big_board: BigBoard, current_player, width, height):
    if big_board.finished:
        return False
    x, y = pos

    big_cell = width / 3
    big_r = int(y // big_cell)
    big_c = int(x // big_cell)

    if big_r not in range(3) or big_c not in range(3):
        return False

    small_board = big_board.boards[big_r][big_c]

    if small_board.finished:
        return False

    small_cell_size = big_cell / 3
    small_r = int((y - big_r * big_cell) // small_cell_size)
    small_c = int((x - big_c * big_cell) // small_cell_size)

    if small_r not in range(3) or small_c not in range(3):
        return False

    if small_board.cells[small_r][small_c] == '':
        small_board.cells[small_r][small_c] = current_player
        small_board.check_winner()
        big_board.check_winner()
        return True
    return False

def show_end_screen(surface, width, height, winner):
    surface.fill(WHITE)
    font_big = pygame.font.SysFont("Segoe UI", 48, bold=True)
    font_med = pygame.font.SysFont("Segoe UI", 28)
    if winner == 'Draw':
        draw_text_center(surface, "It's a Draw!", font_big, DARK_GRAY, width // 2, height // 3)
    else:
        text = f"Player {winner} wins!"
        draw_text_center(surface, text, font_big, RED if winner == 'O' else BLACK, width // 2, height // 3)

    # Draw buttons
    btn_width, btn_height = 200, 60
    start_rect = pygame.Rect(width // 2 - btn_width - 20, height // 2, btn_width, btn_height)
    exit_rect = pygame.Rect(width // 2 + 20, height // 2, btn_width, btn_height)

    pygame.draw.rect(surface, BLUE, start_rect)
    pygame.draw.rect(surface, RED, exit_rect)

    draw_text_center(surface, "Restart", font_med, WHITE, start_rect.centerx, start_rect.centery)
    draw_text_center(surface, "Exit", font_med, WHITE, exit_rect.centerx, exit_rect.centery)

    return start_rect, exit_rect

def main():
    global screen, fullscreen, state, selected

    big_board = BigBoard()
    current_player = 'X'
    winner = None

    while True:
        width, height = screen.get_size()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if state == MENU:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected = (selected - 1) % len(menu_options)
                    elif event.key == pygame.K_DOWN:
                        selected = (selected + 1) % len(menu_options)
                    elif event.key == pygame.K_RETURN:
                        option = menu_options[selected]
                        if option == "Start Game":
                            big_board.reset()
                            current_player = 'X'
                            winner = None
                            state = GAME
                        elif option == "About Game":
                            state = ABOUT
                        elif option == "Toggle Fullscreen":
                            fullscreen = not fullscreen
                            if fullscreen:
                                screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                            else:
                                screen = pygame.display.set_mode((DEFAULT_SIZE, DEFAULT_SIZE), pygame.RESIZABLE)
                        elif option == "Exit":
                            pygame.quit()
                            sys.exit()

            elif state == ABOUT:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        state = MENU

            elif state == GAME:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if big_board.finished:
                        continue

                    if handle_click(event.pos, big_board, current_player, width, height):
                        if big_board.finished:
                            winner = big_board.winner
                            state = END
                        else:
                            current_player = 'O' if current_player == 'X' else 'X'

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        state = MENU

            elif state == END:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = event.pos
                    start_rect, exit_rect = show_end_screen(screen, width, height, winner)
                    if start_rect.collidepoint(mx, my):
                        big_board.reset()
                        current_player = 'X'
                        winner = None
                        state = GAME
                    elif exit_rect.collidepoint(mx, my):
                        pygame.quit()
                        sys.exit()

        # Draw
        if state == MENU:
            draw_menu(screen, width, height, selected)
        elif state == ABOUT:
            draw_about(screen, width, height)
        elif state == GAME:
            size = min(width, height)
            draw_big_board(screen, big_board, size, fullscreen)
        elif state == END:
            show_end_screen(screen, width, height, winner)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
