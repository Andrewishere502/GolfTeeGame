from itertools import tee
import pygame

from board import Board


class Display:
    def __init__(self, width, height, board):
        self.width = width
        self.height = height
        self.win = pygame.display.set_mode((width, height))

        self.reset_game(board)

        pygame.display.set_caption("Golf Tee Game")
        return

    def clear(self):
        self.win.fill((0, 0, 0))
        return

    def reset_game(self, board):
        self.selected_tee = None
        self.click_radius = 20
        self.tee_radius = 8
        self.hole_radius = 4

        self.board = board

        self.refresh_board(board)
        return

    def refresh_board(self, board):
        hole_hor_margin = 50
        hole_vert_margin = round((hole_hor_margin ** 2 - (hole_hor_margin // 2) ** 2) ** 0.5)

        # Center the tiles on the y coordinate starting here
        y = (self.win.get_height() // 2
             - (len(board.rows) - 1) * hole_vert_margin // 2
             )

        # ------------ Set up the board base ---------------
        self.board_corners = [
            # top vertex
            (self.win.get_width() // 2, y - self.click_radius),

            # bottom left vertex
            (self.win.get_width() // 2 - (len(board.rows) - 1) * hole_hor_margin // 2 - self.click_radius * (3 ** 0.5 / 2),
             y + (len(board.rows) - 1) * hole_vert_margin + self.click_radius // 2),

            # bottom right vertex
            (self.win.get_width() // 2 + (len(board.rows) - 1) * hole_hor_margin // 2 + self.click_radius * (3 ** 0.5 / 2),
             y + (len(board.rows) - 1) * hole_vert_margin + self.click_radius // 2),
        ]

        # ------------ Set up the holes and pegs -------------
        self.tee_infos = []
        for row in range(len(board.rows)):
            num_cols = len(board.rows[row])
            # center the tiles on the x coordinate
            x = (self.win.get_width() // 2
                 - (num_cols - 1) * hole_hor_margin // 2
                 )

            for col in range(num_cols):
                try:
                    tee_id = int(board.rows[row][col])
                except ValueError:  # The tee is actually an open hole
                    tee_id = 0

                if tee_id == 0:
                    radius = self.hole_radius
                    tee_color = (0, 0, 0)
                elif tee_id == 1:
                    radius = self.tee_radius
                    tee_color = (232, 232, 232)  # white
                elif tee_id == 2:
                    radius = self.tee_radius
                    tee_color = (153, 38, 0)  # red
                elif tee_id == 3:
                    radius = self.tee_radius
                    tee_color = (0, 36, 153)  # blue
                elif tee_id == 4:
                    radius = self.tee_radius
                    tee_color = (105, 0, 153)  # purple

                self.tee_infos.append((tee_color, (x, y), radius, (row, col)))

                x += hole_hor_margin
            y += hole_vert_margin
        return

    def select_or_move_tee(self, click_pos):
        for tee_info in self.tee_infos:
            tee_pos = tee_info[1]

            x_distance = tee_pos[0] - click_pos[0]
            y_distance = tee_pos[1] - click_pos[1]

            distance = (x_distance ** 2 + y_distance ** 2) ** 0.5
            if distance < self.click_radius:
                # The player is clicking on a tee, not a hole
                if tee_info[2] != self.hole_radius:
                    if self.selected_tee == tee_info:
                        self.selected_tee = None
                    else:
                        self.selected_tee = tee_info
                # The player is clicking on a hole
                else:
                    tee_pos = self.selected_tee[3]
                    move_to = tee_info[3]
                    self.board.make_move(tee_pos, move_to)
                    self.refresh_board(self.board)
                break
        return

    def draw_board(self):
        # pygame.draw.line(self.win, (255, 0, 0), (self.win.get_width() // 2, 0), (self.win.get_width() // 2, self.win.get_height()))
        # pygame.draw.line(self.win, (255, 0, 0), (0, self.win.get_height() // 2), (self.win.get_width(), self.win.get_height() // 2))
        board_color = (79, 66, 31)

        # ------------ draw the board base ---------------
        pygame.draw.polygon(self.win, board_color, self.board_corners)

        # ------------ draw the holes and pegs -------------
        for tee_info in self.tee_infos:
            if tee_info == self.selected_tee:
                pygame.draw.circle(self.win, *tee_info[:2], self.tee_radius + 4, 2)

            # Exclude the index of the tee/hole from tee_info
            pygame.draw.circle(self.win, *tee_info[:3])
        return

    @staticmethod
    def update():
        pygame.display.update()
        return


pygame.init()

side_length = 3
board = Board(side_length)
WIDTH = (side_length - 5) * 40 + 400
HEIGHT = WIDTH - 100
display = Display(WIDTH, HEIGHT, board)
display.reset_game(board)
run = True
while run:
    pygame.time.delay(50)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                board = Board(side_length)
                display.reset_game(board)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click_pos = pygame.mouse.get_pos()
            display.select_or_move_tee(click_pos)


    display.clear()
    display.draw_board()
    display.update()
pygame.quit()