from Assignment_one.game import TentGameEncoding

t = TentGameEncoding.from_text("tent-inputs\\tents-8x8-e1.txt")
t.solve_sat_problem()
print("SOLUTION:")
print(t.output_field())