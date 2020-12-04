from Assignment_one.game import GameEncoderBinomial, GameEncoderSequential, GameEncoderBinary
from Assignment_one.performance import analyse_sat_solvers

if __name__ == "__main__":
    print("Launching tent-game encoder...")

    g1 = GameEncoderBinomial.from_text_file("tent-inputs\\tents-10x10-t1.txt")
    g2 = GameEncoderSequential.from_text_file("tent-inputs\\tents-10x10-t1.txt")
    g3 = GameEncoderBinary.from_text_file("tent-inputs\\tents-10x10-t1.txt")
    # Compare different SAT sovlers and store the result as a png. file.
    analyse_sat_solvers([g1, g2, g3], show_png=True)
