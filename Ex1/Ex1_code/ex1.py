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

RED_COIN = RED + 1
BLUE_COIN = BLUE + 1
YELLOW_COIN = YELLOW + 1
GREEN_COIN = GREEN + 1
REGULAR_SLOT_NO_COIN = 10
REGULAR_SLOT_COIN = 11
WALL = 99
INTMAX = 2147483647

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

    def deep_copy_dict(self, dict: dict):
        """ this function creates a deep copy of a python dictionary """
        new_dict = {}
        for key,value in dict.items():
            new_dict[key] = value
        return new_dict

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
        locations: dict[str, tuple] = {}
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

    def modify_state_tuple(self, state, new_positions: dict):
        """ Modify the state of the tuple with the given changes dictionary """
        modified = list(map(list, state))  # Convert to list of lists for mutability
        for (i, j), value in new_positions.items():
            modified[i][j] = value
        return tuple(map(tuple, modified))


    def ghost_can_move_pos(self, state, new_locations: dict, curr_ghost_color, new_ghost_pos):
        """ Check if the ghost of color curr_ghost can move to new_ghost_pos """
        if state[*new_ghost_pos] == WALL: # check if the new ghost position has a wall
            return False
        for ghost_color_i, new_location in new_locations.items(): # check for any other ghost in new pos
            if ghost_color_i != curr_ghost_color:
                if new_location == new_ghost_pos:
                    return False
        # if there is no wall or other ghost in the new_ghost_pos, current ghost can move there
        return True


    def calculate_ghost_new_pos(self, state, new_locations: dict, curr_ghost_color, n, m):
        """ 
            calculate the nearest position to pacman in hanhatten distance.
            n - number of rows, m - number of columns
        """
        min_dist_to_pacman : tuple = (INTMAX, None)
        ghost_i, ghost_j = new_locations[curr_ghost_color]
        pacman_i, pacman_j = new_locations["PACMAN"]
        # check if can move right
        if self.ghost_can_move_pos(state, new_locations, curr_ghost_color, (ghost_i, ((ghost_j + 1) % m))):
            man_right : int = abs(ghost_i - pacman_i) + abs(((ghost_j + 1) % m) - pacman_j)
            if man_right < min_dist_to_pacman[0]:
                min_dist_to_pacman = (man_right, (ghost_i, ((ghost_j + 1) % m)))
        # check if can move down
        if self.ghost_can_move_pos(state, new_locations, curr_ghost_color, ((ghost_i + 1) % n, ghost_j )):
            man_down : int = abs((ghost_i + 1) % n - pacman_i) + abs(ghost_j - pacman_j)
            if man_down < min_dist_to_pacman[0]:
                min_dist_to_pacman = (man_down, ((ghost_i + 1) % n, ghost_j ))
        # check if can move left
        if self.ghost_can_move_pos(state, new_locations, curr_ghost_color, (ghost_i, ((ghost_j - 1) % m))):
            man_left : int = abs(ghost_i - pacman_i) + abs(((ghost_j - 1) % m) - pacman_j)
            if man_left < min_dist_to_pacman[0]:
                min_dist_to_pacman = (man_left, (ghost_i, ((ghost_j - 1) % m)))
        # check if can move up
        if self.ghost_can_move_pos(state, new_locations, curr_ghost_color, ((ghost_i - 1) % n, ghost_j )):
            man_up : int = abs((ghost_i - 1) % n - pacman_i) + abs(ghost_j - pacman_j)
            if man_up < min_dist_to_pacman[0]:
                min_dist_to_pacman = (man_up, ((ghost_i - 1) % n, ghost_j ))
        # if the ghost cannot move, return without changing the
        if min_dist_to_pacman[0] == INTMAX: 
            return
        # define the new position of the ghost - nearest position with relation to manhatten distance
        new_locations[curr_ghost_color] = min_dist_to_pacman[1]
        
        
        
        

        
    def calculate_new_positions(self, state, player_new_pos, locations, n, m):
        new_positions : dict[tuple, int] = {}
        new_locations: dict[str,tuple] = self.deep_copy_dict(locations)
        new_locations["PACMAN"] = player_new_pos # define the new pacman position in the new state
        # if the red ghost is present in the state
        if new_locations["RED"]:
            self.calculate_ghost_new_pos(new_locations, "RED", n, m)
            if new_locations["RED"] != locations["RED"]: # if the ghost has moved, add relevant positions
                if state[*locations["RED"]] == RED_COIN:
                    new_positions[locations["RED"]] = REGULAR_SLOT_COIN
                else # if the ghost can move, it is because its next position is either 11 or 10
                    new_positions[locations["RED"]] = REGULAR_SLOT_NO_COIN
                if state[*new_locations["RED"]] == REGULAR_SLOT_COIN:
                    new_positions[new_locations["RED"]] = RED_COIN
                else:
                    new_positions[new_locations["RED"]] = RED
        # if the blue ghost is present in the state
        if new_locations["BLUE"]:
            self.calculate_ghost_new_pos(new_locations, "BLUE", n, m)
            if new_locations["BLUE"] != locations["BLUE"]: # if the ghost has moved, add relevant positions
                if state[*locations["BLUE"]] == BLUE_COIN:
                    new_positions[locations["BLUE"]] = REGULAR_SLOT_COIN
                else # if the ghost can move, it is because its next position is either 11 or 10
                    new_positions[locations["BLUE"]] = REGULAR_SLOT_NO_COIN
                if state[*new_locations["BLUE"]] == REGULAR_SLOT_COIN:
                    new_positions[new_locations["BLUE"]] = BLUE_COIN
                else:
                    new_positions[new_locations["BLUE"]] = BLUE
        # if the yellow ghost is present in the state
        if new_locations["YELLOW"]:
            self.calculate_ghost_new_pos(new_locations, "YELLOW", n, m)
            if new_locations["YELLOW"] != locations["YELLOW"]: # if the ghost has moved, add relevant positions
                if state[*locations["YELLOW"]] == YELLOW_COIN:
                    new_positions[locations["YELLOW"]] = REGULAR_SLOT_COIN
                else # if the ghost can move, it is because its next position is either 11 or 10
                    new_positions[locations["YELLOW"]] = REGULAR_SLOT_NO_COIN
                if state[*new_locations["YELLOW"]] == REGULAR_SLOT_COIN:
                    new_positions[new_locations["YELLOW"]] = YELLOW_COIN
                else:
                    new_positions[new_locations["YELLOW"]] = YELLOW
        # if the green ghost is present in the state
        if new_locations["GREEN"]:
            self.calculate_ghost_new_pos(new_locations, "GREEN", n, m)
            if new_locations["GREEN"] != locations["GREEN"]: # if the ghost has moved, add relevant positions
                if state[*locations["GREEN"]] == GREEN_COIN:
                    new_positions[locations["GREEN"]] = REGULAR_SLOT_COIN
                else # if the ghost can move, it is because its next position is either 11 or 10
                    new_positions[locations["GREEN"]] = REGULAR_SLOT_NO_COIN
                if state[*new_locations["GREEN"]] == REGULAR_SLOT_COIN:
                    new_positions[new_locations["GREEN"]] = GREEN_COIN
                else:
                    new_positions[new_locations["GREEN"]] = GREEN
        # return the new positions that need to be changed in the state
        return new_positions


    def successor(self, state):
        """ Generates the successor state """
        n : int = len(state) # number of rows
        m : int = len(state[0]) # number of columns
        successor_state_list = []
        # find the locations of pacman and the ghosts
        locations: dict[str,tuple] = self.find_locations(state, n, m)
        # define the resulting states
        moves_and_states = list[str,tuple]
        # define a resulting state for each move that pacman can make
        player_i, player_j = locations["PACMAN"]
        if state[(player_i + 1) % n][player_j] != WALL: # add state of pacman moving down (circular movement if no walls are present)
            moves_and_states.append(("D", self.modify_state_tuple(state, self.calculate_new_positions(state, ((player_i + 1) % n, player_j), locations, n, m))))
        if state[(player_i - 1) % n][player_j] != WALL:# add state of pacman moving up (circular movement if no walls are present)
            moves_and_states.append(("U", self.modify_state_tuple(state, self.calculate_new_positions(state, ((player_i - 1) % n, player_j), locations, n, m))))
        if state[player_i][(player_j + 1) % m] != WALL:# add state of pacman moving right (circular movement if no walls are present)
            moves_and_states.append(("R", self.modify_state_tuple(state, self.calculate_new_positions(state, (player_i, (player_j + 1) % m), locations, n, m))))
        if state[player_i][(player_j - 1) % m] != WALL:# add state of pacman moving left (circular movement if no walls are present)
            moves_and_states.append(("L", self.modify_state_tuple(state, self.calculate_new_positions(state, (player_i, (player_j) - 1 % m), locations, n, m))))
        
        return moves_and_states

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
