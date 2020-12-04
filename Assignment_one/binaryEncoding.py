import math, itertools


class BinaryAtMost_k_Of_n:
    # instances of this class construct a cnf asserting that exactly k of n vars are correct, and appropriately names them
    # the idea for the encoding  comes from the paper "SAT Encodings of the At-Most-k Constraint "by A. M. Frisch and P. A. Giannaros
    # found here: https://www.it.uu.se/research/group/astra/ModRef10/papers/Alan%20M.%20Frisch%20and%20Paul%20A.%20Giannoros.%20SAT%20Encodings%20of%20the%20At-Most-k%20Constraint%20-%20ModRef%202010.pdf
    # after an instance is created with appropriate values, call self.buildCNF on that object -> self.cnf will now contain the appropriate CNF

    def __init__(self, k, args, counter):
        # args is the list of n variables of which we will want to say "atMost k of n"
        # to not have any naming conflicts, we also need to now, what the highest index of any variable prev occuring was
        self.n = len(args)
        self.args = args
        self.counter = counter
        self.k = k
        self.B = []
        self.T = []
        self.bitStrings = []
        self.numberOfNewVars = 0
        self.cnf = []

    def buildCNF(self):
        # as no methods other than self.buildCNF need to be used outside of this class, we tie them together under this method
        self.initB()
        self.initT()
        self.initBitStrings()
        self.renameExtraVars()
        self.atMost()

    def initB(self):
        for i in range(1, self.k + 1):
            res = []
            for g in range(1, math.ceil(math.log(self.n, 2)) + 1):
                res.append(g)
            self.B.append(res)

    def initT(self):
        for g in range(1, self.k + 1):
            res = []
            for i in range(1, self.n + 1):
                res.append(i)
            self.T.append(res)

    def renameExtraVars(self):
        # the extraVars are those in self.B and self.T. As vars they need to be integers, and to not have any conflicts, they ought
        # to be >self.highestPrevVarIndex. This function is to be called after self.T and self.B are initialized!

        # first rename vars in self.B:
        for i in range(0, len(self.B)):
            for j in range(0, len(self.B[i])):
                self.B[i][j] = next(self.counter)

        # now rename vars in self.T
        for i in range(0, len(self.T)):
            for j in range(0, len(self.T[i])):
                self.T[i][j] = next(self.counter)

    def initBitStrings(self):
        self.bitStrings = list(self.bitStringGenerator())

    def bitStringGenerator(self):
        l = math.ceil(math.log(self.n, 2))
        # returns generator for bitStrings, is used in to initialize self.bitStrings
        chars = "01"
        for item in itertools.product(chars, repeat=l):
            yield "".join(item)

    def phi(self, i, g, j):
        sign = 1 if self.bitStrings[i - 1][j - 1] == '1' else -1
        return sign * self.B[g - 1][j - 1]

    def atMost(self):
        # adds to self.cnf clauses representing "at most k of n" with all vars renamed appropriately
        # this corresponds to the second of the protruding formulas on p. 4 of the Frisch et al. paper
        for i in range(1, self.n + 1):
            # res now becomes the clause of width k+1
            res = [(-1) * self.args[i - 1]]
            for k in range(1, self.k + 1):
                res.append(self.T[k - 1][i - 1])
            self.cnf.append(res)

            # now we add to self.cnf in two further loops the clauses of width 2
            for g in range(1, self.k + 1):
                for j in range(1, math.ceil(math.log(self.n, 2)) + 1):
                    self.cnf.append([(-1) * self.T[g - 1][i - 1], self.phi(i, g, j)])
