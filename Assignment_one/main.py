from Assignment_one.game import TentGameEncoding

# t = TentGameEncoding.from_text("tent-inputs\\tents-8x8-e1.txt")
# t.solve_sat_problem()
t = TentGameEncoding.from_randomness()
t.reduce_to_possible_solution()
# print("SOLUTION:")
print(t.output_field())
