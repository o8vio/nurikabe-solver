# nurikabe-solver
Python script to solve the logic puzzle-game Nurikabe using backtracking.

**Usage**
Each text file in the 'puzzles' directory represents a raw instance of the Nurikabe puzzle to be solved. 
The grid is represented as a matrix, meaning the text should contain m lines with n characters each. Each character can be:
'.' : a dot representing an empty cell in the grid,
'#' : a hashtag representing a cell with a wall,
'1', '2',.. '9' : an integer between 1 and 9 indicating the number of cells of its block.

To solve a puzzle, edit and run 'test.py' specifying the path to the puzzle instance and the desired output file name for the solution.
