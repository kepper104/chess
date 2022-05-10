import installer
from solution import *
from pieces import *
from termcolor import colored
from colorama import init


def main():
    # Создаём шахматную доску
    board = Board()
    # Цикл ввода команд игроков
    while True:
        # Выводим положение фигур на доске
        print_board(board)
        # Подсказка по командам
        init()
        print(colored('Команды:', 'green'))
        print('    exit                               -- выход')
        print('    move <row> <col> <row1> <col1>     -- ход из клетки (row, col)')
        print('                                          в клетку (row1, col1)')
        print("    promote <row> <col> <row1> <col1> <figure>")
        print(
            "                                       -- переместит пешку и превратит ее в фигуру")
        print("                                        из списка rook, knight, bishop, queen, king")
        print("    castle <col>                     -- рокировать ладью из столба col")

        # Выводим приглашение игроку нужного цвета
        if board.current_player_color() == WHITE:
            print('Ход белых:')
        else:
            print('Ход черных:')
        command = input().split()
        if not command:
            print("Вы ввели ничего, попробуйте еще раз.")
            continue

        if command[0] == 'exit':
            print("Выхожу")
            break
        try:
            row = int(command[1])

            if command[0] == "move":
                col = int(command[2])
                row1, col1 = int(command[3]), int(command[4])
                print(row, col, row1, col1)
                move_result = board.move_piece(row, col, row1, col1)
                if move_result:
                    print('Ход успешен')
                else:
                    print("Что-то пошло не так! Попробуйте еще раз")
            elif command[0] == "promote":

                col = int(command[2])
                row1, col1 = int(command[3]), int(command[4])
                fig = command[5]
                print(row, col, row1, col1)
                promote_result = board.move_and_promote_pawn(
                    row, col, row1, col1, fig.lower()[0])
                if promote_result:
                    print("Ход и превращение успешно")
                else:
                    print("Что-то пошло не так! Попробуйте еще раз")
            elif command[0] == "castle":
                if row == 0:
                    castle_result = board.castling0()

                else:
                    castle_result = board.castling7()
                if castle_result:
                    print("Ход успешен")
                else:
                    print("Что-то пошло не так! Попробуйте еще раз")
            else:
                print("Неизвестная команда, попробуйте еще раз")
        except IndexError:
            print("Вы ввели слишком мало параметров. Попробуйте еще раз.")
        except ValueError:
            print("Вы ввели число там, где нужно было ввести строку. (или наоборот)")


if __name__ == '__main__':
    main()
