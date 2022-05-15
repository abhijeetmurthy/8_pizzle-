from sys import maxsize
import time

# https://docs.python.org/3/library/copy.html#copy.deepcopy
# Used to perform copy while expanding children.
from copy import deepcopy
from tracemalloc import start 
#Performing deepcopy as below.
def deep_copy(state, children):
    child = deepcopy(state) #creates a child based on the last move
    child._depth += 1  #increment _depth cost by one for each move (here each edge just costs 1)
    children.append(child)


#def Global Variables
_queue = []
_expanded = 0  #pretty much a static
_goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]] #hold the goal/end state internally in the puzzle class



#def Class State: It is the state of the given state. It is represented by the 3x3 puzzle, G(n) of the solution and H(n) of the solution.
class State:
    def __init__(self, puzzle, depth, heuristic): 
        self.puzzle = puzzle
        self._depth = depth
        self._heuristic = heuristic

#def Class Puzzle: Defines the puzzle, the operators what can be performed and helper function to print the 3x3 puzzles.
class Puzzle:
    def __init__(self, game): 
        self.game = game
        self._y, self._x = self.find_0() #order here is y->x, or row->col

    # def left:move 0 left if possible and report false otherwise
    def left(self): 
        in_left_col = False 
        for x in range(3):
            if self.game[x][0] == 0: 
                in_left_col = True
                break

        if in_left_col == False:
            self.swap(self._y, self._x - 1)
            self._x = self._x - 1 
            return True

        else: 
            return False
    # def right:move 0 right if possible and report false otherwise
    def right(self): 
        in_right_col = False 
        for x in range(3):
            if self.game[x][2] == 0:
                in_right_col = True
                break

        if in_right_col == False:
            self.swap(self._y, self._x + 1)
            self._x = self._x + 1
            return True

        else: 
            return False

    # def up:move 0 up if possible and report false otherwise
    def up(self): 
        if 0 not in self.game[0]: 
            self.swap(self._y - 1, self._x)
            self._y = self._y - 1 
            return True

        else: 
            return False
    # def down:move 0 down if possible and report false otherwise
    def down(self):
        if 0 not in self.game[2]:
            self.swap(self._y + 1, self._x) 
            self._y = self._y + 1
            return True

        else: 
            return False

    # def helper: function to locate 0 in the puzzle.
    def find_0(self):
        for x in range(len(self.game)): 
            for y in range(len(self.game)):
                if self.game[x][y] == 0: 
                    return x, y 

    # def swap: simple swap function to replace any tile with the blank.
    def swap(self, y, x):
        temp_0 = self.game[self._y][self._x] 
        self.game[self._y][self._x] = self.game[y][x] 
        self.game[y][x] = temp_0
    
    # def _print: Print the state.
    def _print(self):
        strstr = []
        for x in range(len(self.game)):
            for y in range(len(self.game)): 
                strstr.append(self.game[x][y]) 
            print(strstr) 
            strstr = [] 

# def operate: Returns all possible children of the given puzzle.    
def operate(state):
    global _expanded 
    children = []
    # We use the operators defined above to create child states, which are added to the queue.
    if state.puzzle.right(): 
        _queue.append(state.puzzle.game) 
        deep_copy(state, children)
        state.puzzle.left()

    if state.puzzle.left():
        _queue.append(state.puzzle.game) 
        deep_copy(state, children)
        state.puzzle.right() 

    if state.puzzle.up(): 
        _queue.append(state.puzzle.game) 
        deep_copy(state, children) 
        state.puzzle.down() 

    if state.puzzle.down(): 
        _queue.append(state.puzzle.game) 
        deep_copy(state, children) 
        state.puzzle.up() 
        
    _expanded += len(children)
    return children

# def pop: works by returning the child with minimum cost given an list of nodes. Alternatively can use priority queue(heapq) in python.
def pop(queue):
    min_total_cost = maxsize
    positition = maxsize 
    
    for n in range(len(queue)):
        if queue[n]._depth + queue[n]._heuristic < min_total_cost:
            min_total_cost = queue[n]._depth + queue[n]._heuristic
            positition = n
    state = queue.pop(positition)
    return state
    
