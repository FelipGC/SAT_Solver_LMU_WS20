from Assignment_one.game import TentGameEncoding

# t = TentGameEncoding.from_text("tent-inputs\\tents-8x8-e1.txt")
game_id = "8x8:cachdbidec_cg,1,3,0,3,0,2,2,1,2,1,2,1,3,1,2,0"
t = TentGameEncoding.from_game_id(game_id)
t.solve_sat_problem()
print(t.output_field())