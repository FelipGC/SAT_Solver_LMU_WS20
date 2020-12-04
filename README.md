# LMU SAT-Solving WS2020/21

## Assignment 1: 
##### Goal:
Building a solver for the puzzle **_Tents_** by encoding it as a SAT problem.

##### Instructions:
File "game.py" contains methods to read and solve game-fields.

##### `Reading in the game-field:`
 ```python
from Assignment_one.game import GameEncoderBinomial
# To read a game-field via a .txt file:
path = "...\\...\\..."
game_from_text = GameEncoderBinomial.from_text_file(path)

#To read a game-field directly via a game-id:
game_id = "...x..:....,...,...,.."
game_from_id = GameEncoderBinomial.from_game_id(game_id)

# To generate a random game-field:
game_random = GameEncoderBinomial.from_randomness(size=(8,8), tree_density=0.5).
```
##### `Solving the game-field:`

 ```python
from Assignment_one.game import GameEncoderBinomial
# Create a game-field:
game = GameEncoderBinomial.from_...
# Print the unsolved game-field:
print(game.output_field())
# Solve the game-field:
game.solve_sat_problem()
# Print the solved game-field:
print(game.output_field())
```

##### `Analysing the game-encoding:`

 ```python
from Assignment_one.performance import print_encoding_details, get_encoding_details
# Create a game-field:
game = GameEncoderBinomial.from_...
# Print the number of variables, clauses and literals:
print_encoding_details(game)
# Get individual values
variables_n, literals_n, clauses_n = get_encoding_details(game)
```
##### `Printing the CNF as DIMACS_CNF:`

 ```python
from Assignment_one.game import GameEncoderBinomial, as_DIMACS_CNF
# Create a game-field:
game = GameEncoderBinomial.from_...
# Get the CNF game encoding
cnf = game.get_cnf_solution()
# Transform and print it in DIMACS format:
print(as_DIMACS_CNF(cnf))
```
##### `Comparing algorithms [sat-solvers]:`

 ```python
from Assignment_one.performance import analyse_sat_solvers

    g1 = GameEncoderBinomial.from_text_file("tent-inputs\\tents-10x10-t1.txt")
    g2 = GameEncoderSequential.from_text_file("tent-inputs\\tents-10x10-t1.txt")
    g3 = GameEncoderBinary.from_text_file("tent-inputs\\tents-10x10-t1.txt")
    # Compare different SAT sovlers and store the result as a png. file.
    analyse_sat_solvers([g1, g2, g3], show_png=True)
```

##### `Comparing algorithms [encodings]:`

 ```python
from Assignment_one.performance import EncodingPerformanceAnalysis, combine_analysis_reports

# Analyse the efficient algorithm.
p = EncodingPerformanceAnalysis(efficient=True)
# Store as csv. file.
p.store_metrics()
# Analyse the inefficient algorithm.
p2 = EncodingPerformanceAnalysis(efficient=False)
# Store as csv. file.
p2.store_metrics()
# Load the files and plot their differences.
combine_analysis_reports()
```