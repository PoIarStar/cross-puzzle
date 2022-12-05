import pygame
from random import randint


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * height for _ in range(width)]
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect((self.left, self.top),
                                                              (self.width * self.cell_size + 1,
                                                               self.height * self.cell_size + 1)))
        for i in range(self.left, self.left + self.width * self.cell_size, self.cell_size):
            for j in range(self.top, self.top + self.height * self.cell_size, self.cell_size):
                n, m = self.get_coords((i, j))
                if not self.board[n][m]:
                    pygame.draw.rect(screen, (0, 0, 0),
                                     pygame.Rect((i + 1, j + 1), (self.cell_size - 1, self.cell_size - 1)))

    def get_coords(self, coords):
        x_coord = (coords[0] - self.left) // self.cell_size
        y_coord = (coords[1] - self.top) // self.cell_size
        if x_coord < self.width and y_coord < self.height:
            return (x_coord, y_coord)
        return None

    def on_click(self, cell):
        if cell:
            for i in range(self.width):
                for j in range(self.height):
                    if i == cell[0] or j == cell[1]:
                        self.board[i][j] = abs(self.board[i][j] - 1)

    def get_click(self, cur_pos):
        coords = self.get_coords(cur_pos)
        self.on_click(coords)


try:
    pygame.init()
    pygame.display.set_caption('Cross puzzle')
    size = width, height = 801, 651
    screen = pygame.display.set_mode(size)
    board = Board(16, 12)
    board.set_view(0, 0, 50)
    running = True
    is_clear = False
    standart = [[0] * board.height for _ in range(board.width)]
    c = 0
    while running:
        for event in pygame.event.get():
            if is_clear:
                c = -1
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event.pos)
                if board.board == standart:
                    c += 1
                    for i in range(c):
                        board.on_click((randint(0, 15), randint(0, 11)))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    board.board = [[0] * board.height for _ in range(board.width)]
                    is_clear = True
                elif event.key == pygame.K_r:
                    board.board = [[0] * board.height for _ in range(board.width)]
                    for i in range(c):
                        board.on_click((randint(0, 15), randint(0, 11)))
                elif event.key == pygame.K_s:
                    is_clear = False
                    c = 0
        screen.fill((0, 0, 0))
        board.render(screen)
        screen.blit(pygame.font.Font(None, 80).render(str(c), True, (100, 255, 100)), (0, 601))
        pygame.display.flip()
    pygame.quit()
except Exception as e:
    print(e)
    pygame.quit()

