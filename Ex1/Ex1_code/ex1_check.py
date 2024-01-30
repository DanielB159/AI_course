import ex1
import search


def run_problem(func, targs=(), kwargs={}):
    result = (-3, "default")
    try:
        result = func(*targs, **kwargs)

    except Exception as e:
        result = (-3, e)
    return result

# check_problem: problem, search_method, timeout
# timeout_exec: search_method, targs=[problem], timeout_duration=timeout
def solve_problems(problem, algorithm):

    for row in problem:
        print(row),
    print

    try:
        p = ex1.create_pacman_problem(problem)
    except Exception as e:
        print("Error creating problem: ", e)
        return None

    if algorithm == "gbfs":
        result = run_problem((lambda p: search.breadth_first_graph_search(p)),targs=[p])
    else:
        result = run_problem((lambda p: search.astar_search(p, p.h)), targs=[p])

    if result and isinstance(result[0], search.Node):
        solve = result[0].path()[::-1]
        solution = [pi.action for pi in solve][1:]
        print(len(solution), solution)
    else:
        print("no solution")

problem1 = ((20,10,10,10,10),
         (10,10,10,10,10),
         (10,11,10,10,10),
         (10,11,10,10,10),
         (77,11,10,10,10))
#solution1: len(solution) = 7
problem2 = ((21,31,41,11,11,11,11,11,11,11,11,11),
(11,99,99,99,99,11,99,99,99,99,99,11),
(11,99,99,99,99,11,99,99,99,99,99,11),
(11,11,11,99,99,11,11,11,11,11,11,11),
(99,99,11,99,99,11,99,99,11,99,99,99),
(99,99,11,99,99,11,99,99,11,99,99,99),
(11,11,11,11,11,11,99,99,11,11,11,11),
(11,99,99,99,99,99,99,99,99,99,99,11),
(11,99,99,99,99,99,99,99,99,99,99,11),
(11,11,11,11,11,11,11,11,11,11,11,77))
#solution2: len(solution) = 98

problem3 = (
            (10, 10, 10, 11),
            (10, 99, 10, 50),
            (10, 10, 10, 10),
            (77, 10, 10, 10),
        )

problem4 = (
            (11, 10, 50, 10),
            (10, 99, 99, 11),
            (20, 10, 10, 10),
            (77, 10, 10, 10),
        )

problem5 = (
            (11, 10, 10, 21),
            (10, 10, 40, 10),
            (10, 50, 77, 10),
            (31, 10, 10, 11),
        )

problem6 = ( ##################################################### PROBLEM
            (10, 10, 10, 30, 99, 10),
            (10, 11, 11, 10, 10, 10),
            (77, 10, 11, 10, 10, 10),
            (10, 10, 10, 99, 10, 10),
            (99, 10, 11, 10, 10, 10),
            (10, 10, 21, 10, 10, 10),
        )

problem7 = (
            (11, 10, 11, 99, 10, 99, 20, 99),
            (10, 99, 10, 77, 99, 99, 99, 99),
            (10, 99, 10, 10, 10, 99, 10, 10),
            (10, 10, 10, 10, 10, 99, 99, 10),
            (99, 30, 10, 99, 10, 10, 99, 11),
            (10, 10, 99, 99, 10, 99, 99, 10),
            (99, 10, 10, 99, 11, 10, 99, 10),
            (99, 10, 11, 99, 99, 10, 10, 10),
        )
problem8 = (
            (10, 21, 10, 11, 11, 10, 11, 99),
            (10, 99, 99, 10, 10, 99, 10, 10),
            (10, 99, 77, 10, 99, 99, 99, 99),
            (10, 10, 10, 10, 10, 10, 99, 99),
            (11, 10, 10, 99, 10, 10, 10, 99),
            (10, 99, 99, 10, 99, 99, 10, 99),
            (99, 30, 99, 10, 10, 10, 11, 99),
            (99, 10, 99, 10, 99, 10, 40, 99),
        )
def main():
    problem = problem2 #or problem2
    algorithm = "astar" #or "astar"

    solve_problems(problem, algorithm)

if __name__ == '__main__':
    main()