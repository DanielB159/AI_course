import search
import math
import utils

id=315113159

""" Rules """
RED = 20
BLUE = 30
YELLOW = 40
GREEN = 50
PACMAN = 77

class PacmanProblem(search.Problem):
    """This class implements a pacman problem"""
    def __init__(self, initial):
        """ Magic numbers for ghosts and Packman: 
        2 - red, 3 - blue, 4 - yellow, 5 - green and 7 - Packman.""" 

        self.locations = dict.fromkeys((7, 2, 3, 4, 5))
        self.dead_end = False

        """ Constructor only needs the initial state.
        Don't forget to set the goal or implement the goal test"""
        search.Problem.__init__(self, initial)

    def find_player_state(self, state, N, M) -> tuple:
        """ finds the (i,j) location of the player in the currents state. None if there is no player """
        for i in range(N):
            for j in range(M):
                if state[i][j] == 77:
                    return (i,j)
        return None
    
    def find_locations(self, state, n, m) -> dict[tuple]:
        """
            finds the (i,j) locations of ghosts and pacman in the currents state.
            returns mapping from "RED", "BLUE", "YELLOW", "GREEN", "PACMAN" to corresponding locations
        """
        locations: dict = {}
        for i in range(n):
            for j in range(m):
                match state[i][j]:
                    case 77:
                        locations["PACMAN"] = (i,j)
                    case 51:
                        locations["GREEN"] = (i,j)
                    case 50:
                        locations["GREEN"] = (i,j)
                    case 41:
                        locations["YELLOW"] = (i,j)
                    case 40:
                        locations["YELLOW"] = (i,j)
                    case 31:
                        locations["BLUE"] = (i,j)
                    case 30:
                        locations["BLUE"] = (i,j)
                    case 21:
                        locations["RED"] = (i,j)
                    case 20:
                        locations["RED"] = (i,j)
                    case _:
                        pass
        return locations

                
    def successor(self, state):
        """ Generates the successor state """
        n : int = len(state) # number of rows
        m : int = len(state[0]) # number of columns
        successor_state_list = []
        # find the locations of pacman and the ghosts
        locations: dict[tuple] = self.find_locations(state, n, m)
        # define the resulting states
        moves_and_states = list[str,tuple]
        # define a resulting state for each move that pacman can make
        player_i, player_j = locations["PACMAN"]
        if state[player_i + 1][player_j] != 

            

        
        # utils.raiseNotDefined()

    def result(self, state, move):
        """given state and an action and return a new state"""
        pass
        # utils.raiseNotDefined()
    
    def goal_test(self, state):
        """ given a state, checks if this is the goal state, compares to the created goal state"""
        pass
        # utils.raiseNotDefined()
        
    def h(self, node):
        """ This is the heuristic. It get a node (not a state)
        and returns a goal distance estimate"""
        pass
        # utils.raiseNotDefined()

def create_pacman_problem(game):
    print ("<<create_pacman_problem")
    """ Create a pacman problem, based on the description.
    game - matrix as it was described in the pdf file"""
    return PacmanProblem(game)

game =()


create_pacman_problem(game)
