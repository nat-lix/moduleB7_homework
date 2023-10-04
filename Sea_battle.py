from re import fullmatch
from random import randint


class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __init__(self, message="Выстрел за поле!"):
        self.message = message
        super().__init__(self.message)


class BoardNearException(BoardException):
    def __init__(self, message="Нельзя ставить корабль вплотную с другим кораблем!"):
        self.message = message
        super().__init__(self.message)


class BoardUsedException(BoardException):
    def __init__(self, message="Тут уже со всеми покончено!"):
        self.message = message
        super().__init__(self.message)

class InvalidCoordinateException(BoardException):
    def __init__(self, message="Введите две числовые координаты от 1 до 6 через пробел!"):
        self.message = message
        super().__init__(self.message)


class Dot:
    def __init__(self, x, y):
        self._x = x - 1
        self._y = y - 1

    def __eq__(self, other):
        return self._x == other.x and self._y == other.y

    def __repr__(self):
        return f'({self._x + 1}, {self._y + 1})'

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value


class ReplaceDot:
    def __init__(self, hidden=False):
        self.status = 'О'
        self.ship = 0
        self.destroy = 0
        self.miss = 0
        self.outline = 0
        self.hidden = hidden

    def set_hidden(self, n):
        self.hidden = n

    def set_ship(self, n):
        self.ship = n

    def set_destroy(self, n):
        self.destroy = n

    def set_miss(self, n):
        self.miss = n

    def set_outline(self, n):
        self.outline = n

    def get_status(self):
        return self.status

    def get_ship(self):
        return self.ship

    def get_destroy(self):
        return self.destroy

    def get_miss(self):
        return self.miss

    def get_outline(self):
        return self.outline

    def change_status(self):
        if self.ship == 1:
            self.status = '■'
        if self.hidden == True:
            self.status = 'o'
        if self.destroy == 1:
            self.status = 'X'
        elif self.miss == 1:
            self.status = 'T'

vert, hor = 1, 2

