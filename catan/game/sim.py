import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "thezhongfamily.settings")
django.setup()

import joblib

import catan.models as catan
import random
import numpy as np

random.seed = 0

class Game():
    def __init__(self, sim=True):
        if sim:
            "Game() constructor called in sim mode"
            self.players = []
            self.tiles = []
            self.vertices = []
            self.edges = []
            self.resources = None
            self.winner = False
            self.initialized = False
            self.board = np.zeros((55, 55))

        else:
            pass

    def initialize(self):
        # create four player models
        for i in range(1,5):
            self.players.append(catan.Player(id=i, name="Player %d" % i, victory_points=0,
                                             brick=0, wood=0, wheat=0, sheep=0, stone=0))

        # create 19 tiles, allocate resource type and dice values
        random.shuffle(resource_vals)
        random.shuffle(resources)
        for i in range(18):
            self.tiles.append(catan.Tile(id=i, resource_type=resources[i],
                                         dice_value=resource_vals[i]))
        self.tiles.append(catan.Tile(id=18, resource_type=u"desert",
                                     dice_value=7))

        # create vertices
        for i in range(1,56):
            self.vertices.append(catan.Vertex(id=i, available=True, has_city=False))

        # create edges
        for i in range(1,73):
            self.edges.append(catan.Edge(id=i, available=True))

        # SAVE PLAYERS, TILES, EDGES, AND VERTICES
        print(len(self.players), len(self.tiles))
        for player in self.players:
            print("Saving player %s" % player.name)
            player.save()

        for tile in self.tiles:
            print("Saving tile of resource %s, dice val %d" % (tile.resource_type, tile.dice_value))
            tile.save()

        for edge in self.edges:
            edge.save()

        for vertex in self.vertices:
            vertex.save()


        self.initialized = True

    def init_board(self):
        self.board[1, 4] = 1
        self.board[1, 5] = 2
        self.board[2, 5] = 3
        self.board[2, 6] = 4
        self.board[3, 6] = 5
        self.board[3, 7] = 6
        self.board[4, 8] = 7
        self.board[5, 9] = 8
        self.board[6, 10] = 9
        self.board[7, 11] = 10
        self.board[8, 13] = 11
        self.board[9, 13] = 12
        self.board[9, 14] = 13
        self.board[10, 14] = 14
        self.board[10, 15] = 15
        self.board[11, 15] = 16
        self.board[8, 12] = 17
        self.board[11, 16] = 18
        self.board[12, 17] = 19
        self.board[13, 18] = 20
        self.board[14, 19] = 21
        self.board[15, 20] = 22
        self.board[16, 21] = 23
        self.board[17, 23] = 24
        self.board[18, 23] = 25
        self.board[18, 24] = 26
        self.board[19, 24] = 27
        self.board[19, 25] = 28
        self.board[20, 25] = 29
        self.board[20, 26] = 30
        self.board[21, 26] = 31
        self.board[17, 22] = 32
        self.board[21, 27] = 33
        self.board[22, 28] = 34
        self.board[23, 29] = 35
        self.board[24, 30] = 36
        self.board[25, 31] = 37
        self.board[26, 32] = 38
        self.board[27, 33] = 39
        self.board[28, 34] = 40
        self.board[29, 34] = 41
        self.board[29, 35] = 42
        self.board[30, 35] = 43
        self.board[30, 36] = 44
        self.board[31, 36] = 45
        self.board[31, 37] = 46
        self.board[32, 37] = 47
        self.board[32, 38] = 48
        self.board[33, 38] = 49
        self.board[34, 39] = 50
        self.board[35, 40] = 51
        self.board[36, 41] = 52
        self.board[37, 42] = 53
        self.board[38, 43] = 54
        self.board[39, 44] = 55
        self.board[40, 44] = 56
        self.board[40, 45] = 57
        self.board[41, 45] = 58
        self.board[41, 46] = 59
        self.board[42, 46] = 60
        self.board[42, 47] = 61
        self.board[43, 47] = 62
        self.board[44, 48] = 63
        self.board[45, 49] = 64
        self.board[46, 50] = 65
        self.board[47, 51] = 66
        self.board[48, 52] = 67
        self.board[49, 52] = 68
        self.board[49, 53] = 69
        self.board[50, 53] = 70
        self.board[50, 54] = 71
        self.board[51, 54] = 72

        self.board += self.board.transpose()

    def assign_tiles(self):
        for i, tile in enumerate(self.tiles):
            print(i, tile)

    def roll_dice(self):
        return random.randint(1,6) + random.randint(1,6)

    def start_turn(self, id):
        """Simulate the dice roll and allocate resources to all players.
        Allow the current player to build roads, settlements, and cities as desired.
        Will eventually implement trading functionality"""

        roll = self.roll_dice()

        if roll != 7:
            self.distribute_resources(roll)
        else:
            self.move_robber()

    def move_robber(self):
        raise NotImplementedError

    def distribute_resources(self, roll):
        raise NotImplementedError


if __name__ == "__main__":
    resources = [u"brick", u"brick", u"brick",
                 u"wood", u"wood", u"wood", u"wood",
                 u"wheat", u"wheat", u"wheat", u"wheat",
                 u"sheep", u"sheep", u"sheep", u"sheep",
                 u"stone", u"stone", u"stone"]

    resource_vals = [2, 3, 3, 4, 4, 5, 5, 6, 6, 8, 8, 9, 9, 10, 10, 11, 11, 12]
    print(len(resource_vals), len(resources))

    sim = Game()
    if not sim.initialized:
        sim.initialize()
        sim.init_board()
        print(sim.board.shape)

    turn = 0

    sim.assign_tiles()

    while sim.winner == False:
        #sim.winner = True
        if turn > 4:
            player = turn % 4
        #sim.start_turn(player + 1)
        #sim.end_turn()
        turn += 1
        _ = input(">>Press Enter for next Turn")

