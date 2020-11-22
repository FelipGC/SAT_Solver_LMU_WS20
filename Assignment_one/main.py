from Assignment_one.game import TentGameEncoding
from Assignment_one.performance import print_encoding_details, combine_analysis_reports, analyse_sat_solvers

g1 = TentGameEncoding.from_text_file("tent-inputs\\tents-10x10-t1.txt", algo_name="Efficient")
g2 = TentGameEncoding.from_text_file("tent-inputs\\tents-10x10-t1.txt", efficient=False, algo_name="Inefficient")

# t.solve_sat_problem()
# print(t.output_field())
# print_encoding_details(t)

analyse_sat_solvers([g1, g2])
