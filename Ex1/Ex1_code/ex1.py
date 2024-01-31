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
                COINS,
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

    # def find_player_state(self, state, N, M) -> tuple:
    #     """finds the (i,j) location of the player in the currents state. None if there is no player"""
    #     for i in range(N):
    #         for j in range(M):
    #             if state[i][j] == 77:
    #                 return (i, j)
    #     return None

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
        # find the amount of coins in the state
        # coins: int = 0
        # for row in state:
        #     for item in row:
        #         if item % 10 == 1:
        #             coins += 1

        for i in range(n):
            for j in range(m):
                match (state[i][j] // 10):
                    case 8:
                        self.locations[DEAD_PACMAN_CHARACTER] = (i, j)
                    case 7:
                        self.locations[PACMAN_CHARACTER] = (i, j)
                    case 5:
                        self.locations[GREEN_GHOST] = (i, j)
                        # if state[i][j] % 10 == 1:
                        #     coins += 1
                    case 4:
                        self.locations[YELLOW_GHOST] = (i, j)
                        # if state[i][j] % 10 == 1:
                        #     coins += 1
                    case 3:
                        self.locations[BLUE_GHOST] = (i, j)
                        # if state[i][j] % 10 == 1:
                        #     coins += 1
                    case 2:
                        self.locations[RED_GHOST] = (i, j)
                        # if state[i][j] % 10 == 1:
                        #     coins += 1
                    case _:
                        pass
                        # if state[i][j] % 10 == 1:
                            # coins += 1
        # self.locations[COINS] = coins

    def modify_state_tuple(self, state, new_positions: dict):
        """Modify the state of the tuple with the given changes dictionary"""
        modified = list(map(list, state))  # Convert to list of lists for mutability
        for (i, j), value in new_positions.items():
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
        ghost_cell = state[new_ghost_pos[0]][new_ghost_pos[1]]
        if (
            ghost_cell != PACMAN
            and ghost_cell != REGULAR_CELL_COIN
            and ghost_cell != REGULAR_CELL_NO_COIN
        ):  # check if the new position has anything but pacman or a ghost-less cell
            # if so, check if it is a wall. if so, the ghost cannot move there
            if ghost_cell == WALL:
                return False
            # otherwise, it is another ghost. check if it has moved already in new locations
            for ghost_color_i, location_i in self.locations.items():
                if location_i == new_ghost_pos:
                    # if the ghost in the new position has not moved anywhere, current ghost cannot move
                    if new_locations[ghost_color_i] == location_i:
                        return False
        # check if the new locations have a ghost in new_ghost_pos
        for (
            ghost_color_i,
            new_location,
        ) in new_locations.items():  # check for any other ghost in new pos
            if ghost_color_i != curr_ghost_color and ghost_color_i != PACMAN_CHARACTER:
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
        old_chost_color = self.locations[ghost_color]
        
        if (
            new_ghost_color != old_chost_color
        ):  # if the ghost has moved, add relevant positions
            if (
                state[old_chost_color[0]][old_chost_color[1]]
                == ghost_coin
            ):
                new_positions[old_chost_color] = REGULAR_CELL_COIN
            else:  # if the ghost can move, its former position was either with coin or without coin
                new_positions[old_chost_color] = REGULAR_CELL_NO_COIN
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
        # locations: dict[str, tuple]
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
            moves_and_states.append(("D", self.result(state, "D")))
        if (
            player_i - 1 >= 0 and state[player_i - 1][player_j] != WALL
        ):  # add state of pacman moving up
            moves_and_states.append(("U", self.result(state, "U")))
        if (
            player_j + 1 < m and state[player_i][player_j + 1] != WALL
        ):  # add state of pacman moving right
            moves_and_states.append(("R", self.result(state, "R")))
        if (
            player_j - 1 >= 0 and state[player_i][player_j - 1] != WALL
        ):  # add state of pacman moving left
            moves_and_states.append(("L", self.result(state, "L")))

        return moves_and_states

    def result(self, state, move):
        """given state and an action and return a new state"""
        n: int = len(state)  # number of rows
        m: int = len(state[0])  # number of columns
        # find the locations of pacman and the ghosts
        # locations: dict[str, tuple]
        self.find_locations(state, n, m)
        # make sure that pacman is in the map
        if self.locations[PACMAN_CHARACTER] is None:
            return state
        player_i, player_j = self.locations[PACMAN_CHARACTER]
        player_i_new: int = None
        player_j_new: int = None
        # calculate the new (i,j) location of pacman
        match move:
            case "R":
                player_i_new = player_i
                player_j_new = player_j + 1
                if player_j_new >= m:
                    return state
            case "L":
                player_i_new = player_i
                player_j_new = player_j - 1
                if player_j_new < 0:
                    return state
            case "U":
                player_i_new = player_i - 1
                player_j_new = player_j
                if player_i_new < 0:
                    return state
            case "D":
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
        # locations: dict[str, tuple]
        self.find_locations(state, n, m)
        coins = len(self.locations[COINS_LOCATIONS])
        if (
            coins == 0
            and self.locations[PACMAN_CHARACTER] is not None
            and self.locations[DEAD_PACMAN_CHARACTER] is None
        ):
            return True
        return False

        # utils.raiseNotDefined()

    def h_coin_weighed_sum(self, state, n, m, pacman_i, pacman_j):
        """Finding the locations of the ghosts and of the coins. doing a weighed sum of the coins"""
        furthest_distance: int = 0
        coin_weighed_sum: int = 0

        # make the manhatten distance matrix and find the coin with the maximum distance distance from pacman
        for i in range(n):
            for j in range(m):
                item = state[i][j]
                if item % 10 == 1:
                    distance = abs(i - pacman_i) + abs(j - pacman_j)
                    coin_weighed_sum += distance
                    if distance > furthest_distance:
                        furthest_distance = distance
        if coin_weighed_sum == 0:
            return 0

        return coin_weighed_sum / furthest_distance

    def h_ghost_sum(self, state, n, m, pacman_i, pacman_j):
        ghost_set = {20, 21, 30, 31, 40, 41, 50, 51}
        near_ghost_sum = 0
        for i in range(-2, 3):
            for j in range(-2, 3):
                index_i, index_j = (pacman_i + i), (pacman_j + j)
                if index_i < n and index_i >= 0 and index_j < m and index_j >= 0:
                    if state[index_i][index_j] in ghost_set:
                        near_ghost_sum += abs(pacman_i - index_i) + abs(
                            pacman_j - index_j
                        )
        return near_ghost_sum

    def find_pacman_new_state(self, new_state, action) -> tuple:
        # check if pacman was in the state prior to this move
        if (
            self.locations[PACMAN_CHARACTER] is None
            or self.locations[DEAD_PACMAN_CHARACTER] is not None
        ):
            return (-1, -1)
        pacman_i, pacman_j = self.locations[PACMAN_CHARACTER]
        pacman_i_new: int
        pacman_j_new: int
        # find the new state of pacman
        match action:
            case "R":
                pacman_i_new = pacman_i
                pacman_j_new = pacman_j + 1
            case "D":
                pacman_i_new = pacman_i + 1
                pacman_j_new = pacman_j
            case "L":
                pacman_i_new = pacman_i
                pacman_j_new = pacman_j - 1
            case "U":
                pacman_i_new = pacman_i - 1
                pacman_j_new = pacman_j
        if new_state[pacman_i_new][pacman_j_new] != 77:
            return (-1, -1)
        return (pacman_i_new, pacman_j_new)

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
        # pacman_i_new, pacman_j_new = self.find_pacman_new_state(state, node.action)
        if self.locations[PACMAN_CHARACTER] is None:
            return INFINITY
        pacman_i_new, pacman_j_new = self.locations[PACMAN_CHARACTER]
        
        # if pacman_i_new == -1:
        #     return INFINITY
        coin_locations = self.locations[COINS_LOCATIONS]
        coins = len(coin_locations)
        # make the heuristic goal aware
        if coins == 0:
            return 0
        
        # find the max distance from a coin to another coin
        # max_coin_distance, coin1, coin2 = 0, None, None
        # for i in range(len(coins_in_state)):
        #     for j in range(i + 1, len(coins_in_state)):
        #         distance = abs(coins_in_state[i][0] - coins_in_state[j][0]) + abs(
        #             coins_in_state[i][1] - coins_in_state[j][1]
        #         )
        #         if distance > max_coin_distance:
        #             max_coin_distance = distance
        #             coin1 = coins_in_state[i]
        #             coin2 = coins_in_state[j]
        # # calculate the minimum distance from pacman to coin 1 and coin 2
        # min_coin1_distance = abs(coin1[0] - pacman_i_new) + abs(coin1[1] - pacman_j_new)
        # min_coin2_distance = abs(coin2[0] - pacman_i_new) + abs(coin2[1] - pacman_j_new)
        # min_coin_distance_from_pacman = min(min_coin1_distance, min_coin2_distance)
        # return min_coin_distance_from_pacman + max_coin_distance

        # check if in this state pacman has eaten a coin
        if self.locations[STATE][pacman_i_new][pacman_j_new] % 10 == 1:
            coins -= 1
        # if coins == 0:
        #     return coins
        # return coins
        # calculate thefurthest manhatten distance coin and the shortest manhatten distance coin
        furthest_distance: int = 0
        # make the manhatten distance matrix and find the coin with the maximum distance distance from pacman
        for (i, j) in coin_locations:
            distance = abs(i - pacman_i_new) + abs(j - pacman_j_new)
            if distance > furthest_distance:
                furthest_distance = distance
        
        # for i in range(n):
        #     for j in range(m):
        #         item = state[i][j]
        #         if item % 10 == 1:
        #             distance = abs(i - pacman_i_new) + abs(j - pacman_j_new)
        #             if distance > furthest_distance:
        #                 furthest_distance = distance
        #             if distance < shortest_distance:
        #                 shortest_distance = distance
                    # distance_sum += abs(i - pacman_i) + abs(j - pacman_j)
        # for i in range(n):
        #     for j in range(m):
        #         item = state[i][j]
        #         if item % 10 == 1:
        #             distance = abs(i - pacman_i_new) + abs(j - pacman_j_new)
        #             coin_weighed_sum += distance

        return max(furthest_distance, coins)
        # keep the heuristic goal aware
        # if coins == 0:
        #     return 0
        # return coins
        # coins_weighed_sum = self.h_coin_weighed_sum(state, n, m, pacman_i, pacman_j)
        # if coins == 0:
        #     return 0
        # return  self.h_ghost_sum(state, n, m, pacman_i, pacman_j)
        # utils.raiseNotDefined()


def create_pacman_problem(game):
    print("<<create_pacman_problem")
    """ Create a pacman problem, based on the description.
    game - matrix as it was described in the pdf file"""
    return PacmanProblem(game)


game = ()


create_pacman_problem(game)
