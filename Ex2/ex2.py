import time
import random
import copy
from pacman import Game

id = ["315113159"]

class Controller:
    "This class is a controller for a Pacman game."
    
    def __init__(self, N, M, init_locations, init_pellets, steps):
        """Initialize controller for given game board and number of steps.
        This method MUST terminate within the specified timeout.
        N - board size along the coordinate x
        M - board size along the coordinate y
        init_locations - the locations of ghosts and Pacman in the initial state
        init_locations - the locations of pellets in the initial state
        steps - number of steps the controller will perform
        """
        # initialize the constants of the problem
        self.game : Game = Game(steps, self.create_board(N, M, init_locations, init_pellets))
        self.N = N
        self.M = M
        self.locations = copy.deepcopy(init_locations)
        self.init_locations = copy.deepcopy(init_locations)
        self.pellets = init_pellets
        self.init_pellets = init_pellets
        self.Q = dict()
        self.initial_state : tuple
        # Assume some value of p
        self.p = 0.75
        self.initialize_Q()
        # run the Q_learning algorithm
        self.Q_learning()


    def create_board(self, N, M, locations, pellets):
        """Create the board for the game"""
        board = [[10] * M for _ in range(N)]
        for key, value in locations.items():
            if value is not None:
                if key == 7:
                    board[value[0]][value[1]] = key * 10
                else:
                    board[value[0]][value[1]] = key * 10
        for i, j in pellets:
            if board[i][j] == 10:
                board[i][j] = 11
            else:
                board[i][j] += 1
            
        return tuple([tuple(row) for row in board])



    def create_state(self, locations: dict, pellets: set) -> tuple:
        """Create state tuple based on the locations and the pellets"""
        N = self.N
        M = self.M
        # create the list that will represent the state that locations represents
        state = [[0] * M for _ in range(N)]
        # update the pacman location in the states
        for key, value in locations.items():
            if key == 7:
                state[value[0]][value[1]] = key
        # update the locations of the pellets
        for i, j in pellets:
            curr = state[i][j]
            if curr == 0:
                state[i][j] = 11
            elif 2 <= curr <= 5:
                state[i][j] += 1
        return tuple([tuple(row) for row in state])

    def Q_learning(self):
        """Run the whole Q_Learning algorithm to learn the best policy"""
        # Set the parameters for the Q-learning algorithm
        GAMMA = 0.7
        ALPHA = 0.5
        ITERATIONS = 100000 * 5
        EPSILON = 0.97


        self.game.reset()
        # Run the first step of the algorithm randomly:
        action = random.choice(['L','D','R','U'])
        reward = self.game.update_board(self.game.actions[action])
        state = self.create_state(self.game.locations, self.game.pellets)
        self.Q[(self.initial_state, action)] = (1 - ALPHA) * self.Q[(self.initial_state, action)] + ALPHA*(reward + GAMMA * self.get_max_Q_value(state))

        # Run the algorithm for a limited amount of iterations
        for _ in range(1,ITERATIONS,1):
            if self.game.done:
                self.game.reset()

            # select by an epsilon greedy policy to explore / exploit
            if random.random() < EPSILON:
                action = random.choice(['L','D','R','U'])
            else:
                action = self.get_max_Q_action(state)
            
            # choose the given action to perform with probability p, and a random other action with prob 1-p
            if random.random() > self.p:
                moves = ['L','D','R','U']
                moves.remove(action)
                action = random.choice(moves)
            
            reward = self.game.update_board(self.game.actions[action])

            # get the current state of the game
            new_state = self.create_state(self.game.locations, self.game.pellets)

            # perform the TD-update
            self.Q[(state, action)] = (1 - ALPHA) * self.Q[(state, action)] + ALPHA * (reward + GAMMA * self.get_max_Q_value(new_state))

            # update the state to be the new state
            state = new_state

    def initialize_Q(self):
        """Initialize the initial values for Q"""
        self.initial_state = self.create_state(self.init_locations, self.init_pellets)
        for action in ['L','D','R','U']:
            self.Q[(self.initial_state,action)] = 0

    def add_new_Q(self, state):
        for action in ['L','D','R','U']:
            self.Q[(state,action)] = 0
    
    def get_max_Q_value(self,state):
        """Get the max value of Q, in the current state"""
        action = 'L'
        if (state, action) not in self.Q:
            self.add_new_Q(state)
        value = self.Q[(state, 'L')]
        for a in ['R', 'U', 'D']:
            new_val = self.Q[(state,a)]
            if new_val > value:
                action = a
                value = new_val
        return value
    
    def get_max_Q_action(self, state):
        """Get the action that maximizes the value of Q, in the current state"""
        action = 'L'
        if (state, action) not in self.Q:
            self.add_new_Q(state)
        value = self.Q[(state, 'L')]
        for a in ['R', 'U', 'D']:
            new_val = self.Q[(state,a)]
            if new_val > value:
                action = a
                value = new_val
        return action
    

    def choose_next_move(self, locations, pellets):
        "Choose next action for Pacman given the current state of the board."
        state = self.create_state(locations, pellets)
        # if state in self.policy:
        return self.get_max_Q_action(state)
    
