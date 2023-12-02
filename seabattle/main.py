from random import randint
from random import choice
from typing import Self, Optional

BOARD_SIZE: int = 6
SHIPS_LENGTH: tuple[int] = (3, 2, 2, 1, 1, 1, 1)
RANDOM_BOARD: int = 1000


class BoardOutException(Exception):
    def __str__(self) -> str:
        return "Точка за пределами доски"


class BoardShootedException(Exception):
    def __str__(self) -> str:
        return "В эту точку уже стреляли"


class BoardShipException(Exception):
    pass


class Dot:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.empty = True
        self.ship = False
        self.contour = False
        self.missed = False
        self.shooted = False

    def __eq__(self, other: Self) -> bool:
        return True if self.x == other.x and self.y == other.y else False

    def __str__(self) -> str:
        if self.shooted:
            return "X"
        elif self.ship:
            return "■"
        elif self.missed:
            return "T"
        else:
            return "O"

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"


class Ship:
    def __init__(self, length: int, nose: Dot, vertical: bool) -> None:
        self.length = length
        self.nose = nose
        # Вертикальное или горизонтальное расположение корабля
        self.vertical = vertical
        self.health = length

    @property
    def dots(self) -> list[Dot]:
        # Возвращает список всех точек корабля
        dots = []
        dotx = self.nose.x
        doty = self.nose.y
        for i in range(self.length):
            dots.append(Dot(dotx, doty))
            if self.vertical:
                dotx += 1
            else:
                doty += 1
        return dots


class Board:
    def __init__(self, hid: bool = False) -> None:
        self.dots = []
        # Наполняем двумерный массив точками этой доски
        for i in range(BOARD_SIZE):
            dots_row = []
            for j in range(BOARD_SIZE):
                dots_row.append(Dot(i+1, j+1))
            self.dots.append(dots_row)
        self.ships = []
        # Для количества оставшихся на доске кораблей
        self.live_ships = 0
        self.hid = hid

    def contour(self, ship: Ship) -> None:
        # Список смещений от начальной точки
        offsets = [(-2, -2), (-2, -1), (-2, 0),
                   (-1, -2), (-1, 0), (0, -1), (0, -2), (0, 0)]
        for shipdot in ship.dots:
            x, y = shipdot.x, shipdot.y
            # Для каждой точки корабля создаем точки со смещением
            for offsetx, offsety in offsets:
                newx = x + offsetx
                newy = y + offsety
                dot = Dot(newx + 1, newy + 1)
                # Если точки со смещением в пределах доски,
                # то помечаем их как точки контура
                if not self.out(dot) and newx >= 0 and newy >= 0:
                    self.dots[newx][newy].contour = True
                    self.dots[newx][newy].empty = False

    def add_ship(self, ship: Ship) -> None:
        for dot in ship.dots:
            x, y = dot.x, dot.y
            if self.out(dot):
                raise BoardShipException()
            elif not self.dots[x-1][y-1].empty:
                raise BoardShipException()
        # Если точки добавляемого корабля в пределах доски,
        # то помечаем их как точки корабля на доске и добавляем
        # корабль в список кораблей на этой доске
        for dot in ship.dots:
            x, y = dot.x, dot.y
            self.dots[x-1][y-1].ship = True
            self.dots[x-1][y-1].empty = False
        self.live_ships += 1
        self.ships.append(ship)
        self.contour(ship)

    @property
    def print(self) -> None:
        result = "    1   2   3   4   5   6"
        for i, row in enumerate(self.dots):
            result += f"\n{i+1} | " + " | ".join(str(dot) for dot in row) + " |"
        # Если есть этот флаг, то не выводим корабли
        if self.hid:
            result = result.replace("■", "O")
        print(result)

    def out(self, dot: Dot) -> bool:
        return (
            True
            if (dot.x > BOARD_SIZE or dot.x <= 0) or (dot.y > BOARD_SIZE or dot.y <= 0)
            else False
        )

    def shot(self, x: int, y: int) -> Optional[bool]:
        dot = Dot(x, y)
        # Если точка за пределами доски, то вызываем ошибку
        if self.out(dot):
            raise BoardOutException()
        else:
            board_dot = self.dots[x-1][y-1]
            # Если точка доски уже была помечена как промах
            # или как выстрел, то вызываем ошибку
            if board_dot.missed or board_dot.shooted:
                raise BoardShootedException()
            else:
                for ship in self.ships:
                    if dot in ship.dots:
                        # Если точка выстрела есть в списке точек
                        # корабля, то помечаем ее как выстрел
                        ship.health = ship.health - 1
                        board_dot.shooted = True
                        if ship.health == 0:
                            self.live_ships = self.live_ships - 1
                            print("Корабль уничтожен. Переход хода.")
                            return False
                        else:
                            print("Корабль ранен. Повторный ход.")
                            return True
                board_dot.missed = True
                print("Промах. Переход хода.")
                return False


