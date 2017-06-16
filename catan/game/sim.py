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

        # create 19 tiles, random dice values and random resource type
        for i in range(19):
            self.tiles.append(catan.Tile(resource_type=resources[random.randint(0, 4)],
                                         dice_value=random.randint(1, 12)))
        # create vertices

        # create edges
        print(len(self.players), len(self.tiles))
        for player in self.players:
            print("Saving player %s" % player.name)


        for tile in self.tiles:
            print("Saving tile of resource %s" % tile.resource_type)


        self.initialized = True

    def roll_dice(self):
        return random.randint(1,6) + random.randint(1,6)



if __name__ == "__main__":
    resources = [u"brick", u"wood", u"wheat", u"sheep", u"stone"]
    sim = Game()
    if not sim.initialized:
        sim.initialize()

    turn = 0

    while sim.winner == False:
        sim.winner = True
        if turn > 4:
            player = turn % 4
        #sim.start_turn(player + 1)
        #sim.end_turn()
        turn += 1