class Board:
    def __init__(self, hidden=False):
        self.field = [[ReplaceDot(hidden) for j in range(6)] for i in range(6)]

    def field_rendering(self):
        for i in self.field:
            for j in i:
                j.change_status()
        num = 0
        print('  | 1 | 2 | 3 | 4 | 5 | 6 |')
        for i in self.field:
            num += 1
            print(num, '|', i[0].get_status(), '|', i[1].get_status(), '|', i[2].get_status(), '|', i[3].get_status(),
                  '|',
                  i[4].get_status(), '|', i[5].get_status(), '|')

    def ships_count(self):
        ships_cnt = 0
        for i in self.field:
            for j in i:
                if j.get_ship() == 1:
                    ships_cnt += 1
        return ships_cnt

    def add_ship(self, ship):
        if ship.direction == vert:
            for i in range(ship.length):
                if self.field[ship.get_start_dot().x + i][ship.get_start_dot().y].get_outline() == 1:
                    raise BoardNearException
                elif ship.get_start_dot().x + ship.length >= 6:
                    raise BoardOutException
                else:
                    self.field[ship.get_start_dot().x + i][ship.get_start_dot().y].set_ship(1)
        elif ship.direction == hor:
            for i in range(ship.length):
                if self.field[ship.get_start_dot().x][ship.get_start_dot().y + i].get_outline() == 1:
                    raise BoardNearException
                elif ship.get_start_dot().y + ship.length >= 6:
                    raise BoardOutException
                else:
                    self.field[ship.get_start_dot().x][ship.get_start_dot().y + i].set_ship(1)
        self.outline(ship)

    def outline(self, ship):
        if ship.direction == vert:
            for n in range(ship.length):
                for i in range(3):
                    for j in range(3):
                        if ship.get_start_dot().x + 1 - j + n >= 0 and ship.get_start_dot().x + 1 - j + n <= 5 and ship.get_start_dot().y + 1 - i >= 0 and ship.get_start_dot().y + 1 - i <= 5:
                            self.field[ship.get_start_dot().x + 1 - j + n][ship.get_start_dot().y + 1 - i].set_outline(
                                1)
        elif ship.direction == hor:
            for n in range(ship.length):
                for i in range(3):
                    for j in range(3):
                        if ship.get_start_dot().x + 1 - j >= 0 and ship.get_start_dot().x + 1 - j <= 5 and ship.get_start_dot().y + 1 - i + n >= 0 and ship.get_start_dot().y + 1 - i + n <= 5:
                            self.field[ship.get_start_dot().x + 1 - j][ship.get_start_dot().y + 1 - i + n].set_outline(
                                1)

    def shot(self, dot):
        if self.field[dot.x][dot.y].get_destroy() == 1 or self.field[dot.x][dot.y].get_miss() == 1:
            raise BoardUsedException
        else:
            if self.field[dot.x][dot.y].get_ship() == 1:
                self.field[dot.x][dot.y].set_destroy(1)
                self.field[dot.x][dot.y].set_ship(0)
                self.contour(dot)
                return True
            else:
                self.field[dot.x][dot.y].set_miss(1)
                return False

    def contour(self, dot):
        ship_counter = 0
        try:
            for i in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
                if dot.x + i[0] <= 5 and dot.x + i[0] >= 0 and dot.y + i[1] <= 5 and dot.y + i[1] >= 0:
                    if dot.x + i[0] + i[0] <= 5 and dot.x + i[0] + i[0] >= 0 and dot.y + i[1] + i[1] <= 5 and dot.y + i[
                        1] + i[1] >= 0:
                        if self.field[dot.x + i[0]][dot.y + i[1]].get_ship() == 1 or self.field[dot.x + i[0]][
                            dot.y + i[1]].get_destroy() == 1:
                            if self.field[dot.x + i[0] + i[0]][dot.y + i[1] + i[1]].get_destroy() == 1:
                                ship_counter = 3
                                break
                            if self.field[dot.x + i[0] + i[0]][dot.y + i[1] + i[1]].get_ship() == 1:
                                ship_counter = 0
                                break
                    if self.field[dot.x + i[0]][dot.y + i[1]].get_destroy() == 1 and self.field[dot.x - i[0]][
                        dot.y - i[1]].get_ship() == 0:
                        ship_counter = 2
                        break
                    if self.field[dot.x + i[0]][dot.y + i[1]].get_ship() == 1:
                        ship_counter = 0
                        break
                    if self.field[dot.x + i[0]][dot.y + i[1]].get_ship() == 0 and self.field[dot.x + i[0]][
                        dot.y + i[1]].get_destroy() == 0:
                        ship_counter = 1
            if ship_counter == 2:
                for a in range(3):
                    for b in range(3):
                        if dot.x + 1 - b <= 5 and dot.x + 1 - b >= 0 and dot.y + 1 - a <= 5 and dot.y + 1 - a >= 0:
                            if self.field[dot.x + 1 - b][dot.y + 1 - a].get_ship() != 1:
                                self.field[dot.x + 1 - b][dot.y + 1 - a].set_miss(1)
                for a in range(3):
                    for b in range(3):
                        if dot.x + i[0] + 1 - a <= 5 and dot.x + i[0] + 1 - a >= 0 and dot.y + i[
                            1] + 1 - b <= 5 and dot.y + i[1] + 1 - b >= 0:
                            if self.field[dot.x + i[0] + 1 - a][dot.y + i[1] + 1 - b].get_ship() != 1:
                                self.field[dot.x + i[0] + 1 - a][dot.y + i[1] + 1 - b].set_miss(1)
            if ship_counter == 3:
                for a in range(3):
                    for b in range(3):
                        if dot.x + 1 - b <= 5 and dot.x + 1 - b >= 0 and dot.y + 1 - a <= 5 and dot.y + 1 - a >= 0:
                            if self.field[dot.x + 1 - b][dot.y + 1 - a].get_ship() != 1:
                                self.field[dot.x + 1 - b][dot.y + 1 - a].set_miss(1)
                for a in range(3):
                    for b in range(3):
                        if dot.x + i[0] + 1 - a <= 5 and dot.x + i[0] + 1 - a >= 0 and dot.y + i[
                            1] + 1 - b <= 5 and dot.y + i[1] + 1 - b >= 0:
                            if self.field[dot.x + i[0] + 1 - a][dot.y + i[1] + 1 - b].get_ship() != 1:
                                self.field[dot.x + i[0] + 1 - a][dot.y + i[1] + 1 - b].set_miss(1)
                for a in range(3):
                    for b in range(3):
                        if dot.x + i[0] + i[0] + 1 - a <= 5 and dot.x + i[0] + i[0] + 1 - a >= 0 and dot.y + i[1] + i[
                            1] + 1 - b <= 5 and dot.y + i[1] + i[1] + 1 - b >= 0:
                            if self.field[dot.x + i[0] + i[0] + 1 - a][dot.y + i[1] + i[1] + 1 - b].get_ship() != 1:
                                self.field[dot.x + i[0] + i[0] + 1 - a][dot.y + i[1] + i[1] + 1 - b].set_miss(1)
            if ship_counter == 1:
                for a in range(3):
                    for b in range(3):
                        if dot.x + 1 - b <= 5 and dot.x + 1 - b >= 0 and dot.y + 1 - a <= 5 and dot.y + 1 - a >= 0:
                            if self.field[dot.x + 1 - b][dot.y + 1 - a].get_ship() != 1:
                                self.field[dot.x + 1 - b][dot.y + 1 - a].set_miss(1)
        except BoardException:
            pass
        ship_counter = 0


