from Assignment_one.game import GameEncoderBinomial, GameEncoderSequential
from Assignment_one.performance import print_encoding_details, combine_analysis_reports, analyse_sat_solvers

g1 = GameEncoderSequential.from_text_file("tent-inputs\\tents-10x10-t1.txt")
g1.solve_sat_problem()
print(g1.output_field())
print_encoding_details(g1)
