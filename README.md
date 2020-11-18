# LMU SAT-Solving WS2020/21

## Assignment 1: 
##### Goal:
Building a solver for the puzzle **_Tents_** by encoding it as a SAT problem.
##### Instructions:
File "game.py" contains methods to read and solve game-fields.

##### `Reading in the game-field:`
 ```python
from Assignment_one.game import TentGameEncoding
# To read a game-field via a .txt file:
path = "...\\...\\..."
game_from_text = TentGameEncoding.from_text_file(path)

#To read a game-field directly via a game-id:
game_id = "...x..:....,...,...,.."
game_from_id = TentGameEncoding.from_game_id(game_id)

# To generate a random game-field:
game_random = TentGameEncoding.from_randomness(size=(8,8), tree_density=0.5).
```
##### `Solving the game-field:`

 ```python
from Assignment_one.game import TentGameEncoding
# Create a game-field:
game = TentGameEncoding.from_...
# Print the unsolved game-field:
print(game.output_field())
# Solve the game-field:
game.solve_sat_problem()
# Print the solved game-field:
print(game.output_field())
```

##### `Analysing the game-encoding:`

 ```python
from Assignment_one.performance import print_encoding_details
# Create a game-field:
game = TentGameEncoding.from_...
# Print the number of variables, clauses and literals:
print_encoding_details(game)
```
##### `Printing the CNF as DIMACS_CNF:`

 ```python
from Assignment_one.game import TentGameEncoding, as_DIMACS_CNF
# Create a game-field:
game = TentGameEncoding.from_...
# Get the CNF game encoding
cnf = game.get_cnf_solution()
# Transform and print it in DIMACS format:
print(as_DIMACS_CNF(cnf))
```