class Ship:
    def __init__(self, length, start_dot, direction):
        self.length = length
        self.start_dot = start_dot
        self.direction = direction

    def get_length(self):
        return self.length

    def get_start_dot(self):
        return self.start_dot

    def get_direction(self):
        return self.direction


class Player:
    def __init__(self, board, enemy_board):
        self.board = board
        self.enemy_board = enemy_board

    def ask(self):
        pass

    def move(self):
        while True:
            try:
                target = self.ask()
                return self.enemy_board.shot(target)
            except BoardException as e:
                print(e)
            else:
                break


class User(Player):
    def ask(self):
        n = input("Ваш ход: ")
        if fullmatch('\d \d', n):
            n = n.split(' ', 2)
            x, y = int(n[0]), int(n[1])
            if x >= 1 and x <= 6 and y >= 1 and y <= 6:
                return Dot(x, y)
            else:
                raise BoardOutException
        else:
            raise InvalidCoordinateException



class Ai(Player):
    def ask(self):
        c = Dot(randint(1, 6), randint(1, 6))
        print(f"Ход компьютера: {c}")
        return c


class Game:
    def __init__(self):
        user_board = self.random_board()
        ai_board = self.random_board(hidden=True)
        self.user = User(user_board, ai_board)
        self.ai = Ai(ai_board, user_board)

    def random_board(self, hidden=False):
        board = Board(hidden)
        length_list = [3, 2, 2, 1, 1, 1, 1]
        index = 0
        attempts = 0
        while index <= 6:
            if attempts == 2000 or board.ships_count() > 10:
                board = Board(hidden)
                index = 0
                attempts = 0
            try:
                ship = Ship(length_list[index], Dot(randint(1, 6), randint(1, 6)), randint(1, 2))
                board.add_ship(ship)
            except BoardException:
                pass
            else:
                index += 1
            attempts += 1
        return board

    def show_boards(self):
        print("Поле игрока:")
        self.user.board.field_rendering()
        print("Поле компьютера:")
        self.ai.board.field_rendering()

    def loop(self):
        counter = 2
        while True:
            if counter % 2 == 0:
                self.show_boards()
                repeat = self.user.move()
                if repeat:
                    print("Попал!")
                elif not repeat:
                    print("Мимо!")

            else:
                repeat = self.ai.move()
            if self.ai.board.ships_count() == 0:
                self.show_boards()
                print("Ура! Победа игрока!")
                break
            elif self.user.board.ships_count() == 0:
                self.show_boards()
                print("Ха-ха! Мешок с костями повержен!")
                break

            if not repeat:
                counter += 1

    def greet(self):
        print("")
        print("  Добро пожаловать  ")
        print("")
        print("        в       ")
        print("")
        print("      игру!     ")
        print("")
        print("    *  *  *")
        print("")
        print("Введите координаты x y через пробел")
        print("")
        print("x - номер строки")
        print("y - номер столбца")
        print("")

    def start(self):
        self.greet()
        self.loop()


game = Game()
game.start()