from Assignment_one.game import GameEncoderBinomial, GameEncoderSequential, write_to_text_file, remove_tents
from Assignment_one.performance import print_encoding_details, combine_analysis_reports, analyse_sat_solvers

size = (10, 10)
difficulty = 0.2

write_to_text_file(remove_tents(GameEncoderBinomial.from_randomness(size, difficulty).output_field()), "tent-inputs\\gamefield.txt")

