import search
import math
import utils

id = 315113159

""" Rules """
# state indexes
RED = 20
BLUE = 30
YELLOW = 40
GREEN = 50
PACMAN = 77

RED_COIN = RED + 1
BLUE_COIN = BLUE + 1
YELLOW_COIN = YELLOW + 1
GREEN_COIN = GREEN + 1
REGULAR_CELL_NO_COIN = 10
REGULAR_CELL_COIN = 11
WALL = 99
INTMAX = 2147483647
INFINITY = utils.infinity
DEAD_PACMAN = 88

# character indexes
PACMAN_CHARACTER = 7
DEAD_PACMAN_CHARACTER = 8
RED_GHOST = 2
BLUE_GHOST = 3
YELLOW_GHOST = 4
GREEN_GHOST = 5
COINS = 10
STATE = 12
COINS_LOCATIONS = 13


class PacmanProblem(search.Problem):
    """This class implements a pacman problem"""

    def __init__(self, initial):
        """Magic numbers for ghosts and Packman:
        2 - red, 3 - blue, 4 - yellow, 5 - green and 7 - Packman."""

        self.locations = dict.fromkeys(
            (
                PACMAN_CHARACTER,
                DEAD_PACMAN_CHARACTER,
                GREEN_GHOST,
                BLUE_GHOST,
                RED_GHOST,
                YELLOW_GHOST,
                STATE,
                COINS_LOCATIONS
            )
        )
        self.dead_end = False

        """ Constructor only needs the initial state.
        Don't forget to set the goal or implement the goal test"""
        search.Problem.__init__(self, initial)

    def deep_copy_dict(self, dict: dict):
        """this function creates a deep copy of a python dictionary"""
        new_dict = {}
        for key, value in dict.items():
            new_dict[key] = value
        return new_dict


    def find_locations(self, state, n, m):
        """
        finds the (i,j) locations of ghosts and pacman in the currents state.
        returns mapping from "RED", "BLUE", "YELLOW", "GREEN", "PACMAN" to corresponding locations
        also returns the number of coins currently in the state
        """
        self.locations[PACMAN_CHARACTER] = None
        self.locations[DEAD_PACMAN_CHARACTER] = None
        self.locations[STATE] = state
        # find the (i,j) locations of all of the coins in the state
        self.locations[COINS_LOCATIONS] = [(i,j) for i in range(n) for j in range(m) if state[i][j] % 10 == 1]

        for i in range(n):
            for j in range(m):
                comp = (state[i][j] // 10)
                if comp == 8:
                    self.locations[DEAD_PACMAN_CHARACTER] = (i, j)
                elif comp == 7:
                    self.locations[PACMAN_CHARACTER] = (i, j)
                elif comp == 5:
                    self.locations[GREEN_GHOST] = (i, j)
                elif comp == 4:
                    self.locations[YELLOW_GHOST] = (i, j)
                elif comp == 3:
                    self.locations[BLUE_GHOST] = (i, j)
                elif comp == 2:
                    self.locations[RED_GHOST] = (i, j)


    def modify_state_tuple(self, state, new_positions: dict):
        """Modify the state of the tuple with the given changes dictionary"""
        modified = list(map(list, state))  # Convert to list of lists for mutability
        # check the list of new positions if it contains a dead pacman
        # for value in new_positions.values():
        #     if value == DEAD_PACMAN:
        #         return None
        for (i, j), value in new_positions.items():
            if value == DEAD_PACMAN:
                return None
            modified[i][j] = value
        return tuple(map(tuple, modified))

    def ghost_can_move_pos(
        self,
        state,
        new_locations: dict,
        curr_ghost_color,
        new_ghost_pos,
        n,
        m,
    ):
        """Check if the ghost of color curr_ghost can move to new_ghost_pos"""
        # check if the move is in the matrix
        new_ghost_pos_i, new_ghost_pos_j = new_ghost_pos
        if (
            new_ghost_pos_i >= n
            or new_ghost_pos_i < 0
            or new_ghost_pos_j >= m
            or new_ghost_pos_j < 0
        ):
            return False

        # check if new_ghost_pos has anything other than PACMAN or a regular cell
        ghost_new_cell = state[new_ghost_pos[0]][new_ghost_pos[1]]
        if (
            ghost_new_cell != PACMAN
            and ghost_new_cell != REGULAR_CELL_COIN
            and ghost_new_cell != REGULAR_CELL_NO_COIN
        ):  # check if the new position has anything but pacman or a ghost-less cell
            # if so, check if it is a wall. if so, the ghost cannot move there
            if ghost_new_cell == WALL:
                return False
            # otherwise, it is another ghost. check if it has moved already in new locations
            for ghost_color_i, location_i in self.locations.items():
                if location_i == new_ghost_pos and ghost_color_i not in {PACMAN_CHARACTER, DEAD_PACMAN_CHARACTER, COINS_LOCATIONS, STATE}:
                    # if the ghost in the new position has not moved anywhere, current ghost cannot move
                    if new_locations[ghost_color_i] == location_i:
                        return False
        # check if the new locations have a ghost in new_ghost_pos
        for (
            ghost_color_i,
            new_location,
        ) in new_locations.items():  # check for any other ghost in new pos
            if ghost_color_i != curr_ghost_color and ghost_color_i not in {PACMAN_CHARACTER, DEAD_PACMAN_CHARACTER, COINS_LOCATIONS, STATE}:
                if new_location == new_ghost_pos:
                    return False
        # if pacman or regular cell in the next position, ghost can move there
        return True

    def calculate_ghost_new_pos(
        self, state, new_locations: dict, curr_ghost_color, n, m
    ):
        """
        calculate the nearest position to pacman in hanhatten distance.
        n - number of rows, m - number of columns
        """
        min_dist_to_pacman: tuple = (INFINITY, None)
        ghost_i, ghost_j = new_locations[curr_ghost_color]
        pacman_i, pacman_j = new_locations[PACMAN_CHARACTER]
        # check if can move right
        if self.ghost_can_move_pos(
            state,
            new_locations,
            curr_ghost_color,
            (ghost_i, ghost_j + 1),
            n,
            m,
        ):
            man_right: int = abs(ghost_i - pacman_i) + abs(ghost_j + 1 - pacman_j)
            if man_right < min_dist_to_pacman[0]:
                min_dist_to_pacman = (man_right, (ghost_i, ghost_j + 1))
        # check if can move down
        if self.ghost_can_move_pos(
            state,
            new_locations,
            curr_ghost_color,
            (ghost_i + 1, ghost_j),
            n,
            m,
        ):
            man_down: int = abs(ghost_i + 1 - pacman_i) + abs(ghost_j - pacman_j)
            if man_down < min_dist_to_pacman[0]:
                min_dist_to_pacman = (man_down, (ghost_i + 1, ghost_j))
        # check if can move left
        if self.ghost_can_move_pos(
            state,
            new_locations,
            curr_ghost_color,
            (ghost_i, ghost_j - 1),
            n,
            m,
        ):
            man_left: int = abs(ghost_i - pacman_i) + abs(ghost_j - 1 - pacman_j)
            if man_left < min_dist_to_pacman[0]:
                min_dist_to_pacman = (man_left, (ghost_i, ghost_j - 1))
        # check if can move up
        if self.ghost_can_move_pos(
            state,
            new_locations,
            curr_ghost_color,
            (ghost_i - 1, ghost_j),
            n,
            m,
        ):
            man_up: int = abs(ghost_i - 1 - pacman_i) + abs(ghost_j - pacman_j)
            if man_up < min_dist_to_pacman[0]:
                min_dist_to_pacman = (man_up, (ghost_i - 1, ghost_j))
        # if the ghost cannot move, return without changing the
        if min_dist_to_pacman[0] == INFINITY:
            return
        # define the new position of the ghost - nearest position with relation to manhatten distance
        new_locations[curr_ghost_color] = min_dist_to_pacman[1]

    def add_positions(
        self,
        state,
        new_positions,
        new_locations,
        ghost_color,
        ghost_coin,
        ghost_no_coin,
        n,
        m,
    ):
        """Calculate the new positions to update in the next state and add them to new_positions"""
        self.calculate_ghost_new_pos(state, new_locations, ghost_color, n, m)
        new_ghost_color = new_locations[ghost_color]
        old_ghost_color = self.locations[ghost_color]
        
        if (
            new_ghost_color != old_ghost_color
        ):  # if the ghost has moved, add relevant positions
            if (
                state[old_ghost_color[0]][old_ghost_color[1]]
                == ghost_coin
            ):
                new_positions[old_ghost_color] = REGULAR_CELL_COIN
            else:  # if the ghost can move, its former position was either with coin or without coin
                new_positions[old_ghost_color] = REGULAR_CELL_NO_COIN
            # check if pacman is in the next ghost's position
            if new_ghost_color == new_locations[PACMAN_CHARACTER]:
                new_positions[new_ghost_color] = DEAD_PACMAN
            elif state[  # check if the next location has a coin and is not pacman
                new_ghost_color[0]
            ][new_ghost_color[1]] in {
                REGULAR_CELL_COIN,
                RED_COIN,
                BLUE_COIN,
                GREEN_COIN,
                YELLOW_COIN,
            }:
                new_positions[new_ghost_color] = ghost_coin
            else:  # if got here it's a regular slot with no coins
                new_positions[new_ghost_color] = ghost_no_coin

    def calculate_new_positions(self, state, player_new_pos, player_old_pos, n, m):
        new_positions: dict[tuple, int] = {}
        # calculate the new state positions of pacman
        new_positions[(player_old_pos[0], player_old_pos[1])] = REGULAR_CELL_NO_COIN
        if (
            state[player_new_pos[0]][player_new_pos[1]] == REGULAR_CELL_COIN
            or state[player_new_pos[0]][player_new_pos[1]] == REGULAR_CELL_NO_COIN
        ):
            new_positions[player_new_pos] = PACMAN
        else:  # if no wall, coin or no coin, then there is a ghost
            new_positions[player_new_pos] = DEAD_PACMAN
        new_locations: dict[str, tuple] = self.deep_copy_dict(self.locations)
        # define the new pacman position in the new state
        new_locations[PACMAN_CHARACTER] = player_new_pos
        # if the red ghost is present in the state
        if new_locations[RED_GHOST] is not None:
            self.add_positions(
                state,
                new_positions,
                new_locations,
                RED_GHOST,
                RED_COIN,
                RED,
                n,
                m,
            )
        # if the blue ghost is present in the state
        if new_locations[BLUE_GHOST] is not None:
            self.add_positions(
                state,
                new_positions,
                new_locations,
                BLUE_GHOST,
                BLUE_COIN,
                BLUE,
                n,
                m,
            )
        # if the yellow ghost is present in the state
        if new_locations[YELLOW_GHOST] is not None:
            self.add_positions(
                state,
                new_positions,
                new_locations,
                YELLOW_GHOST,
                YELLOW_COIN,
                YELLOW,
                n,
                m,
            )
        # if the green ghost is present in the state
        if new_locations[GREEN_GHOST] is not None:
            self.add_positions(
                state,
                new_positions,
                new_locations,
                GREEN_GHOST,
                GREEN_COIN,
                GREEN,
                n,
                m,
            )
        # return the new positions that need to be changed in the state
        return new_positions

    def successor(self, state):
        """Generates the successor state"""
        n: int = len(state)  # number of rows
        m: int = len(state[0])  # number of columns
        # find the locations of pacman and the ghosts
        self.find_locations(state, n, m)
        # define the resulting states
        moves_and_states: list[tuple] = []
        if self.locations[PACMAN_CHARACTER] is None:  # if pacman is dead, no successors
            return moves_and_states
        # define a resulting state for each move that pacman can make
        player_i, player_j = self.locations[PACMAN_CHARACTER]
        if (
            player_i + 1 < n and state[player_i + 1][player_j] != WALL
        ):  # add state of pacman moving down
            res = self.result(state, "D")
            if res is not None:
                moves_and_states.append(("D", res))
        if (
            player_i - 1 >= 0 and state[player_i - 1][player_j] != WALL
        ):  # add state of pacman moving up
            res = self.result(state, "U")
            if res is not None:
                moves_and_states.append(("U", res))
        if (
            player_j + 1 < m and state[player_i][player_j + 1] != WALL
        ):  # add state of pacman moving right
            res = self.result(state, "R")
            if res is not None:
                moves_and_states.append(("R", res))
        if (
            player_j - 1 >= 0 and state[player_i][player_j - 1] != WALL
        ):  # add state of pacman moving left
            res = self.result(state, "L")
            if res is not None:
                moves_and_states.append(("L", res))

        return moves_and_states

    def result(self, state, move):
        """given state and an action and return a new state"""
        n: int = len(state)  # number of rows
        m: int = len(state[0])  # number of columns
        # find the locations of pacman and the ghosts
        self.find_locations(state, n, m)
        # make sure that pacman is in the map
        if self.locations[PACMAN_CHARACTER] is None or self.locations[DEAD_PACMAN_CHARACTER] is not None:
            return state
        player_i, player_j = self.locations[PACMAN_CHARACTER]
        player_i_new: int = None
        player_j_new: int = None
        # calculate the new (i,j) location of pacman
        if move == "R":
            player_i_new = player_i
            player_j_new = player_j + 1
            if player_j_new >= m:
                return state
        elif move == "L":
            player_i_new = player_i
            player_j_new = player_j - 1
            if player_j_new < 0:
                return state
        elif move == "U":
            player_i_new = player_i - 1
            player_j_new = player_j
            if player_i_new < 0:
                return state
        elif move == "D":
            player_i_new = player_i + 1
            player_j_new = player_j
            if player_i_new >= n:
                return state
       
        return self.modify_state_tuple(
            state,
            self.calculate_new_positions(
                state,
                (player_i_new, player_j_new),
                self.locations[PACMAN_CHARACTER],
                n,
                m,
            ),
        )

    def goal_test(self, state):
        """given a state, checks if this is the goal state, compares to the created goal state"""
        n: int = len(state)  # number of rows
        m: int = len(state[0])  # number of columns
        # find the locations of pacman and the ghosts
        self.find_locations(state, n, m)
        coins = len(self.locations[COINS_LOCATIONS])
        if (
            coins == 0
            and self.locations[PACMAN_CHARACTER] is not None
            and self.locations[DEAD_PACMAN_CHARACTER] is None
        ):
            return True
        return False

        # if new_state[pacman_i - 1][pacman]

    def h(self, node):
        """This is the heuristic. It get a node (not a state)
        and returns a goal distance estimate"""
        # find the locations of pacman and the ghosts
        state = node.state
        n: int = len(state)  # number of rows
        m: int = len(state[0])  # number of columns
        self.find_locations(state, n, m)
        # find the locations of pacman and the ghosts
        if self.locations[PACMAN_CHARACTER] is None or self.locations[DEAD_PACMAN_CHARACTER] is not None:
            return INFINITY
        pacman_i_new, pacman_j_new = self.locations[PACMAN_CHARACTER]
        
        coin_locations = self.locations[COINS_LOCATIONS]
        coins = len(coin_locations)
        # make the heuristic goal aware
        if coins == 0:
            return 0
        
        furthest_distance: int = 0
        # find the coin with the maximum distance distance from pacman
        for (i, j) in coin_locations:
            distance = abs(i - pacman_i_new) + abs(j - pacman_j_new)
            if distance > furthest_distance:
                furthest_distance = distance
        
        return max(furthest_distance, coins)


def create_pacman_problem(game):
    print("<<create_pacman_problem")
    """ Create a pacman problem, based on the description.
    game - matrix as it was described in the pdf file"""
    return PacmanProblem(game)


game = ()


create_pacman_problem(game)
