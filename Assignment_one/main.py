from Assignment_one.game import TentGameEncoding
from Assignment_one.performance import print_encoding_details

t = TentGameEncoding.from_text_file("tent-inputs\\tents-8x8-e1.txt")
t.solve_sat_problem()
print(t.output_field())
print_encoding_details(t)