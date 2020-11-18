import glob
from itertools import chain

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import datetime

from Assignment_one import game
from Assignment_one.game import TentGameEncoding


def combine_analysis_reports():
    paths = glob.glob("data\\*.csv")
    df = pd.concat([pd.read_csv(path) for path in paths], ignore_index=True)
    sns.lineplot(data=df, x="Capacity", y="Variables", hue="Algorithm")
    plt.show()
    ax = sns.lineplot(data=df, x="Capacity", y="Literals", hue="Algorithm")
    ax.set(yscale="log")
    plt.show()


def print_encoding_details(g: TentGameEncoding):
    print("\n" + "-" * 30)
    print("Game size:", g.size)
    cnf = g.get_cnf_solution()
    literals = list(chain(*cnf))
    print("Nr. of \tvariables:\t", len(set(abs(x) for x in literals)))
    print("Nr. of \tclauses:\t", len(cnf))
    print("Nr. of \tliterals:\t", len(literals))
    print("-" * 30)


class PerformanceAnalysis:
    def __init__(self, efficient=True):
        print("Creating and solving multiple games, this might take a while...")
        paths = glob.glob("tent-inputs\\*.txt")
        self.efficient = efficient
        self.games = [game.TentGameEncoding.from_text_file(path, efficient=self.efficient, verbose=False) for path in
                      paths]
        self.games_cnf = [g.get_cnf_solution() for g in self.games]

    def plot_metrics(self):
        df = pd.DataFrame(columns=["Capacity", "Literals", "Variables", "Clauses", "Algorithm"])
        for index, cnf in enumerate(self.games_cnf):
            game_size = self.games[index].capacity
            clauses_n = len(cnf)
            literals = list(chain(*cnf))
            variables = set(abs(x) for x in literals)
            df = df.append({"Algorithm": "Efficient" if self.efficient else "Simple",
                            "Clauses": clauses_n, "Capacity": game_size, "Literals": len(literals),
                            "Variables": len(variables)}, ignore_index=True)
        df.Capacity = df.Capacity.astype(int)
        df.Literals = df.Literals.astype(int)
        df.Variables = df.Variables.astype(int)
        time_id = datetime.datetime.now().strftime('%m-%d_%H-%M-%S')
        df.to_csv(f"data\\performance_analysis_{time_id}.csv", index=False)
        print("Saved data-frame as csv.")
