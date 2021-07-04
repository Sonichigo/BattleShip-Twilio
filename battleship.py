import random
from copy import deepcopy


class Battleship:
    def __init__(self):
        self.players = {}
        self.lon = {
            'a': 0,
            'b': 1,
            'c': 2,
            'd': 3,
            'e': 4,
            'f': 5,
            'g': 6,
            'h': 7,
            'i': 8,
            'j': 9
        }

    def turn(self, number, coordinates):
        #Create a new Game
        if number not in self.players.keys():
            self.players[number] = {'p_ships': self.create_board(), 'p_shots': [], 'c_ships': self.create_board(),
                                    'c_shots': []}
        coordinates = coordinates.split(', ')
        return self.shot(number, (self.lon[coordinates[0].lower()], int(coordinates[1]) - 1))

    #Function to resolve the events of a shot
    def shot(self, number, coordinates):
        if coordinates in self.players[number]['p_shots']:
            return 'You did that shot already'

        #player shot
        self.players[number]['p_shots'].append(coordinates)

        if all(item in self.players[number]['p_shots'] for item in self.players[number]['c_ships']):
            c_board, p_board = self.get_boards(self.players[number])
            self.players.pop(number)
            return 'congrats you won: \n' + self.stringify_board(c_board) + '\n' + self.stringify_board(p_board)

        #computer shoots
        c_shot = self.c_shoots(number)
        self.players[number]['c_shots'].append(c_shot)
        c_board, p_board = self.get_boards(self.players[number])

        if all(item in self.players[number]['c_shots'] for item in self.players[number]['p_ships']):
            return 'Sorry you lost that game: \n' + self.stringify_board(c_board) + '\n' + self.stringify_board(p_board)

        msg = ''
        if coordinates in self.players[number]['c_ships']:
            msg += 'Nice shot! You hit a ship on ' + list(self.lon.keys())[
                list(self.lon.values()).index(coordinates[0])].upper() +', ' + str(coordinates[1] + 1) + '!\n'
        else:
            msg += 'Unfortunately off target.\n'

        msg += 'The computer shoots back:\n'
        if c_shot in self.players[number]['p_ships']:
            msg += 'Oh NO! your ship on ' + list(self.lon.keys())[
                list(self.lon.values()).index(c_shot[0])].upper() +', ' + str(c_shot[1] + 1) + ' has been hit!\n'
        else:
            msg += 'Lucky you, the computers shot on ' + list(self.lon.keys())[
                list(self.lon.values()).index(c_shot[0])].upper() +', ' + str(c_shot[1] + 1) + ' and missed.\n'

        return msg + '\n' + self.stringify_board(p_board)

    #computer shoots
    def c_shoots(self, number):
        shot = (random.randint(0, 4), random.randint(0, 4))
        if shot in self.players[number]['c_shots']:
            return self.c_shoots(number)
        return shot

    def create_board(self):
        ships = []
        # 2*Battleships
        for _ in range(2):
            self.set_ship(3, ships)
        # 3*Cruiser
        for _ in range(3):
            self.set_ship(2, ships)
        # 4*Submarines
        for _ in range(4):
            self.set_ship(1, ships)
        return ships

    #sets a ship to random empty position
    def set_ship(self, fields, ships):
        vertical = random.randint(0, 1)
        if vertical:
            row = random.randint(0, 4)
            column = random.randint(0, 4 - fields)
            ship = [x for x in zip([row] * fields, range(column, column + fields))]
        else:
            row = random.randint(0, 4 - fields)
            column = random.randint(0, 4)
            ship = [x for x in zip(range(row, row + fields), [column] * fields)]
        for coordinate in ship:
            if coordinate in ships:
                self.set_ship(fields, ships)
                return

        ships.extend(ship)

    # Retruns the boards as array
    def get_boards(self, player):
        p_board = [
            ['', '', '', '', ''],
            ['', '', '', '', ''],
            ['', '', '', '', ''],
            ['', '', '', '', ''],
            ['', '', '', '', '']
        ]
        c_board = deepcopy(p_board)

        for shot in player['p_shots']:
            p_board[shot[0]][shot[1]] += '+'
            c_board[shot[0]][shot[1]] += '*'
        for shot in player['c_shots']:
            p_board[shot[0]][shot[1]] += '*'
            c_board[shot[0]][shot[1]] += '+'
        for ship in player['p_ships']:
            p_board[ship[0]][ship[1]] += 'O'
        for ship in player['c_ships']:
            c_board[ship[0]][ship[1]] += 'O'
        return c_board, p_board

    #returns a string of the board
    def stringify_board(self, board):
        s = ''
        for row in board:
            for field in row:
                s += ' [' + field + ']'
            s += '\n'
        return s
