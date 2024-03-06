import time
import random
import copy

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
        self.N = N
        self.M = M
        self.locations = copy.deepcopy(init_locations)
        self.init_locations = copy.deepcopy(init_locations)
        self.pellets = init_pellets
        self.init_pellets = init_pellets
        self.policy = dict()
        self.initialize_Q()
        # run the Q_learning algorithm
        self.Q_learning()
        # update the policy
        self.update_policy()



    def create_state(self, locations: dict, pellets: set) -> tuple:
        """Create state tuple based on the locations and the pellets"""
        N = self.N
        M = self.M
        # create the list that will represent the state that locations represents
        state = [0] * (N * M)
        # update the pacman location in the states
        for key, value in locations.items():
            if key == 70:
                state[value[0]*N + value[1]] = key
        # update the locations of the pellets
        for i, j in pellets:
            curr = state[i*N + j]
            if curr == 0:
                state[i*N + j] = 11
            elif 20 <= curr <= 50:
                state[i*N + j] += 1
        return tuple(state)


    def Q_learning(self):
        """Run the whole Q_Learning algorithm to learn the best policy"""
        epsilon = 1



    def initialize_Q(self):
        """Initialize the initial values for Q"""
        self.Q = dict()
        for action in ['L','D','R','U']:
            self.Q[(self.create_state(self.init_locations, self.init_pellets),action)] = 0
    


    def get_max_Q_action(self, state):
        """Get the action that maximizes the value of Q, in the current state"""
        action : 'L'
        value = self.Q[(state, 'L')]
        for a in ['R', 'U', 'D']:
            new_val = self.Q[(state,a)]
            if new_val > value:
                action = a
                value = new_val
        return action
    
    def update_policy(self):
        for state in self.Q.keys():
            self.policy[state] = self.get_max_Q_action(state)

        


    def choose_next_move(self, locations, pellets):
        "Choose next action for Pacman given the current state of the board."
        state = self.create_state(locations, pellets)
        # if state in self.policy:
        return self.policy[state]
        # return random.choice('L','D','R','U')
    
