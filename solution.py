from pieces import *
WHITE = 1
BLACK = 2
FIGURES = {
    "Q": Queen,
    "R": Rook,
    "N": Knight,
    "B": Bishop,
    "K": King
}


class Board:

    def __init__(self):
        self.color = WHITE
        self.field = []
        for row in range(8):
            self.field.append([None] * 8)

        # Стандартная расстановка фигур

        self.field[0] = [
            Rook(WHITE), Knight(WHITE), Bishop(WHITE), Queen(WHITE),
            King(WHITE), Bishop(WHITE), Knight(WHITE), Rook(WHITE)
        ]
        self.field[1] = [
            Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE),
            Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE)
        ]
        self.field[6] = [
            Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK),
            Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK)
        ]
        self.field[7] = [
            Rook(BLACK), Knight(BLACK), Bishop(BLACK), Queen(BLACK),
            King(BLACK), Bishop(BLACK), Knight(BLACK), Rook(BLACK)
        ]

    def current_player_color(self):
        """Получить цвет игрока, который сейчас ходит"""
        return self.color

    def cell(self, row, col):
        """Возвращает строку из двух символов. Если в клетке (row, col)
        находится фигура, символы цвета и фигуры. Если клетка пуста,
        то два пробела."""
        piece = self.field[row][col]
        if piece is None:
            return '  '
        color = piece.get_color()
        c = 'w' if color == WHITE else 'b'
        return c + piece.char()

    def move_piece(self, row, col, row1, col1, move=True):
        """Переместить фигуру из точки (row, col) в точку (row1, col1).
        Если перемещение возможно, метод выполнит его и вернет True.
        Если нет --- вернет False"""

        if not correct_coords(row, col) or not correct_coords(row1, col1):
            return False
        if row == row1 and col == col1:
            return False  # нельзя пойти в ту же клетку
        piece = self.field[row][col]
        if piece is None:
            return False
        if piece.get_color() != self.color:  # Ходит не тот человек/фигурой не того цвета
            return False
        if self.field[row1][col1] is None:
            if not piece.can_move(self, row, col, row1, col1):
                return False
        elif self.field[row1][col1].get_color() == opponent(piece.get_color()):
            if not piece.can_attack(self, row, col, row1, col1):
                return False
        else:
            return False
        if move:
            self.field[row][col] = None  # Снять фигуру.
            piece.moved = True
            self.field[row1][col1] = piece  # Поставить на новое место.
            self.color = opponent(self.color)
        return True

    def get_piece(self, row, col):
        """Получить фигуру в клетке row, col. Аналог field[row][col], но проверяет правильность координат"""
        if correct_coords(row, col):
            return self.field[row][col]
        return None

    def move_and_promote_pawn(self, row, col, row1, col1, char):
        """Возвышение пешки, получает начальные и конечные координаты, 
        символ фигуры, в которую конвертируется пешка """
        # Получаем фигуру
        piece = self.field[row][col]
        # Проверяем что это пешка
        if piece.char() != "P":
            return False
        # Проверяем что она может походить на крайний ряд
        if not self.move_piece(row, col, row1, col1, move=False):
            return False

        self.field[row][col] = None  # Снимаем пешку
        # Ставим новую фигуру выбранного знака
        self.field[row1][col1] = FIGURES[char](piece.get_color())
        self.color = opponent(self.color)  # Меняем цвет
        return True

    def castling0(self):
        """Длинная рокировка (C левой ладьи)"""
        # Определение строки по цвету
        row = 7 if self.color == BLACK else 0

        # Провека отсутствия фигур между
        figs_beetween = [self.field[row][1], self.field[row]
                         [2], self.field[row][3]]
        if any(figs_beetween):
            return False
        # Проверка того, что фигуры, которыми играют это ладья и король
        if not isinstance(self.field[row][0], Rook) or not isinstance(self.field[row][4], King):
            return False

        # Проверка того, что никакие фигуры не двигались
        action_figs = [self.field[row][0].moved, self.field[row]
                       [4].moved]

        if any(action_figs):
            return False

        self.field[row][0] = None  # Снимаем ладью
        self.field[row][3] = Rook(self.color, True)  # Ставим ладью

        self.field[row][4] = None  # Снимаем короля
        self.field[row][2] = King(self.color, True)  # Ставим короля

        self.color = opponent(self.color)  # Меняем цвет

        return True

    def castling7(self):
        """Короткая рокировка (C правой ладьи)"""
        # Определение строки по цвету
        row = 7 if self.color == BLACK else 0

        # Провека отсутствия фигур между
        figs_beetween = [self.field[row][5], self.field[row]
                         [6]]

        if any(figs_beetween):
            return False

        # Проверка того, что фигуры, которыми играют это ладья и король
        if not isinstance(self.field[row][7], Rook) or not isinstance(self.field[row][4], King):
            return False

        # Проверка того, что никакие фигуры не двигались
        action_figs = [self.field[row][7].moved, self.field[row]
                       [4].moved]

        if any(action_figs):
            return False

        self.field[row][7] = None  # Снимаем ладью
        self.field[row][5] = Rook(self.color, True)  # Ставим ладью

        self.field[row][4] = None  # Снимаем короля
        self.field[row][6] = King(self.color, True)  # Ставим короля

        self.color = opponent(self.color)  # Меняем цвет

        return True


def correct_coords(row, col):
    """Функция проверяет, что координаты (row, col) лежат
    внутри доски"""
    return 0 <= row <= 8 and 0 <= col <= 7


def opponent(color):
    """Возвращает цвет, противоположный введенному"""
    if color == WHITE:
        return BLACK
    return WHITE


def print_board(board):
    """Красиво выводит доску со всеми фигурами"""
    print('     +----+----+----+----+----+----+----+----+')
    for row in range(7, -1, -1):
        print(' ', row, end='  ')
        for col in range(8):
            print('|', board.cell(row, col), end=' ')
        print('|')
        print('     +----+----+----+----+----+----+----+----+')
    print(end='        ')
    for col in range(8):
        print(col, end='    ')
    print()
