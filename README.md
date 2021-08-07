This program is meant to efficiently solve Sudoku boards using backtracking and a min-heap. Brute-force backtracking approaches tend to be incredibly inefficient,
as an enormous amount of casework must be performed. This algorithm, however, uses a min-heap to minimize the amount of casework to be done, greatly improving its 
efficiency in the process. The program works on general n^2 x n^2 Sudoku boards, not just the standard 9 x 9.

To run the program, simply input a board into board.txt and run sudoku.py. A solution file solution.txt will be produced which displays the solution (if one exists)
and the run-time of the solving algorithm. Example boards exist in example_boards.txt, but you may input an arbitrary one and the program will always find a solution
(given one exists).

The casework is optimized in the following way: the "sets" dictionary maps each blank cell to three sets: the cell's row, column, and square. These three sets each
contain the values which remain to be filled into the board in that given row, column, or square. For example, if row 4 already has 3, 4, 6, and 8 written into it,
then rows[4] = {1, 2, 5, 7, 9} for a 9 x 9 board. The smaller the set, the more constrained the casework on a cell. Thus, we aim to casework on the cell with the
minimum row, col, and square set size, and we use the min-heap to repeatedly find that cell. The min-heap is then repeatedly updated (because the values change as
more cells are filled in) until it is empty, at which point all cells have been properly filled in.
