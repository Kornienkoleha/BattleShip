# импортируем random для игры с компьютером
import random

# Создаем класс исключений
class BoardOutException(Exception):
    pass

# Класс точек на поле
class Dot:
    def __init__(self, x, y):
        self.x = x # координаты точки
        self.y = y

    def __eq__(self, other): # Проверка точек на равенство
        return self.x == other.x and self.y == other.y

# Класс кораблей на игровом поле
class Ship(Dot):
    def __init__(self, length, bow, direction):
        self.length = length # длина корабля
        self.bow = bow # Точка, где размещён нос корабля
        self.direction = direction # Направление корабля (V - вертикальное/ G - горизонтальное)
        self.lives = [1] * length # количество жизней

    @property
    def dots(self): # возвращает список всех точек корабля
        ship_dots = []
        for i in range(self.length):
            if self.direction == "V": # Если direction имеет вертикальное положение
                ship_dots.append(Dot(self.bow.x + i, self.bow.y)) # Добавляет корабль на игровое поле
            elif self.direction == "G": # Если direction имеет вертикальное положение
                ship_dots.append(Dot(self.bow.x, self.bow.y + i))
        return ship_dots

# Класс игровой доски
class Board:
    def __init__(self, hid=False):
        self.field = [["O"] * 6 for i in range(6)] # Пустой массив 6 на 6
        self.ships = [] # Список кораблей доски
        self.alive_ships = 0 # Игровая жизнь
        self.hid = hid # Скрывать корабли на доске

    # Метод установки кораблей на доску
    def add_ship(self, ship):
        for d in ship.dots:
            if self.out(d) or self.field[d.x][d.y] != "O":
                raise Exception
        for d in ship.dots:
            self.field[d.x][d.y] = "■"
        self.ships.append(ship)
        self.alive_ships += 1
# Метод обводит корабль по контуру
    def contour(self, ship, value):
        for d in ship.dots:
            if not self.out(d):
                if self.field[d.x][d.y] == "O":
                    self.field[d.x][d.y] = value
# Метод выводит доску в консоль в зависимости от параметра hid
    def __str__(self):
        result = ""
        result += "    1   2   3   4   5   6"
        for y, row in enumerate(self.field):
            result += "\n"
            result += chr(y + 65) + " | "
            for x in row:
                if self.hid and x == "■":
                    result += " O "
                else:
                    result += x + " | "
        return result
# Метод out, который для точки (объекта класса Dot) возвращает True,
    # если точка выходит за пределы поля, и False, если не выходит
    def out(self, dot):
        return dot.x < 0 or dot.x > 6 or dot.y < 0 or dot.y > 6
# Метод shot, который делает выстрел по доск
    def shot(self, dot):
        if self.out(dot):
            raise BoardOutException
        if self.field[dot.x][dot.y] == "■":
            self.field[dot.x][dot.y] = "X"
            for ship in self.ships:
                if dot in ship.dots:
                    ship.lives -= 1
                    if ship.lives == 0:
                        self.alive_ships -= 1
                        self.contour(ship, "X")
                        return True
            return True
        elif self.field[dot.x][dot.y] == "O":
            self.field[dot.x][dot.y] = "-"
            return False
        else:
            raise Exception("Вы уже стреляли в эту клетку")
#  Класс игрока
class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy
    # метод, который «спрашивает» игрока, в какую клетку он делает выстрел
    def ask(self):
        pass
    # метод, который делает ход в игре
    def move(self):
        while True:
            try:
                target = self.ask()
                hit = self.enemy.shot(target)
                return hit
            except BoardOutException:
                print("Вы стреляете за пределы поля!")
            except Exception as e:
                print(e)
# Унаследование классов AI и User от Player
class AI(Player):
    def ask(self): # Случайный выстрел компьютером
        return Dot(random.randint(0, 6), random.randint(0, 6))

class User(Player):
    def __init__(self, board, enemy):
        self.board = Board(hid=False)
        self.enemy = enemy

    def ask(self): # Выстрел в противника игроком
        while True:
            cords = input("Введите координаты выстрела (напр. A1): ").upper()
            if len(cords) != 2:
                print("Введите координаты в правильном формате.")
                continue
            x = ord(cords[0]) - 65
            y = int(cords[1]) - 1
            if x < 0 or x > 6 or y < 0 or y > 6:
                print("Введите координаты в пределах поля.")
                continue
            return Dot(x, y)
# Основной игровой класс
class Game:
    def __init__(self):
        self.user = User(Board(), Board())
        self.ai = AI(Board(), Board())

    # Случайное расставление кораблей на игровом поле ИИ
    def random_board(self, board):
        attempts = 0
        for ship in reversed([4, 5, 3]):
            while True:
                attempts += 1
                if attempts > 2000:
                    return False
                bow = Dot(random.randint(0, 6), random.randint(0, 6))
                direction = random.choice(["V", "G"])
                if direction == "V":
                    if bow.x + ship <= 6:
                        try:
                            board.add_ship(Ship(ship, bow, direction))
                            break
                        except Exception:
                            pass
                elif direction == "G":
                    if bow.y + ship <= 6:
                        try:
                            board.add_ship(Ship(ship, bow, direction))
                            break
                        except Exception:
                            pass
            board.alive_ships = len(board.ships)
            return True
    # Правила игры
    def greet(self):
        print("Морской бой!\n"
              "Правила просты:\n"
              "У каждого из вас есть доска 6x6.\n"
              "На досках расположены корабли разной длины (от 1 до 3 клеток).\n"
              "Цель игры - потопить все корабли противника.\n"
              "Выиграет тот, кто первый потопит все корабли.\n"
              "Координаты клеток указываются буквами (A-F) и цифрами (1-6).\n")
    # Метод с самим игровым циклом
    def loop(self):
        while True:
            print("\nДоска пользователя:")
            print(self.user.board)
            print("\nДоска компьютера:")
            print(self.user.enemy)
            if self.user.move():
                print("Попадание!")
            else:
                print("Промах!")
            if self.ai.move():
                print("Компьютер попал!")
            else:
                print("Компьютер промахнулся!")
            if self.user.board.alive_ships == 0:
                print("Вы проиграли!")
                break
            if self.ai.board.alive_ships == 0:
                print("Вы выиграли!")
                break
    # Запуск игры
    def start(self):
        self.greet()
        while True:
            if self.random_board(self.user.board) and self.random_board(self.ai.board):
                break
        self.loop()

game = Game()
game.start()
