WHITE = 1
BLACK = 2


class Piece():
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color

    def set_position(self, row, col):
        self.row = row
        self.col = col

    def char(self):
        return None

    def get_color(self):
        return self.color

    def can_move(self):
        return False

    def is_out_of_bounds(self, row, col):
        if 0 <= row <= 7 and 0 <= col <= 7:
            return False
        return True


class Pawn(Piece):
    def char(self):
        return 'P'

    def can_move(self, row, col):
        # Пешка может ходить только по вертикали
        # "взятие на проходе" не реализовано
        if self.col != col:
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
        if self.row + direction == row:
            return True

        # ход на 2 клетки из начального положения
        if self.row == start_row and self.row + 2 * direction == row:
            return True

        return False


class Rook(Piece):
    def char(self):
        return 'R'

    def can_move(self, row, col):
        if self.row == row or self.col == col:
            return True
        return False


class Knight(Piece):
    def char(self):
        return "N"

    def can_move(self, row, col):
        r1 = abs(self.row - row)
        r2 = abs(self.col - col)
        can = r1 == 1 and r2 == 2 or r1 == 2 and r2 == 1
        if can and not self.is_out_of_bounds(row, col):
            return True
        return False


class Bishop(Piece):
    def char(self):
        return "B"

    def can_move(self, row, col):
        if (abs(self.row - row) == abs(self.col - col)) and not self.is_out_of_bounds(row, col):
            return True
        return False


class Queen(Piece):
    def char(self):
        return "Q"

    def can_move(self, row, col):
        can = self.col == col or self.row == row or abs(
            self.row - row) == abs(self.col - col)

        if can and not self.is_out_of_bounds(row, col):
            return True
        return False
