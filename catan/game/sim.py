import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "thezhongfamily.settings")
django.setup()
import joblib
import catan.models as catan
import random
import numpy as np


class Game():
    def __init__(self, sim=True):
        if sim:
            "Game() constructor called in sim mode"
            self.players = []
            self.tiles = []
            self.vertices = []
            self.edges = []
            self.winner = False
            self.winning_player = None
            self.initialized = False
            self.board = np.zeros((54, 54))
            self.turn = 0
            self.turn_count = 0

        else:
            pass

    def initialize(self):
        """

        """
        print("initialize() called")

        # create players, edges, vertices, and tiles
        self.create_models()

        #print(len(self.players), len(self.tiles), len(self.edges), len(self.vertices))

        # Assign 6 vertices and 6 edges to each tile
        self.init_tiles()

        # Initialize connectivity of edges and vertices
        self.init_board()

        # Save game, AKA create/update database
        self.save_game()

        # Assign everyone's first settlement and give 4 of each resource
        self.start_location_and_resources()

        # Save game, AKA create/update database
        self.save_game()

        print("initialize() done")

    def create_models(self):
        """
        Instantiate player, edge, vertex, and tile models that compose the game
        All models are stored in lists and the id of the model matches the index of
        the object in the list
        """
        print("create_models() called")

        # create four player models
        for i in range(4):
            self.players.append(catan.Player(id=i, name="Player %d" % i, victory_points=0,
                                             brick=0, wood=0, wheat=0, sheep=0, stone=0))

        # create 54 vertices
        for i in range(54):
            self.vertices.append(catan.Vertex(id=i, available=True, has_city=False))

        # create 72 edges
        for i in range(72):
            self.edges.append(catan.Edge(id=i, available=True))

        # create 19 tiles, allocate resource type and dice values
        random.shuffle(resource_vals)
        random.shuffle(resources)
        for i in range(18):
            self.tiles.append(catan.Tile(id=i, resource_type=resources[i],
                                         dice_value=resource_vals[i]))
        self.tiles.append(catan.Tile(id=18, resource_type=u"desert",
                                     dice_value=7))

        print("create_models() done")

    def init_tiles(self):
        """
        j_vertex and j_edge are 19 element lists, where each element is a list
        containing the index of the edge or tile that composes the tile. A many-to-many relationship
        is created here. Django many-to-many relationships allow lookups across relations
        so given a tile, I can check all its availabilities and who owns what.
        NOTHING IS SAVED THOUGH UNTIL the save_game() function is called
        """
        print("init_tiles() called")

        # contains lists of the tile and edge id's that belong to each tile
        j_vertex = [
                    [0, 3, 4, 7, 8, 12],
                    [1, 4, 5, 8, 9, 13],
                    [2, 5, 6, 9, 10, 14],
                    [7, 11, 12, 16, 17, 22],
                    [8, 12, 13, 17, 18, 23],
                    [9, 13, 16, 18, 19, 24],
                    [10, 14, 15, 19, 20, 25],
                    [16, 21, 22, 27, 28, 33],
                    [17, 22, 23, 28, 29, 34],
                    [18, 23, 24, 29, 30, 35],
                    [19, 24, 25, 30, 31, 36],
                    [20, 25, 26, 31, 32, 37],
                    [28, 33, 34, 38, 39, 43],
                    [29, 34, 35, 39, 40, 44],
                    [30, 35, 36, 40, 41, 45],
                    [31, 36, 37, 41, 42, 46],
                    [39, 43, 44, 47, 48, 51],
                    [40, 44, 45, 48, 49, 52],
                    [41, 45, 46, 49, 50, 53],
                    ]
        j_edge = [
                  [0, 1, 6, 7, 11, 12],
                  [2, 3, 7, 8, 13, 14],
                  [4, 5, 8, 9, 15, 16],
                  [10, 11, 18, 19, 24, 25],
                  [12, 13, 19, 20, 26, 27],
                  [14, 15, 20, 21, 28, 29],
                  [16, 17, 21, 22, 30, 31],
                  [23, 24, 33, 34, 39, 40],
                  [25, 26, 34, 35, 41, 42],
                  [27, 28, 35, 36, 43, 44],
                  [29, 30, 36, 37, 45, 46],
                  [31, 32, 37, 38, 47, 48],
                  [40, 41, 49, 50, 64, 55],
                  [42, 43, 50, 51, 56, 57],
                  [44, 45, 51, 52, 58, 59],
                  [46, 47, 52, 53, 60, 61],
                  [55, 56, 62, 63, 66, 67],
                  [57, 58, 63, 64, 68, 69],
                  [59, 60, 64, 65, 70, 71],
                  ]

        # Each tile has 6 edges and 6 vertices
        for i in range(18):
            for v, e in zip(j_vertex[i], j_edge[i]):
                #print(v, e)
                self.tiles[i].vertex.add(self.vertices[v])
                self.tiles[i].edge.add(self.edges[e])

        print("init_tiles() done")

    def init_board(self):
        """
        Populate matrix mapping edge and vertex connectivity
        Vertex id's are along the rows and columns. A '0' entry at (i, j) indicates
        vertices i and j are not connected. Any other entry at (i, j) indicates that
        i and j are connected by edge with id = entry value
        """
        print("init_board() called")
        self.board[0, 3] = 0
        self.board[0, 4] = 1
        self.board[1, 4] = 2
        self.board[1, 5] = 3
        self.board[2, 5] = 4
        self.board[2, 6] = 5
        self.board[3, 7] = 6
        self.board[4, 8] = 7
        self.board[5, 9] = 8
        self.board[6, 10] = 9
        self.board[7, 11] = 10
        self.board[7, 12] = 11
        self.board[8, 12] = 12
        self.board[8, 13] = 13
        self.board[9, 13] = 14
        self.board[9, 14] = 15
        self.board[10, 14] = 16
        self.board[10, 15] = 17
        self.board[11, 16] = 18
        self.board[12, 17] = 19
        self.board[13, 18] = 20
        self.board[14, 19] = 21
        self.board[15, 20] = 22
        self.board[16, 21] = 23
        self.board[16, 22] = 24
        self.board[17, 22] = 25
        self.board[17, 23] = 26
        self.board[18, 23] = 27
        self.board[18, 24] = 28
        self.board[19, 24] = 29
        self.board[19, 25] = 30
        self.board[20, 25] = 31
        self.board[20, 26] = 32
        self.board[21, 27] = 33
        self.board[22, 28] = 34
        self.board[23, 29] = 35
        self.board[24, 30] = 36
        self.board[25, 31] = 37
        self.board[26, 32] = 38
        self.board[27, 33] = 39
        self.board[28, 33] = 40
        self.board[28, 34] = 41
        self.board[29, 34] = 42
        self.board[29, 35] = 43
        self.board[30, 35] = 44
        self.board[30, 36] = 45
        self.board[31, 36] = 46
        self.board[31, 37] = 47
        self.board[32, 37] = 48
        self.board[33, 38] = 49
        self.board[34, 39] = 50
        self.board[35, 40] = 51
        self.board[36, 41] = 52
        self.board[37, 42] = 53
        self.board[38, 43] = 54
        self.board[39, 43] = 55
        self.board[39, 44] = 56
        self.board[40, 44] = 57
        self.board[40, 45] = 58
        self.board[41, 45] = 59
        self.board[41, 46] = 60
        self.board[42, 46] = 61
        self.board[43, 47] = 62
        self.board[44, 48] = 63
        self.board[45, 49] = 64
        self.board[46, 50] = 65
        self.board[47, 51] = 66
        self.board[48, 51] = 67
        self.board[48, 52] = 68
        self.board[49, 52] = 69
        self.board[49, 53] = 70
        self.board[50, 53] = 71

        self.board += self.board.transpose()
        print("init_board() done")

    def start_location_and_resources(self):
        """
        Allocate 1 settlement and 1 road for each player to start the game. Also gives each player
        3 of each resource to start. This function is only called during initialization
        """
        print("start_location_and_resources() called")

        for player in self.players:
            player.brick += 4
            player.wood += 4
            player.wheat += 4
            player.sheep += 4
            player.stone += 4

        self.assign_vertex(12, self.players[0])
        self.assign_edge(12, self.players[0])
        self.assign_vertex(14, self.players[1])
        self.assign_edge(15, self.players[1])
        self.assign_vertex(39, self.players[2])
        self.assign_edge(50, self.players[2])
        self.assign_vertex(41, self.players[3])
        self.assign_edge(59, self.players[3])

        print("start_location_and_resources() done")

    def save_game(self):
        """
        Performs a create/update call to the backend database to store the models
        """
        print("save_game() called")

        # SAVE PLAYERS, TILES, EDGES, AND VERTICES
        for player in self.players:
            #print("Saving player %s" % player.name)
            player.save()

        for tile in self.tiles:
            #print("Saving tile of resource %s, dice val %d" % (tile.resource_type, tile.dice_value))
            tile.save()

        for edge in self.edges:
            edge.save()

        for vertex in self.vertices:
            vertex.save()

        print("save_game() done")

    def load_game(self):
        """

        """
        print("load_game() called")

        self.players = list(catan.Player.objects.all())
        self.tiles = list(catan.Tile.objects.all())
        self.edges = list(catan.Edge.objects.all())
        self.vertices = list(catan.Vertex.objects.all())

        self.init_tiles()
        self.init_board()

        print("load_game() done")

    def pickle(self):
        """Pickle the Game object, lazy save"""
        print("pickle() called")
        joblib.dump(self.__dict__, "save_game.pkl")
        print("pickle() done")

    def unpickle(self):
        """Unpickle Game object, lazy load"""
        print("unpickle() called")
        joblib.load("save_game.pkl")
        print("unpickle() done")

    def assign_vertex(self, vertex_id, player):
        """
        Functional equivalent of a player building a settlement on a vertex
        Resources are deducted from the player
        Vertex and all neighboring vertices are made unavailable
        1 victory point is given to the player
        :param vertex_id: ID of the vertex model to be claimed
        :param player: player model building the settlement
        """
        print("assign_vertex() called, assigning vertex", vertex_id, "to Player", player.id)

        # assign vertex to player and give victory point
        player.vertex_set.add(self.vertices[vertex_id])
        player.victory_points += 1

        # make vertex and neighboring vertices unavailable
        self.vertices[vertex_id].available = False
        vertex_slice = self.board[vertex_id, :]
        neighbor_vertex_ids = np.where(vertex_slice != 0)
        for v_id in neighbor_vertex_ids[0]:
            print("making neighbor vertex", v_id, "unavailable")
            self.vertices[v_id].available = False

        # deduct resources
        player.brick -= 1
        player.wood -= 1
        player.wheat -= 1
        player.sheep -=1

        print("assign_vertex() done")

    def assign_edge(self, edge_id, player):
        """
        Functional equivalent of a player building a road on an edge
        Resources are deducted from the player
        Edge is made unavailable
        :param edge_id: ID of the edge model to be claimed
        :param player: player model building the road
        """
        print("assign_edge() called, assigning edge", edge_id, "to Player", player.id)

        player.edge_set.add(self.edges[edge_id])
        self.edges[edge_id].available = False
        player.brick -= 1
        player.wood -= 1

        print("assign_edge() done")

    def roll_dice(self):
        return random.randint(1,6) + random.randint(1,6)

    def start_turn(self):
        """
        Simulate the dice roll and allocate resources to all players.
        Allow the current player to build roads, settlements, and cities as desired.
        Will eventually implement trading functionality and dev cards
        """
        print("start_turn() called")

        print("Current player's turn:", self.turn)
        print("Rolling dice...")
        roll = self.roll_dice()
        print("You rolled a: ", roll)

        if roll != 7:
            self.distribute_resources(roll)
        else:
            self.move_robber()

        self.display_player(self.players[self.turn])

        self.display_resources(self.players[self.turn])

        choice = input("Would you like to build (b), trade(t), buy dev card (d), or pass (p)?")
        while choice not in ('b', 't', 'd', 'p'):
            choice = input("Would you like to build (b), trade(t), buy dev card (d), or pass (p)?")

        if choice == 'p':
            pass
        elif choice == 'b':
            while self._build() != 0:
                pass
        elif choice == 't':
            print("Not implemented")
        elif choice == 'd':
            print("Not implemented")


        if self.players[self.turn].victory_points >= 10:
            self.winner = True
            print("***We Have A Winner***")
            print("***Congrats Player", self.players[self.turn].id, "***")
            exit(0)

        self.save_game()

        print("start_turn() done")

    def display_tiles(self):
        """
        Display current tiles, their dice values, and the resource they provide
        """
        print("****************************************")
        for tile in self.tiles:
            print("Tile", tile.id, "has dice value:", tile.dice_value, "and provides resource:", tile.resource_type)
        print("****************************************")

    def display_player(self, player):
        """
        Display current player's victory points, roads, and settlements/cities
        :param player: current player's turn
        """
        print("****************************************")
        print("Player", player.id, "has:")
        print(player.victory_points, "victory points")
        print("The following roads: ")
        for edge in player.edge_set.all():
            print(edge.id)
        print("The following settlements/cities")
        for vertex in player.vertex_set.all():
            if vertex.has_city:
                print(vertex.id, "city")
            else:
                print(vertex.id, "settlement")
        print("****************************************")

    def display_resources(self, player):
        """
                Display current player's resources
                :param player: current player's turn
                """
        print("****************************************")
        print("Player", player.id, "has:")
        print(player.brick, "brick")
        print(player.wood, "wood")
        print(player.wheat, "wheat")
        print(player.sheep, "sheep")
        print(player.stone, "stone")
        print("****************************************")

    def _build(self):
        """
        Heavy lifting function which prompts players to make a build selection.
        All options other than pass (p) will result in a non-zero build_flag which will simply prompt
        another call to _build. This allows players to build multiple things per turn.
        This function checks player resources for the thing to be built. If adequate, the function makes calls
        to assign_edge and assign_vertex depending on if a road or settlement is being built.
        If a city is being built, this function handles that by giving the player a victory point and changing
        the has_city attribute of the vertex to True.
        :return:
        """
        print("_build called")

        build_flag = 1
        build_choice = input("What would you like to build? road (r), settlement (s), city (c), pass (p)")

        # for each option display list of possible build locations as per game rules
        # check if resources are available for the build
        # update victory points if needed
        if build_choice == 'r':
            build_flag = self._build_road()

        elif build_choice == 's':
            build_flag = self._build_settlement()

        elif build_choice == 'c':
            build_flag = self._build_city()

        elif build_choice == 'p':
            build_flag = 0

        print("_build() done. Returning with flag", build_flag)
        return build_flag

    def _build_road(self):
        """
        Helper function to build road
        :return: build_flag
        """
        player = self.players[self.turn]
        build_flag = 1

        # check player resources are adequate
        if player.wood < 1 or player.brick < 1:
            print("Not enough resources to build a road")
            build_flag = 2

        else:
            active_v = []
            for edge in player.edge_set.all():
                # print(edge)
                active_v_ids = np.where(self.board == edge.id)
                # print(active_v_ids[0][0], active_v_ids[0][1])
                active_v.append(active_v_ids[0][0])
                active_v.append(active_v_ids[1][0])

            locations = []
            for vertex_id in active_v:
                for edge_id in self.board[vertex_id, :]:
                    if edge_id != 0 and self.edges[int(edge_id)].available:
                        locations.append(int(edge_id))

            # print(locations, type(locations), type(locations[0]))
            locations = list(set(locations))

            print("List of possible road locations: ")
            for location in locations:
                print(location, type(location))

            location_choice = int(input("Where would you like to build a road?"))
            while location_choice not in locations:
                print("Invalid location")
                location_choice = int(input("Where would you like to build a road?"))
            # assign edge/road to player
            self.assign_edge(location_choice, player)

        return build_flag

    def _build_settlement(self):
        """
        Helper function to build settlements
        :return: build_flag
        """
        player = self.players[self.turn]
        build_flag = 1

        # check player resources are adequate
        if player.brick < 1 or player.wood < 1 or player.wheat < 1 or player.sheep < 1:
            print("Not enough resources to build a settlement")
            build_flag = 2

        # generate list of available vertices
        else:
            active_v = []
            for edge in player.edge_set.all():
                print(edge.id)
                active_v_ids = np.where(self.board == edge.id)
                print(active_v_ids)
                active_v.append(active_v_ids[0][0])
                active_v.append(active_v_ids[1][0])

            active_v = list(set(active_v))

            locations = []
            for vertex_id in active_v:
                if self.vertices[vertex_id].available:
                    locations.append(vertex_id)

            # if no places to build settlement, set build_flag
            if len(locations) == 0:
                print("No valid places to build a settlement")
                build_flag = 3

            else:
                print("List of possible settlement locations: ")
                for location in locations:
                    print(location)

                # prompt user for build location
                location_choice = int(input("Where would you like to build a settlement?"))
                while location_choice not in locations:
                    print("Invalid location")
                    location_choice = int(input("Where would you like to build a settlement?"))

                # assign vertex/settlement to player
                self.assign_vertex(location_choice, player)

        return build_flag

    def _build_city(self):
        """
        Helper function to build city
        :return: build_flag
        """
        player = self.players[self.turn]
        build_flag = 1

        # check resources
        if player.wheat < 2 or player.stone < 3:
            print("Not enough resources to build a city")
            build_flag = 2

        else:
            locations = [vertex.id for vertex in player.vertex_set.filter(has_city=False)]
            for location in locations:
                print(location)

            location_choice = int(input("Where would you like to upgrade to a city?"))
            while location_choice not in locations:
                print("Invalid location")
                location_choice = input("Where would you like to upgrade to a city?")

            else:
                self.vertices[location_choice].has_city = True
                player.victory_points += 1
                print("Player", player.id, "upgraded settlement", location_choice, "to a city")

        return build_flag

    def move_robber(self):
        print("Not implemented")

    def distribute_resources(self, roll):
        """
        Given a dice roll value, will find all tiles that have that dice value,
        then find all vertices which have a settlement. For each vertex with settlement,
        a helper function _pay_player is called with the player, resource_type, and has_city
        as arguments
        :param roll: integer value of dice roll (2-12)
        """
        print("distribute_resources() called")

        # find all tiles with the dice value
        active_tiles = [tile for tile in self.tiles if tile.dice_value == roll]

        for tile in active_tiles:
            resource_type = tile.resource_type
            active_vertices = [vertex for vertex in tile.vertex.all() if vertex.settlement is not None]

            for vertex in active_vertices:
                player = vertex.settlement
                self._pay_player(player, resource_type, vertex.has_city)

        print("distribute_resources() done")

    def _pay_player(self, player, resource_type, has_city):
        """
        Helper function which assigns resources to players based on the resource type
        and absence/presence of city. This function does not verify that the player owns
        a given vertex and it is up to the calling function to make those checks
        :param player: Player model to give resources
        :param resource_type: String variable denoting resource type of the tile
        :param has_city: Boolean variable denoting whether or not there is a city
        """
        #print("_pay_player() called")

        if has_city:
            multiplier = 2
        else:
            multiplier = 1

        if resource_type == "brick":
            player.brick += multiplier
        elif resource_type == "wood":
            player.wood += multiplier
        elif resource_type == "wheat":
            player.wheat += multiplier
        elif resource_type == "sheep":
            player.sheep += multiplier
        elif resource_type == "stone":
            player.stone += multiplier
        else:
            print("Invalid resource_type specified")

        print("Player ", player.id, " gets ", multiplier, resource_type)

        #print("_pay_player() done")


