from collections import deque
import time
import sys
import argparse
import random
import copy
import math

intchar = [i for i in '123456789ABCEDFG']
N = 0
subblock_height = 0
subblock_width = 0
symbol_set = list()

csp_count = 0

drow = {}
dcol = {}
dblock = {}

ddrow = {}
ddcol = {}
ddblock = {}

pos_list = {}

prestored_neighbors = {}

# pretty prints the puzzle
# n: board string
def display_puzzle(n):
    puzzle = ''
    for x in range(N):
        for y in range(N):
            if y % subblock_width == 0 and not y == 0:
                puzzle += '| '
            puzzle += n[x * N + y] + ' '
        puzzle += '\n'
        if (x + 1) % subblock_height == 0 and not (x + 1) == N:
            puzzle += '-' * (subblock_width * 2) + '+'
            for t in range(subblock_height - 2):
                puzzle += '-' * (subblock_width * 2 + 1) + '+'
            puzzle += '-' * (subblock_width * 2) + '\n'
    print(puzzle)

# checks board is filled properly
def gut_check(n):
    for x in symbol_set:
        aa = n.count(x)
        if not aa == N:
            return False
    return True

# checks if puzzle is valid
def puzzle_check(n):
    leng = math.sqrt(len(n))
    if leng - math.floor(leng) != 0:
        print('Please input a valid puzzle')
        sys.exit(1)
    for i in n:
        valid_chars = set(symbol_set.copy())
        valid_chars.add('.')
        if i not in valid_chars:
            print('Please input a valid puzzle')
            sys.exit(1)


#csp backtracking
def sudoku_back_with_forward(n, p):
    if gut_check(n):
        return n
    # finds empty spaces, returns most constrained
    var = get_next_unassigned_var(n, p)
    for k in get_sorted_values(var, p):
        cn = n[:var] + k + n[var + 1:]
        new_state = p.copy()
        new_state[var] = k
        # forward looking
        result = forward_looking(new_state, cn, {var})
        if result is not None:
            # constraint propagation
            result = constraint_prop(new_state, result)
            if result is not None:
                aa = new_state.copy()
                # if passes all checks, recurse
                f_result = sudoku_back_with_forward(result, aa)
                if f_result is not None:
                    return f_result
    return None

# forward looking method, fills in trivial values
def forward_looking(new_state, puz, changed):
    if puz == None:
        return None
    puz = list(puz)
    while len(changed) > 0:
        x = changed.pop()
        for y in prestored_neighbors[x]:
            if not y == x:
                if new_state[x] in new_state[y]:
                    ab = new_state[y].index(new_state[x])
                    new_state[y] = new_state[y][:ab] + new_state[y][ab + 1:]
                    if len(new_state[y]) == 0:
                        return None
                    if len(new_state[y]) == 1 and puz[y] == '.':
                        puz[y] = new_state[y]
                        changed.add(y)
    puz = ''.join(puz)
    return puz

