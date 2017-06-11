

class Game():
    def __init__(self, sim=True):
        if sim:
            "Game() constructor called in sim mode"
            self.players = None
            self.tiles = None
            self.resources = None
            self.winner = False

        else:
            pass

    def initialize(self):
        raise NotImplementedError



if __name__ == "__main__":
    sim = Game()
    sim.initialize()
    turn = 0
    while sim.winner == False:
        player = turn % 3
        sim.start_turn(player)
        sim.end_turn()

