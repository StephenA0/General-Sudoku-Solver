import time
import math

#Creation Methods ----------------------------------------------------------------------------------
def make_board(lines):
    board = []
    for line in lines:
        line = line[:-1] #Removes "\n" at end
        board.append(line.split(" "))
        for i in range(len(board[0])):
            board[-1][i] = int(board[-1][i])
    
    n = int(math.sqrt(len(board)))
    return (n, board)

def make_sets(n):
    rows = []
    cols = []
    squares = []
    for _ in range(n):
        squares.append([])
    for i in range(n**2):
        rows.append(set(range(1, n**2 + 1)))
        cols.append(set(range(1, n**2 + 1)))
        squares[i//n].append(set(range(1, n**2 + 1)))
    
    sets = {}
    for i in range(n**2):
        for j in range(n**2):
            sets[(i, j)] = [rows[i], cols[j], squares[i//n][j//n]]
    
    return ((rows, cols, squares), sets)

def input_board(n, board, all_sets):
    rows, cols, squares = all_sets
    for i in range(n**2):
        for j in range(n**2):
            if board[i][j] != 0:
                try:
                    rows[i].remove(board[i][j])
                    cols[j].remove(board[i][j])
                    squares[i//n][j//n].remove(board[i][j])
                except:
                    raise Exception("Invalid input board.")

#Heap Methods --------------------------------------------------------------------------------------

#heap_val: value used for comparison in heap.
#Smaller values indicate lower set lengths and thus less casework to perform.
def heap_val(n, cell, sets):
    lens = []
    lens.append(len(sets[cell][0]))
    lens.append(len(sets[cell][1]))
    lens.append(len(sets[cell][2]))
    lens.sort()
    base = n**2 + 1
    return (base**2) * lens[0] + base * lens[1] + lens[2]

def get_heap_vals(n, sets):
    heap_vals = {}
    for i in range(n**2):
        for j in range(n**2):
            if board[i][j] == 0:
                heap_vals[(i, j)] = heap_val(n, (i, j), sets)

    return heap_vals

def build_heap(array, root_num, heap_vals, heap_inds = {}):
    if root_num >= len(array) // 2: #index of first leaf
        return
    build_heap(array, 2*root_num + 1, heap_vals, heap_inds)
    build_heap(array, 2*root_num + 2, heap_vals, heap_inds)
            
    sift_down(array, root_num, heap_vals, heap_inds)

def sift_down(heap, index, heap_vals, heap_inds):
    if index >= len(heap) // 2: #leaf, no children
        return
    
    if 2*index + 1 == len(heap) - 1: #one left child
        if heap_vals[heap[2*index + 1]] < heap_vals[heap[index]]:
            heap[index], heap[2*index + 1] = heap[2*index + 1], heap[index] #swap
            heap_inds[heap[index]] = index
            heap_inds[heap[2*index + 1]] = 2*index + 1
        return
                
    if heap_vals[heap[2*index + 1]] <= heap_vals[heap[2*index + 2]]: #two children
        smaller_child_index = 2*index + 1
    else:
        smaller_child_index = 2*index + 2
                
    if heap_vals[heap[index]] <= heap_vals[heap[smaller_child_index]]:
        return
    
    heap[index], heap[smaller_child_index] = heap[smaller_child_index], heap[index] #swap
    heap_inds[heap[index]] = index
    heap_inds[heap[smaller_child_index]] = smaller_child_index
    sift_down(heap, smaller_child_index, heap_vals, heap_inds) #sift_down on child

def sift_up(heap, index, heap_vals, heap_inds):
    if index == 0: #root reached
        return
    
    parent = (index - 1) // 2
    if heap_vals[heap[parent]] > heap_vals[heap[index]]:
        heap[index], heap[parent] = heap[parent], heap[index] #swap
        heap_inds[heap[index]] = index
        heap_inds[heap[parent]] = parent
        sift_up(heap, parent, heap_vals, heap_inds) #sift_up on parent

def get_heap_indices(heap):
    heap_inds = {}
    for i in range(len(heap)):
        heap_inds[heap[i]] = i
    
    return heap_inds

#Precondition: Sets has already been updated, but
#heap_vals and the heap itself have not.
def update_heap(n, board, cell, sets, heap, heap_vals, heap_inds):
    i, j = cell

    #Row Update
    for k in range(n**2):
        if board[i][k] == 0:
            heap_vals[(i, k)] = heap_val(n, (i, k), sets)
            sift_up(heap, heap_inds[(i, k)], heap_vals, heap_inds)
            sift_down(heap, heap_inds[(i, k)], heap_vals, heap_inds)
    
    #Col Update
    for k in range(n**2):
        if board[k][j] == 0:
            heap_vals[(k, j)] = heap_val(n, (k, j), sets)
            sift_up(heap, heap_inds[(k, j)], heap_vals, heap_inds)
            sift_down(heap, heap_inds[(k, j)], heap_vals, heap_inds)

    #Square Update
    for k in range(n*(i//n), n*(i//n) + n):
        for l in range(n*(j//n), n*(j//n) + n):
            if board[k][l] == 0:
                heap_vals[(k, l)] = heap_val(n, (k, l), sets)
                sift_up(heap, heap_inds[(k, l)], heap_vals, heap_inds)
                sift_down(heap, heap_inds[(k, l)], heap_vals, heap_inds)

#Used in testing to verify the heap property is always maintained.
def is_heap(heap, index, heap_vals):
    if index >= len(heap) // 2: #leaf, no children
        return True
    if 2*index + 2 < len(heap): #two children
        return heap_vals[heap[index]] <= min(heap_vals[heap[2*index + 1]], heap_vals[heap[2*index + 2]]) and is_heap(heap, 2*index + 1, heap_vals) and is_heap(heap, 2*index + 2, heap_vals)
    if 2*index + 1 < len(heap): #one left child
        return heap_vals[heap[index]] <= heap_vals[heap[2*index + 1]]

#Solve Methods ------------------------------------------------------------------------------------

#Dictionaries for a given cell:
        #sets -- row, col, and square associated with cell
        #heap_vals -- value for cell used in heap comparisons
        #heap_inds -- location of cell in heap
    #Other data structures:
        #all_sets -- the tuple (rows, cols, squares) of all rows, cols, and squares
        #board -- the game board
        #heap -- the min-heap of currently blank cells organized by heap_val

def initialize_data(n, board):
    all_sets, sets = make_sets(n)
    input_board(n, board, all_sets)

    heap_vals = get_heap_vals(n, sets)
    heap = list(heap_vals.keys())
    build_heap(heap, 0, heap_vals)
    heap_inds = get_heap_indices(heap)

    return (sets, heap, heap_vals, heap_inds)

def solve(board, data):
    sets, heap, heap_vals, heap_inds = data
    if not heap:
        return True
    i, j = heap[0]
    row, col, square = sets[(i, j)]
    cases = row & col & square
    if not cases:
        return False

    heap[0] = heap[-1]
    heap.pop()
    if heap:
        heap_inds[heap[0]] = 0
        sift_down(heap, 0, heap_vals, heap_inds)

    first_case = True
    for case in cases:
        board[i][j] = case
        row.remove(case)
        col.remove(case)
        square.remove(case)

        if first_case:
            #heap_vals are only dependent upon set length, so the heap stays the same when switching cases
            update_heap(n, board, (i, j), sets, heap, heap_vals, heap_inds)
            first_case = False

        if solve(board, data):
            return True

        row.add(case)
        col.add(case)
        square.add(case)
    
    board[i][j] = 0
    heap.append((i, j))
    heap_inds[(i, j)] = len(heap) - 1
    sift_up(heap, len(heap) - 1, heap_vals, heap_inds)
    update_heap(n, board, (i, j), sets, heap, heap_vals, heap_inds)
    return False

#Verification Methods -----------------------------------------------------------------------------
def verify_valid(n, board):
    curr_set = set()
    range_set = set()
    for i in range(1, n**2 + 1):
        range_set.add(str(i))

    for i in range(n**2):
        for j in range(n**2):
            curr_set.add(board[i][j])
        if curr_set != range_set:
            return False
        curr_set = set()

    for j in range(n**2):
        for i in range(n**2):
            curr_set.add(board[i][j])
        if curr_set != range_set:
            return False
        curr_set = set()
    
    for i in range(n):
        for j in range(n):
            for k in range(n):
                for l in range(n):
                    curr_set.add(board[n*i + k][n*j + l])
            if curr_set != range_set:
                return False
            curr_set = set()
    
    return True

#Display Methods ---------------------------------------------------------------------------------
def stringify(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            board[i][j] = str(board[i][j])

def print_sol(n, board, f):
    line_len = len(" ".join(board[0])) + 2*n + 1
    num_dashes = line_len - 1
    dash_line = num_dashes * ["-"]
    dash_line = "".join(dash_line)
    dash_border = "x" + dash_line + "x\n"
    dash_line = "|" + dash_line + "|\n"

    f.write(dash_border)
    for i in range(len(board)):
        if i % n == 0 and i != 0:
            f.write(dash_line)
        row = board[i]
        for j in range(n+1):
            row.insert((n+1)*j, "|")
        line = " ".join(row)
        f.write(line + "\n")
    f.write(dash_border)

#MAIN --------------------------------------------------------------------------------------------
with open("board.txt") as f:
    lines = f.readlines()

start = time.time()
n, board = make_board(lines)
data = initialize_data(n, board)
solve(board, data)
end = time.time()

stringify(board)
with open("solution.txt", "w") as f:
    if verify_valid(n, board):
        f.write("Solution is valid!\n\n")
        print_sol(n, board, f)
    else:
        f.write("No solution found.")

    f.write("\nRun-Time: " + str(end - start) + " s")