class Player:
    def __init__(self, opponent_board: Board) -> None:
        self.opponent_board = opponent_board

    def ask(self) -> None:
        pass

    def move(self) -> None:
        switch = True
        while switch:
            try:
                x, y = self.ask()
                switch = self.opponent_board.shot(x, y)
            except (BoardOutException, BoardShootedException) as e:
                print(e)


class User(Player):
    def ask(self) -> list[int]:
        # Возращает два введенных числа
        result = map(int, input(f"Введите два числа в диапазоне от 1 до {BOARD_SIZE} через пробел: ").split())
        return result


class AI(Player):
    def ask(self) -> list[int]:
        # Возращает два случайных числа
        x = randint(1, BOARD_SIZE)
        y = randint(1, BOARD_SIZE)
        print(f"Ход компьютера: {x} {y}")
        return [x, y]


class Game:
    def __init__(self) -> None:
        switch = True
        while switch:
            try:
                # Пытаемся создать доску со случайными кораблями,
                # попыток может быть больше 1000
                board_user, i = self.random_board()
                board_ai, j = self.random_board()
                print("Доска юзера создана, попытки:", i)
                print("Доска компа создана, попытки:", j)
                board_ai.hid = True
                switch = False
            except BoardShipException:
                pass

        self.user_player = User(board_ai)
        self.ai_player = AI(board_user)

    def random_board(self) -> tuple[Board, int]:
        board = Board()
        counter = 0
        for sh_length in SHIPS_LENGTH:
            switch = True
            while switch:
                if counter == RANDOM_BOARD:
                    raise BoardShipException()
                # Создаем случайный корабль
                nose_dot = Dot(randint(1, BOARD_SIZE), randint(1, BOARD_SIZE))
                vertical = choice([True, False])
                ship = Ship(sh_length, nose_dot, vertical)
                counter += 1
                try:
                    # Пытаемся добавить корабль на доску, если возникнет
                    # ошибка, то пропускаем ее и продолжаем попытки
                    board.add_ship(ship)
                    switch = False
                except BoardShipException:
                    pass

        return (board, counter)

    def greet(self) -> str:
        greeting = f"""
        Морской бой
        -------------------
        Доски с кораблями генерируются автоматически.
        Размер доски: {BOARD_SIZE}x{BOARD_SIZE}
        Количество кораблей на доске: {len(SHIPS_LENGTH)}

        Формат ввода: x y
        x - номер строки
        y - номер столбца
        """
        print(greeting)
        self.user_player.opponent_board.print
        self.ai_player.opponent_board.print

    def loop(self) -> None:
        counter = 0
        switcher = True
        while switcher:
            # Чередуем ходы пользователя и компа
            if counter % 2 == 0:
                self.user_player.move()
            else:
                self.ai_player.move()
            print(f"Доска компа (осталось кораблей {self.user_player.opponent_board.live_ships}):")
            self.user_player.opponent_board.print
            print(f"Доска юзера (осталось кораблей: {self.ai_player.opponent_board.live_ships}):")
            self.ai_player.opponent_board.print
            counter += 1

            if self.user_player.opponent_board.live_ships == 0:
                print("Юзер выиграл!")
                switcher = False
            elif self.ai_player.opponent_board.live_ships == 0:
                print("Комп выиграл!")
                switcher = False

    def start(self) -> None:
        self.greet()
        self.loop()


game = Game()
game.start()