# def misplaced_tiles: measures the number of tiles out of position.
def misplaced_tiles(state):
    h = 0 
    for i in range(len(state.puzzle.game)):
        for j in range(len(state.puzzle.game)):
            if state.puzzle.game[i][j] != _goal_state[i][j]: 
                if state.puzzle.game[i][j] != 0: 
                    h += 1
    print("printing h:")
    return h

# def manhattan_distance: measures the number of tiles out of position.
def manhattan_distance(state):
    h = 0 
    def map(state, i, j):
        tile = state.puzzle.game[i][j] 
        find_tile={1:[0,0],2:[0,1],3:[0,2],4:[1,0],5:[1,1],6:[1,2],7:[2,0],8:[2,1]}
        return find_tile[tile][0],find_tile[tile][1]

    for i in range(len(state.puzzle.game)):
        for j in range(len(state.puzzle.game)):
            if state.puzzle.game[i][j] != _goal_state[i][j]: 
                if state.puzzle.game[i][j] != 0: 
                    row_diff, col_diff = map(state, i, j) 
                    temp_h = pow(pow((i - row_diff), 2) + pow(j - col_diff, 2), 0.5) #h formula
                    h += temp_h
    return h

def expand_blind(queue, state, children):     
    for child in children: 
        if child.puzzle.game not in _queue: 
            queue.append(child)
            _queue.append(child.puzzle.game)

def expand_misplaced(queue, state, children):
    for child in children: 
        child._heuristic = misplaced_tiles(child)
        if child.puzzle.game not in _queue: 
            queue.append(child)
            _queue.append(child.puzzle.game)
            
def expand_manhattan(queue, state, children):
    for child in children: 
        child._heuristic = manhattan_distance(child)
        if child.puzzle.game not in _queue: 
            queue.append(child)
            _queue.append(child.puzzle.game)

# def expand: calculate the h(n) value. 
def expand(queue, state, _algo):
    print("Expanding State [G(n) = " + str(state._depth) + " and H(n) = " + str(state._heuristic)+"]")
    state.puzzle._print()

    children = operate(state) 
    if _algo==1:
        expand_blind(queue, state, children)
            
    elif _algo==2:
        expand_misplaced(queue, state, children)

    elif _algo==3:
        expand_manhattan(queue, state, children)
    return queue



# def General_search: Puesdo code as per slides of Dr.Eamonn.
def General_search(puzzle, _algo):
    # if _algo==1:
    _depth = 0
    heuristic = 0
    #initialisation with 
    state = State(puzzle, _depth, heuristic)  
    #update heuristic for misplaced tiles h(n)
    if _algo == 2: 
        state._heuristic = misplaced_tiles(state)

    #update _heuristic for manhattan h(n)
    elif _algo == 3: 
        state._heuristic = manhattan_distance(state)

    #initialize with first state
    queue = [state] 
    max_queue_size = 0

    while True:
        max_queue_size = max(len(queue), max_queue_size) #max size seen so far is the max queue size ever seen

        if not queue: 
            print("Invalid Puzzle!")
            return

        (state) = pop(queue)

        if state.puzzle.game == _goal_state: 
            print("Goal State!\n")
            print("Number of nodes expanded: " + str(_expanded))
            print("Max queue size: " + str(max_queue_size))
            return

        queue = expand(queue, state, _algo)

# def main: driver code to retreive user inputs of the puzzle and the algorithm to be used. 
def main():
    
    _puzzle = []
    print("Use 0 for the blank and , for space.")
    for i in range(0,3):
        row=(input("Numbers in "+str(i)+" row.")).split(",")
        row=[int(_) for _ in row]
        _puzzle.append(row)

    puzzle = Puzzle(_puzzle)
    _algo = int(input("Choice of algorithms to use:\n"+ "1. Uniform Cost Search\n2. A* with Misplaced Tile Heuristic\n3: A* with manhattan  Distance Heuristic\n"))
    start = time.time()
    puzzle._print()
    General_search(puzzle,_algo)
    # General_search(puzzle,1)
    end = time.time()
    print(end-start)

main()