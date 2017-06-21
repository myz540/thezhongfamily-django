import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "thezhongfamily.settings")
import django
django.setup()

import catan.models as catan
import random

random.seed = 0


class Game():
    def __init__(self, sim=True):
        if sim:
            "Game() constructor called in sim mode"
            self.players = []
            self.tiles = []
            self.resources = None
            self.winner = False
            self.initialized = False

        else:
            pass

    def initialize(self):
        # create four player models
        for i in range(1,5):
            self.players.append(catan.Player(name="Player %d" % i, victory_points=0,
                                             brick=0, wood=0, wheat=0, sheep=0, stone=0))

        # create 19 tiles, allocate resource type and dice values
        random.shuffle(resource_vals)
        random.shuffle(resources)
        for i in range(18):
            self.tiles.append(catan.Tile(resource_type=resources[i],
                                         dice_value=resource_vals[i]))
        self.tiles.append(catan.Tile(resource_type=u"desert",
                                     dice_value=7))
        # create vertices

        # create edges

        print(len(self.players), len(self.tiles))
        for player in self.players:
            print("Saving player %s" % player.name)
            player.save()

        for tile in self.tiles:
            print("Saving tile of resource %s, dice val %d" % (tile.resource_type, tile.dice_value))
            tile.save()

        self.initialized = True

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

    turn = 0

    while sim.winner == False:
        #sim.winner = True
        if turn > 4:
            player = turn % 4
        #sim.start_turn(player + 1)
        #sim.end_turn()
        turn += 1
        _ = input(">>Press Enter for next Turn")