if __name__ == "__main__":

    print(os.getcwd())
    random.seed = 0

    resources = [u"brick", u"brick", u"brick",
                 u"wood", u"wood", u"wood", u"wood",
                 u"wheat", u"wheat", u"wheat", u"wheat",
                 u"sheep", u"sheep", u"sheep", u"sheep",
                 u"stone", u"stone", u"stone"]

    resource_vals = [2, 3, 3, 4, 4, 5, 5, 6, 6, 8, 8, 9, 9, 10, 10, 11, 11, 12]
    #print(len(resource_vals), len(resources))

    sim = Game()

    choice = input("Start new game (n) or load previous game (l)")
    while choice not in ('n', 'l'):
        choice = input("Start new game (n) or load previous game (l)")

    if choice == 'n':
        sim.initialize()

    elif choice == 'l':
        sim.load_game()
        for player in sim.players:
            sim.display_player(player)
            sim.display_resources(player)
        for edge in sim.edges:
            print(edge)
        for vertex in sim.vertices:
            print(vertex)
        for tile in sim.tiles:
            print(tile)

    print("********Game starting********")
    sim.display_tiles()
    while sim.winner == False:
        # sim.winner = True
        if sim.turn > 4:
            sim.turn = 0
        sim.start_turn()

        sim.turn += 1
        sim.turn_count += 1
        _ = input(">>Press Enter for next Turn, or 'X' to exit")

        if _ == 'X':
            exit(0)

