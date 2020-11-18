import glob
from itertools import chain

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import datetime

from Assignment_one import game


def combine_analysis_reports():
    paths = glob.glob("data\\*.csv")
    df = pd.concat([pd.read_csv(path) for path in paths], ignore_index=True)
    sns.lineplot(data=df, x="Capacity", y="Variables", hue="Algorithm")
    plt.show()
    ax = sns.lineplot(data=df, x="Capacity", y="Literals", hue="Algorithm")
    ax.set(yscale="log")
    plt.show()


class PerformanceAnalysis:
    def __init__(self):
        print("Creating and solving multiple games, this might take a while...")
        paths = glob.glob("tent-inputs\\*.txt")
        self.efficient = True
        self.games = [game.TentGameEncoding.from_text_file(path, efficient=self.efficient, verbose=False) for path in paths]
        self.games_cnf = [g.combine_conditions() for g in self.games]

    def plot_metrics(self):
        df = pd.DataFrame(columns=["Capacity", "Literals", "Variables", "Algorithm"])
        for index, cnf in enumerate(self.games_cnf):
            game_size = self.games[index].capacity
            literals = list(chain(*cnf))
            variables = set(abs(x) for x in literals)
            df = df.append({"Algorithm": "Efficient" if self.efficient else "Simple"
                               , "Capacity": game_size, "Literals": len(literals),
                            "Variables": len(variables)}, ignore_index=True)
        df.Capacity = df.Capacity.astype(int)
        df.Literals = df.Literals.astype(int)
        df.Variables = df.Variables.astype(int)
        time_id = datetime.datetime.now().strftime('%m-%d_%H-%M-%S')
        df.to_csv(f"data\\performance_analysis_{time_id}.csv", index=False)
        print("Saved data-frame as csv.")


pa = PerformanceAnalysis()
pa.plot_metrics()
combine_analysis_reports()
