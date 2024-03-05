import pacman
import random
import ex2
import time

def evaluate(board, steps, p = 0.7):    
        """Run solver function on given problem and evaluate it's effectiveness."""
        run_pacman = pacman.Game(steps, board) 

        t1 = time.time()
        controller = ex2.Controller(len(board[0]), len(board), run_pacman.init_locations.copy(), 
                          run_pacman.init_pellets.copy(), steps)
        t2 = time.time()
        
        print("Controller initialization took: ", t2 - t1, " seconds.\n")
        
        t3 = time.time()
        print("The average score for the problem is:", 
            run_pacman.evaluate_policy(controller, p, 30, visualize=False))
        t4 = time.time()
        print("Controller evaluation took: ", t4 - t3, " seconds")

def main():
    """Print student id and run evaluation on a given game"""
    print("\n", ex2.id)
    
    game0 = ((20,10,10,99,10),
             (10,10,10,10,41),
             (10,11,10,99,11),
             (10,11,10,10,10),
             (70,10,10,99,11))
    
    evaluate(game0, 100, 0.7)    


if __name__ == '__main__':
    main()
    

