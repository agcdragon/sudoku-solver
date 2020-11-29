# sudoku-solver

This Sudoku solver is based off of a TJ Artificial Intelligence course project. It employs CSP backtracking, forward looking, and constraint propagation to solve Sudoku puzzles.
It currently has support for 2x2, 2x3, 2x4, 3x3, 2x5, 3x4, and 4x4 Sudoku subgrids. 

## Installation

Clone the repository: `git clone https://github.com/agcdragon/sudoku-solver.git`

## Usage

The solver takes in two types of command line input: a file with Sudoku puzzles separated by new lines or a single Sudoku puzzle string. Puzzles are translated into a string where you read the puzzle left to right, top to bottom. Empty slots are represented with a period and numbers greater than 9 are represented by A, B, C, etc. 

Note: The verbose setting (pretty-printing) is enabled for string input, but is not for file input. 

```
usage: sudoku_solver.py [-h] [-p PUZZLE | -f FILE] [-v] 

arguments:
  -h, --help            show this help message and exit
  -p PUZZLE             puzzle string, fill empty slots with '.'
  -f FILE, --file FILE  puzzle filename, separate puzzles with a new line
  -v, --verbose         pretty-prints puzzles for files
```
#### Example Puzzle Representation
##### Sudoku String Representation
`1..92....524.1...........7..5...81.2.........4.27...9..6...........3.945....71..6`

##### Pretty-Printed:
```
1 . . | 9 2 . | . . .
5 2 4 | . 1 . | . . .
. . . | . . . | . 7 .
------+-------+------
. 5 . | . . 8 | 1 . 2
. . . | . . . | . . .
4 . 2 | 7 . . | . 9 .
------+-------+------
. 6 . | . . . | . . .
. . . | . 3 . | 9 4 5
. . . | . 7 1 | . . 6
```
## Todo

* Create an interactive website for easier Sudoku input
* Develop a computer vision mobile app to scan Sudoku boards and solve automatically
