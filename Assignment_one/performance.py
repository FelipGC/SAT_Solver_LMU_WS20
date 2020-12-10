import glob

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import datetime

from game import *


def combine_analysis_reports():
    paths = glob.glob("data\\*.csv")
    df = pd.concat([pd.read_csv(path) for path in paths], ignore_index=True)
    # sns.lineplot(data=df, x="Field-size", y="Variables", hue="Algorithm")
    plt.show()
    ax = sns.lineplot(data=df, x="Field-size", y="Literals", hue="Algorithm")
    ax.set(yscale="log")
    plt.show()


def get_encoding_details(g: GameEncoder):
    cnf = g.get_cnf_solution()
    a = list(chain(*cnf))
    clauses_n = len(cnf)
    variables_n = len(set(abs(x) for x in a))
    return variables_n, clauses_n


def print_encoding_details(g: GameEncoder):
    variables_n, clauses_n = get_encoding_details(g)
    print("\n" + "-" * 30)
    print("Game size:", g.size)
    print("Nr. of \tvariables:\t", variables_n)
    print("Nr. of \tclauses:\t", clauses_n)
    print("-" * 30)


def analyse_sat_solvers(games: [GameEncoder], show_png=False):
    from timeit import default_timer as timer
    from pysat.solvers import Cadical, Glucose4, Lingeling, Minisat22, Maplesat
    df = pd.DataFrame(columns=["Solver", "Execution time [sec]", "Algorithm"])
    for g in games:
        cnf_ = CNF(from_string=as_DIMACS_CNF(g.get_cnf_solution()))
        solvers = {"Cadical": Cadical(cnf_), "Glucose4": Glucose4(cnf_), "Lingeling": Lingeling(cnf_),
                   "Minisat22": Minisat22(cnf_), "Maplesat": Maplesat(cnf_)}
        for name, solver in solvers.items():
            start = timer()
            solved = solver.solve()
            end = timer()
            delta_t = end - start
            print(name, "\tSolved:", solved, "\tTime:", delta_t)
            df = df.append({"Solver": name, "Execution time [sec]": delta_t, "Algorithm": g.algo_name},
                           ignore_index=True)
    df.to_csv("data\\solver_analysis.csv", index=False)
    print("Saved data-frame as csv.")
    plt.yscale('log')
    sns.barplot(x="Solver", y="Execution time [sec]", hue="Algorithm", data=df)
    plt.savefig("data\\solver_performance_analysis.png")
    if show_png:
        print("Plotting graph...")
        plt.show()

    class EncodingPerformanceAnalysis:
        def __init__(self, efficient=True):
            print(f"EFFICIENT={efficient}: Creating and solving multiple games, this might take a while...")
            paths = glob.glob("tent-inputs\\*.txt")
            self.efficient = efficient
            self.games = [GameEncoderBinomial.from_text_file(path, efficient=self.efficient, verbose=False) for
                          path
                          in
                          paths]
            self.games_cnf = [g.get_cnf_solution() for g in self.games]

        def store_metrics(self):
            df = pd.DataFrame(columns=["Field-size", "Literals", "Variables", "Clauses", "Algorithm"])
            for index, cnf in enumerate(self.games_cnf):
                game_size = self.games[index].capacity
                clauses_n = len(cnf)
                literals = list(chain(*cnf))
                variables = set(abs(x) for x in literals)
                df = df.append({"Algorithm": "Efficient" if self.efficient else "Simple",
                                "Clauses": clauses_n, "Field-size": game_size, "Literals": len(literals),
                                "Variables": len(variables)}, ignore_index=True)
            df.Capacity = df.Capacity.astype(int)
            df.Literals = df.Literals.astype(int)
            df.Variables = df.Variables.astype(int)
            time_id = datetime.datetime.now().strftime('%m-%d_%H-%M-%S')
            df.to_csv(f"data\\encoding_performance_analysis_{time_id}.csv", index=False)
            print("Saved data-frame as csv.")
