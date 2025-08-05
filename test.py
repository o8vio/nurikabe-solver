from auxfunctions import *
from nurikabe import Grid

path_to_puzzle = './puzzles/puzzle5_5x5.txt'
path_to_solved = path_to_puzzle.replace('./puzzles', './solved')

nuri = Grid(path_to_puzzle)
nuri.solve_nurikabe(path_to_solved)