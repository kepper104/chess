from pieces import *
WHITE = 1
BLACK = 2


class Board:
    def __init__(self):
        self.color = WHITE
        self.field = []
        for row in range(8):
            self.field.append([None] * 8)

        # Default placement

        # self.field[0] = [
        #     Rook(WHITE), Knight(WHITE), Bishop(WHITE), Queen(WHITE),
        #     King(WHITE), Bishop(WHITE), Knight(WHITE), Rook(WHITE)
        # ]
        # self.field[1] = [
        #     Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE),
        #     Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE)
        # ]
        # self.field[6] = [
        #     Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK),
        #     Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK)
        # ]
        # self.field[7] = [
        #     Rook(BLACK), Knight(BLACK), Bishop(BLACK), Queen(BLACK),
        #     King(BLACK), Bishop(BLACK), Knight(BLACK), Rook(BLACK)
        # ]

    def current_player_color(self):
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

    def move_piece(self, row, col, row1, col1):
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
        self.field[row][col] = None  # Снять фигуру.
        self.field[row1][col1] = piece  # Поставить на новое место.
        piece.set_position(row1, col1)
        self.color = opponent(self.color)
        return True

    def get_piece(self, row, col):
        if correct_coords(row, col):
            return self.field[row][col]
        return None


def correct_coords(row, col):
    """Функция проверяет, что координаты (row, col) лежат
    внутри доски"""
    return 0 <= row <= 8 and 0 <= col <= 7


def opponent(color):
    if color == WHITE:
        return BLACK
    return WHITE


def print_board(board):  # Распечатать доску в текстовом виде (см. скриншот)
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


def main():
    # Создаём шахматную доску
    board = Board()
    # Цикл ввода команд игроков
    while True:
        # Выводим положение фигур на доске
        print_board(board)
        # Подсказка по командам
        print('Команды:')
        print('    exit                               -- выход')
        print('    move <row> <col> <row1> <col1>     -- ход из клетки (row, col)')
        print('                                          в клетку (row1, col1)')
        # Выводим приглашение игроку нужного цвета
        if board.current_player_color() == WHITE:
            print('Ход белых:')
        else:
            print('Ход черных:')
        command = input()
        if command == 'exit':
            break
        move_type, row, col, row1, col1 = command.split()
        row, col, row1, col1 = int(row), int(col), int(row1), int(col1)
        if board.move_piece(row, col, row1, col1):
            print('Ход успешен')
        else:
            print('Координаты некорректы! Попробуйте другой ход!')


if __name__ == '__main__':
    # main()
    pass
