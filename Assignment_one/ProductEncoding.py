import math, itertools, copy


class ProductEncoding:
    def __init__(self, k, args, highestPrevVarIndex):
        self.n = len(args)
        self.args = args
        self.k = k
        self.highestPrevVarIndex = highestPrevVarIndex
        self.newHighestVarIndex = 0
        self.numberOfNewVars = 0
        self.P = []  # once initialized, will define domain for tuples representing args; every entry >= 2
        self.argsRepresentations = []  # once initialized, will contain a 1:1 mapping from arguments to k+1 tuples
        self.tuplesNumbering = []  # will contain a numbering of the k+1-tuples
        self.A = []  # will contain the new variables
        self.factorTuples = []  # will contain tuples x/d for all tuples used and all 1 <= d <= k+1

    def initP(self):
        # initializes self.P with a list of k+1 numbers p_i which determine the domain (cart. prod.) of tuples representing args
        # self.P is minimal w.r.t the highest occuring number in it
        # important: For each i: p_i has to be at least 2!
        res = [2 for x in range(0, self.k + 1)]
        cond = math.prod(res) >= self.n
        l = 0
        while (not cond):
            res[l % len(res)] += 1
            l += 1
            cond = math.prod(res) >= self.n
        self.P = res

    def initArgsRepres(self):
        # sets self.argsRepresentations to a mapping (i.e. tuples) between args and k+1-tuples
        cartProd = list(itertools.product(*(list(map(lambda x: list(range(1, x + 1)), self.P)))))
        cartProd = list(map(lambda x: list(x), cartProd))  # make tuples into list

        # this adds the k+2 tuples [1,1..1], [2,1..1], [1,2..1]..[1,1..2] which ensure the recursive function call to have
        # strictly fever args: on top of p. 8 in Frisch et al.
        avoid = [[1 for x in range(0, self.k + 1)]]
        for j in range(0, self.k + 1):
            avoid.append([1 for i in range(0, self.k + 1)])
            avoid[-1][j] = 2

        # add pairs of args and k+1-tuples to our mapping. Keep track of which tuples where already added
        # start with adding those from avoid, to ensure they cerainly appear
        counter = 0
        argToRepresMap = []
        alreadyUsed = []

        for k in range(0, len(self.args)):
            if (counter >= self.k + 2):
                break
            argToRepresMap.append((self.args[counter], avoid[counter]))
            alreadyUsed.append(avoid[counter])
            counter += 1

        for k in range(0, len(self.args) - (self.k + 2)):
            argToRepresMap.append((self.args[counter], [x for x in cartProd if not x in alreadyUsed][0]))
            alreadyUsed.append([x for x in cartProd if not x in alreadyUsed][0])
            counter += 1
        self.argsRepresentations = argToRepresMap

    def initFactorTuples(self):
        # only to be used after the two above init methods are called
        # will set self.factorTuples to a list of all tuples x_i factored to d, with 1 <= d <= k+1; factored means the tuple:
        # x_i/d which is the result of removing position d from x_i. Duplicates will be removed. In the end, we will identify
        # the resulting factor tuples with numbers 0...l, s.t. self.factorTuples will be a list of 2-tuples (j, x_i/d)
        alreadyUsed = [x for (_, x) in self.argsRepresentations]
        for d in range(0, self.k):
            for tup in alreadyUsed:
                res = copy.deepcopy(tup)
                del res[d]
                self.factorTuples.append(res)
        self.factorTuples.sort()
        self.factorTuples = list(
            self.factorTuples for self.factorTuples, _ in itertools.groupby(self.factorTuples))  # remove duplicates
        for k in range(0, len(self.factorTuples)):
            self.factorTuples[k] = (k, self.factorTuples[k])

    def initTuplesNumbering(self):
        # TODO: is this even used?
        tuples = [x for (_, x) in self.argsRepresentations]
        counter = 0
        for k in tuples:
            self.tuplesNumbering.append((counter, k))
            counter += 1

    def initA(self):
        # simply creates 2D array, with all 1's as entries, and appropriate lengths, s.t. access with appropriate indices is possible
        for d in range(0, self.k + 1):
            res = []
            for y in range(0, len(self.factorTuples)):
                res.append(1)
            self.A.append(res)

    def renameA(self):
        # gives the entries in 2D list self.A new names. As they represent variables, we need count from the prevHighestVarIndex
        counter = self.highestPrevVarIndex + 1
        for d in range(0, self.k + 1):
            for y in range(0, len(self.factorTuples)):
                self.A[d][y] = counter
                counter += 1

    def initialize(self):
        self.initP()
        self.initArgsRepres()
        self.initFactorTuples()
        self.initTuplesNumbering()
        self.initA()
        self.renameA()
        self.numberOfNewVars = self.newHighestVarIndex - self.highestPrevVarIndex

    def returnCNF(self):
        if (self.k == 0):
            return [[-x] for x in self.args]
        if (self.k == 1):
            res = []
            for i in range(0, len(self.args) - 1):
                for j in range(i + 1, len(self.args)):
                    res.append([-self.args[i], -self.args[j]])
            return res
        if (self.n == self.k + 1):
            return [[-x for x in self.args]]
        self.initialize()
        res = []
        for d in range(0, self.k + 1):
            argsForRecursionCall = []
            for x in self.argsRepresentations:
                (n, m) = x
                m2 = copy.deepcopy(m)
                del m2[d]
                factor = [x for (x, y) in self.factorTuples if y == m2][0]
                res.append([(-1) * n, self.A[d][factor]])
                argsForRecursionCall.append(self.A[d][factor])
            self.newHighestVarIndex = max([item for sublist in res for item in sublist])
            argsForRecursionCall = list(dict.fromkeys(argsForRecursionCall))  # remove duplicates
            recursionCNF = ProductEncoding(self.k, argsForRecursionCall, self.newHighestVarIndex)
            res.extend(recursionCNF.returnCNF())
            self.newHighestVarIndex = recursionCNF.newHighestVarIndex
        return res


def exactly_k_Of_n(k, args, maxPrevVarIndex):
    productAtMost = ProductEncoding(k, args, maxPrevVarIndex)
    productAtLeast = ProductEncoding(len(args) - k, list(map(lambda x: (-1) * x, args)),
                                     productAtMost.numberOfNewVars + maxPrevVarIndex)

    return productAtMost.returnCNF() + productAtLeast.returnCNF()