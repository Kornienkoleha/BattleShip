# Класс точек на поле
class Dot:
    def __init__(self, X: int = None, Y: int = None):
        self.Coordinate_X = X
        self.Coordinate_Y = Y

    def __eq__(self, other):
        return self.Coordinate_X == other.Coordinate_X and self.Coordinate_Y == other.Coordinate_Y

    def __str__(self):
        return f'Dot: {self.Coordinate_X, self.Coordinate_Y}'


p1=Dot(1,2)
p2=Dot(1,2)

print(p1)
print(p2)

# Класс кораблей
class Ship:

    HORIZONTAL = 1
    VERTICAL = 2

    def __init__(self, length: int, HV: int = HORIZONTAL, x: int = None, y: int = None):
        self.length = length  # длина корабля
        self.x = x  # координаты начала корабля (нос корабля)
        self.y = y
        self.HV = HV  # ориентация корабля (1 - горизонтальная, 2 - вертикальная)
        self.life = True  # Количество жизней (сколько точек корабля ещё не подбито - True, иначе False)
        self.dots = [1] * length  # список всех точек корабля


Hy2 = Ship(4, 1, 1, 4)
print(Hy2.dots)
print(Hy2.life)
print(Hy2)

# Класс игровой доски
class Board(Ship):
    def __init__(self, size: int = 6):
        self.size = size  # размер игровой доски
        self.field = [['О'] * self.size for i in range(self.size)]  # игровая доска
        self.ships = [3, 2, 2, 1, 1, 1, 1]  # список кораблей на доске
        self.hid = True
        self.count_living_ships = 0

    def add_ship(self):
        return self.field[self.Coordinate_X - 1].pop(self.Coordinate_Y - 1)
        # self.field[self.Coordinate_X - 1].insert(self.Coordinate_Y - 1, '■')

GGG = Board().field
print(GGG)


JJ = [['О', 'О', 'О', 'О', 'О', 'О'], ['О', 'О', 'О', 'О', 'О', 'О'], ['О', 'О', 'О', 'О', 'О', 'О'], ['О', 'О', 'О', 'О', 'О', 'О'], ['О', 'О', 'О', 'О', 'О', 'О'], ['О', 'О', 'О', 'О', 'О', 'О']]

x = 1
y = 2

u = y + 3
del JJ[x][y:u]


JJ[x].insert(y, 'X')

print(JJ)