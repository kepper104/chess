WHITE = 1
BLACK = 2


class Piece():
    def __init__(self, color, moved=False):
        self.color = color
        self.moved = False

    def char(self):
        return None

    def get_color(self):
        return self.color

    def can_move(self, board, row, col, row1, col1):
        return False

    def is_out_of_bounds(self, row, col):
        if 0 <= row <= 7 and 0 <= col <= 7:
            return False
        return True

    def in_its_position(self, row, col, row1, col1):
        if row == row1 and col == col1:
            return True
        return False

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Pawn(Piece):
    def char(self):
        return 'P'

    def can_move(self, board, row, col, row1, col1):
        if self.in_its_position(row, col, row1, col1):
            return False
        # Пешка может ходить только по вертикали
        # "взятие на проходе" не реализовано
        if col != col1:
            return False

        # Пешка может сделать из начального положения ход на 2 клетки
        # вперёд, поэтому поместим индекс начального ряда в start_row.
        if self.color == WHITE:
            direction = 1
            start_row = 1
        else:
            direction = -1
            start_row = 6

        # ход на 1 клетку
        if row + direction == row1:
            return True

        # ход на 2 клетки из начального положения
        if (row == start_row
                and row + 2 * direction == row1
                and board.field[row + direction][col] is None):
            return True
        return False

    def can_attack(self, board, row, col, row1, col1):
        direction = 1 if (self.color == WHITE) else -1
        return (row + direction == row1
                and (col + 1 == col1 or col - 1 == col1))


class Rook(Piece):
    def char(self):
        return 'R'

    def can_move(self, board, row, col, row1, col1):
        if self.in_its_position(row, col, row1, col1):
            return False

        if row != row1 and col != col1:
            return False

        step = 1 if (row1 >= row) else -1
        for r in range(row + step, row1, step):
            # Если на пути по вертикали есть фигура
            if not (board.get_piece(r, col) is None):
                return False

        step = 1 if (col1 >= col) else -1
        for c in range(col + step, col1, step):
            # Если на пути по горизонтали есть фигура
            if not (board.get_piece(row, c) is None):
                return False

        if not (board.get_piece(row1, col1) is None):
            return False
        return True


class Knight(Piece):
    def char(self):
        return "N"

    def can_move(self, board, row, col, row1, col1):
        if self.in_its_position(row, col, row1, col1):
            return False
        r1 = abs(row - row1)
        r2 = abs(col - col1)
        can = r1 == 1 and r2 == 2 or r1 == 2 and r2 == 1
        if can and not self.is_out_of_bounds(row, col):
            return True
        return False


class Bishop(Piece):
    def char(self):
        return "B"

    def can_move(self, board, row, col, row1, col1):
        if self.in_its_position(row, col, row1, col1):
            return False
        if (abs(row - row1) == abs(col - col1)) and not self.is_out_of_bounds(row, col):
            return True
        return False


class Queen(Piece):
    def char(self):
        return "Q"

    def can_move(self, board, row, col, row1, col1):
        if self.in_its_position(row, col, row1, col1):
            return False
        can = col == col1 or row == row1 or abs(
            row - row1) == abs(col - col1)
        if not can or self.is_out_of_bounds(row1, col1):
            return False

        piece_dest = board.get_piece(row1, col1)
        if not (piece_dest is None):
            if piece_dest.get_color() == self.get_color():
                return False

        if col1 == col:
            step = 1 if (row1 >= row) else -1
            for r in range(row + step, row1, step):
                # Если на пути по вертикали есть фигура
                mb_piece = board.get_piece(r, col)
                if not (mb_piece is None):
                    return False

        elif row1 == row:
            step = 1 if (col1 >= col) else -1
            for c in range(col + step, col1, step):
                # Если на пути по горизонтали есть фигура
                mb_piece = board.get_piece(row, c)
                if not (mb_piece is None):
                    return False
        else:
            step_row = 1 if (row1 >= row) else -1
            step_col = 1 if (col1 >= col) else -1
            cur_row, cur_col = row, col
            for i in range(abs(row1 - row)):
                cur_row += step_row
                cur_col += step_col
                mb_piece = board.get_piece(cur_row, cur_col)
                if not (mb_piece is None):
                    same = row1 == cur_row and col1 == cur_col
                    if mb_piece.get_color() != self.get_color() and same:
                        return True
                    return False
        return True


class King(Piece):
    def char(self):
        return "K"

    def can_move(self, board, row, col, row1, col1):
        if self.in_its_position(row, col, row1, col1):
            return False
        if abs(row - row1) <= 1 and abs(col - col1) <= 1:
            return True
        return False