# finds cells connected to index x
def findNeighbors(x):
    a = (x % N) // subblock_width
    b = x // (subblock_height * N)
    return ddrow[x // N] | ddcol[x % N] | ddblock[a + b * (N // subblock_width)]

# eliminates possible value from neighboring cells
# updates board if only 1 value left
# calls forward looking if changes detected
def constraint_prop(new_state, puz):
    changes = set()
    if gut_check(puz):
        return puz
    puz = list(puz)
    for x in range(N):
        for pos_num in symbol_set:
            for cons in [ddrow, ddcol, ddblock]:
                con_count = 0
                con_index = -1
                for constraint_pos in cons[x]:
                    constraint_pos = int(constraint_pos)
                    if pos_num in new_state[constraint_pos]:
                        con_count += 1
                        con_index = constraint_pos
                    if con_count > 1:
                        break
                if con_count == 1:
                    new_state[con_index] = str(pos_num)
                    puz[con_index] = str(pos_num)
                    changes.add(con_index)
                elif con_count == 0:
                    return None

    puz = ''.join(puz)
    if len(changes) > 0:
        return forward_looking(new_state, puz, changes)
    else:
        return puz

# broken method
def find_pairs(new_state, puz):
    changed = set()
    puz = list(puz)
    for x in range(N):
        for cons in [ddrow, ddcol, ddblock]:
            dupes = {}
            for con_set in cons[x]:
                if not new_state[con_set] in dupes:
                    dupes[new_state[con_set]] = 1
                else:
                    dupes[new_state[con_set]] = dupes[new_state[con_set]] + 1
                    if len(new_state[con_set]) == dupes[new_state[con_set]]:
                        for rep in cons[x]:
                            if not new_state[rep] == new_state[con_set]:
                                for v in new_state[rep]:
                                    ind = new_state[rep].find(v)
                                    if ind > -1:
                                        new_state[rep] = new_state[rep][:ind] + new_state[rep][ind + 1:]
                                if len(new_state[rep]) == 1:
                                    puz[rep] = new_state[rep]
                                    changed.add(rep)
    puz = ''.join(puz)
    return forward_looking(new_state, puz, changed)


# finds most constrained index, if tied, randomly picks
def get_next_unassigned_var(n, p):
    min = 9
    minpos = [0]
    for x in range(N * N):
        bobb = len(p[x])
        if bobb > 1 and bobb < min:
            min = bobb
            minpos = [x]
        if bobb == min:
            minpos.append(x)
    return random.choice(minpos)


# returns values 
def get_sorted_values(x, p):
    return p[x]


# initializes static values
def initialize_values(line, NN):
    global N, ddrow, ddcol, ddblock, subblock_width, subblock_height, symbol_set
    N = NN
    ddrow = {}
    ddcol = {}
    ddblock = {}
    symbol_set = intchar[0:N]
    propose = int(N ** 0.5)
    for x in range(propose, 0, -1):
        if N % x == 0:
            subblock_height = x
            subblock_width = N // x
            break
    # Load in row, col, block groups
    for x in range(0, N):
        ddrow[x] = set()
        ddcol[x] = set()
        ddblock[x] = set()
    for x in range(N * N):
        ddrow[x // N].add(x)
        ddcol[x % N].add(x)
        a = int((x % N) // subblock_width)
        b = x // (subblock_height * N)
        ddblock[int(a + b * (N // subblock_width))].add(x)
    for x in range(N * N):
        prestored_neighbors[x] = findNeighbors(x)

# creates the constraint set
def create_constraint(line):
    global pos_list, drow, dcol, dblock
    pos_list = {}
    for x in range(0, N):
        drow[x] = set()
        dcol[x] = set()
        dblock[x] = set()
    for x in range(N * N):
        a = int((x % N) // subblock_width)
        b = x // (subblock_height * N)
        if not line[x] == '.':
            drow[x // N].add(line[x])
            dcol[x % N].add(line[x])
            dblock[int(a + b * (N // subblock_width))].add(line[x])

    # configure constraint set
    for x in range(N * N):
        if not line[x] == '.':
            pos_list[x] = line[x]
        else:
            ret = ''
            a = (x % N) // subblock_width
            b = x // (subblock_height * N)
            dtot = drow[x // N] | dcol[x % N] | dblock[a + b * (N // subblock_width)]
            for k in symbol_set:
                if k not in dtot:
                    ret += k
            pos_list[x] = ret


def algo(line):
    newb = set()
    for x in range(N * N):
        if len(pos_list[x]) == 1 and line[x] == '.':
            newb.add(x)
    new_state = pos_list.copy()
    bob = forward_looking(new_state, line, newb)
    bob = constraint_prop(new_state, bob)
    bob = sudoku_back_with_forward(bob, new_state)
    return bob


def solve(line):
    NN = int(len(line) ** 0.5)
    if not N == NN:
        initialize_values(line, NN)
    puzzle_check(line)
    if args.verbose:
        print('Inputted Puzzle:')
        display_puzzle(line)

    create_constraint(line)

    # start solving!
    ans = algo(line)
    if ans is not None:
        if args.verbose:
            print('Solved Puzzle:')
            display_puzzle(ans)
        else:
            print(ans)
    else:
        print('Sorry, we were unable to solve this puzzle.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Sudoku Solver')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-p', metavar='PUZZLE', help="puzzle string. Fill empty slots with '.'")
    group.add_argument('-f', '--file', help="puzzle filename. Separate puzzles with a new line")
    parser.add_argument("-v", "--verbose", action="store_true", help="pretty-prints puzzles for files", default=False)
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    start = time.perf_counter()

    if args.p is not None:
        puzzle = args.p
        args.verbose = True
        solve(puzzle)
        end = time.perf_counter()

    elif args.file is not None:
        puzzles = []
        try:
            with open(args.file, "rb") as fil:
                for line in fil:
                    puzzles.append(line.strip().decode('utf-8'))   
        except OSError as e:
            print("File not found or not readable.")
            exit(1)

        for pp in puzzles:
            solve(pp)
        end = time.perf_counter()
    else:
        print('Please input a puzzle or filename')
        sys.exit(1)
    print(f'Solve Time: {(end - start)}s')    
