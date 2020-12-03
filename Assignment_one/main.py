from Assignment_one.game import GameEncoderBinomial, GameEncoderSequential, write_to_text_file, random_field
from Assignment_one.performance import print_encoding_details, combine_analysis_reports, analyse_sat_solvers
from Assignment_one.parse_gameid import parse_id

write_to_text_file((random_field((8,8),0.5)),"tent-inputs\\gamefield.txt")
