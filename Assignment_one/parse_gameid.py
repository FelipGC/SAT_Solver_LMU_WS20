# python3 script to convert game-ids of empty(!) grids into text
# This script is based on the provided code for parsing game_ids, but slightly modified.
import sys


def parse_id(game_id):
    size, data = game_id.split(":")
    m, n = map(int, size.split("x"))
    grid, i = ['.'] * n * m, 0
    trees, *values = data.split(',')
    for c in trees:
        if 'a' <= c <= 'z':
            i += min(25, ord(c) - ord('a') + 1)
        if c != 'z' and i < n * m:
            grid[i] = 'T'
            i += 1

    game_txt = f"{n} {m}\n"
    for i in range(n):
        game_txt += "".join(grid[i * m + j] for j in range(m)) + " " + values[m + i] + "\n"
    game_txt += " ".join(values[:m])
    return game_txt


if __name__ == "__main__":
    if len(sys.argv) != 2:
        #print("usage %s gameid" % sys.argv[0])
        exit(1)
    #print(parse_game_id(sys.argv[1]))
