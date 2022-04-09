import random


class Board:
    def __init__(self, side_length):
        self.rows = []
        for k in range(1, side_length + 1):
            new_row = random.choices([1, 2, 3, 4], cum_weights=[90, 94, 98, 100], k=k)
            new_row = [str(tee) for tee in new_row]
            self.rows.append(new_row)

        row = random.randrange(0, len(self.rows))
        col = random.randrange(0, len(self.rows[row]))
        self.rows[row][col] = "0"
        return

    def draw(self):
        for row_num, row in enumerate(self.rows):
            print("  " * (len(self.rows) - row_num) + "   ".join(row))
        return

    def __get_valid_move(self, move, middle_pos):
        """Return True if the given move is valid, otherwise return False.
        
        move -- the spot where the tee is being moved to
        middle_pos -- the spot between move and the tee being moved
        """

        move_is_good = True
        # check to make sure the move fits in the board
        try:
            self.rows[move[0]][move[1]]
            self.rows[middle_pos[0]][middle_pos[1]]
        except IndexError:
            move_is_good = False
        else:
            # check if the indices in move are positive so
            # pieces can't loop around the board
            if move[0] < 0 or move[1] < 0:
                move_is_good = False

            # check if the spot to move to is not empty
            if self.rows[move[0]][move[1]] != "0":
                move_is_good = False

            # check if the spot being jumped over is empty
            if self.rows[middle_pos[0]][middle_pos[1]] == "0":
                move_is_good = False
        return move_is_good

    def calc_tee_moves(self, tee_pos):
        """Return a set of all the valid moves from a given tee position.
        
        tee_pos -- the position of a tee, given as a tuple of indices
        """
        possible_tee_moves = []

        # top left
        move = tee_pos[0] - 2, tee_pos[1] - 2
        middle_pos = tee_pos[0] - 1, tee_pos[1] - 1
        if self.__get_valid_move(move, middle_pos):  # append move if it is valid
            possible_tee_moves.append(move)

        # top right
        move = tee_pos[0] - 2, tee_pos[1]
        middle_pos = tee_pos[0] - 1, tee_pos[1]
        if self.__get_valid_move(move, middle_pos):  # append move if it is valid
            possible_tee_moves.append(move)

        # left
        move = tee_pos[0], tee_pos[1] - 2
        middle_pos = tee_pos[0], tee_pos[1] - 1
        if self.__get_valid_move(move, middle_pos):  # append move if it is valid
            possible_tee_moves.append(move)

        # right
        move = tee_pos[0], tee_pos[1] + 2
        middle_pos = tee_pos[0], tee_pos[1] + 1
        if self.__get_valid_move(move, middle_pos):  # append move if it is valid
            possible_tee_moves.append(move)

        # bottom left
        move = tee_pos[0] + 2, tee_pos[1]
        middle_pos = tee_pos[0] + 1, tee_pos[1]
        if self.__get_valid_move(move, middle_pos):  # append move if it is valid
            possible_tee_moves.append(move)

        # bottom right
        move = tee_pos[0] + 2, tee_pos[1] + 2
        middle_pos = tee_pos[0] + 1, tee_pos[1] + 1
        if self.__get_valid_move(move, middle_pos):  # append move if it is valid
            possible_tee_moves.append(move)

        return possible_tee_moves

    def make_move(self, tee_pos, move_to):
        valid_moves = self.calc_tee_moves(tee_pos)
        if move_to in valid_moves:
            tee = self.rows[tee_pos[0]][tee_pos[1]]
            middle_tee_pos = (int((tee_pos[0] + move_to[0]) / 2),
                              int((tee_pos[1] + move_to[1]) / 2))

            # Set the current tee position to blank
            self.rows[tee_pos[0]][tee_pos[1]] = "0"
            # Set the tee that was jumped over to blank
            self.rows[middle_tee_pos[0]][middle_tee_pos[1]] = "0"
            # Set the blank position the tee moved to the
            # tee which was moved
            self.rows[move_to[0]][move_to[1]] = tee
        return

    def calc_all_moves(self):
        """Return a dictionary where the keys are the position of the
        tee being moved, and the values as the valid moves for that
        tee.
        """
        moves = {}
        for y in range(len(self.rows)):
            for x in range(len(self.rows[y])):
                tee_moves = self.calc_tee_moves((y, x))
                if len(tee_moves) > 0:
                    moves.update({f"{y}, {x}": tee_moves})
        return moves


if __name__ == "__main__":
    side_length = 5
    board = Board(side_length)
    board.draw()

    # Show valid moves for each tee, 1 at a time
    # for y in range(len(board.rows)):
    #     for x in range(len(board.rows[y])):
    #         pos = (y, x)
    #         print(pos)
    #         moves = board.calc_tee_moves(pos)
    #         print(moves)
    #         input()

    # Show valid moves for all tees at once
    # moves = board.calc_all_moves()
    # print(moves)

    tee_pos = (1, 1)
    move_to = (3, 3)
    board.make_move(tee_pos, move_to)

    board.draw()
