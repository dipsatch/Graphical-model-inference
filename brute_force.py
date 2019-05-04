# Generates all the permutations of the possible values (0 & 1) for n random variables, using Recursion.
def genCombs(n):
    if n == 1:
        return [[0], [1]]
    combs = genCombs(n-1)
    list = []
    for c in [0, 1]:
        for item in combs:
            list.append([c] + item)
    return list

# Calculates the joint probability value for the given model with the trgt using all permutations.
def calcJoint(combs, trgt, model):
    if len(trgt) == 0: return 1
    res = 0
    for comb in combs:
        flag = True
        for k, v in trgt.items():
            if comb[k-1] != v:
                flag = False
                break
        if flag:
            res += model(comb)
    return res

# Gives the joint probability of Chain model for a particular permutation conf using the given probability values.
def chain(conf):
    pX1 = [0.05, 0.95]

    def getP(a, b):
        if a == b:
            return 0.95
        return 0.05

    res = pX1[conf[0]]
    for i in range(1, len(conf)):
        res *= getP(conf[i-1], conf[i])

    return res

# Gives the joint probability of Tree model for a particular permutation conf using the given probability values.
def tree(conf):
    pX1 = [0.05, 0.95]

    def getP(a, b):
        if a == b:
            return 0.95
        return 0.05

    res = pX1[conf[0]]
    for i in range(1, len(conf)):
        res *= getP(conf[int((i+1)/2)-1], conf[i])

    return res

#Gives the joint probability of Grid model for a particular permutation conf using the given probability values.
def grid(conf):
    pX1 = [0.5, 0.5]

    def getP(i, j, k=None):
        if k is None:
            if i == j:
                return 0.95
            return 0.05
        if i == j == k:
            return 0.99
        elif j == k:
            return 0.01
        return 0.5

    L = int(len(conf)**.5)
    res = 1
    for y in range(L):
        for x in range(L):
            i = L*y + x
            if y == x == 0: res *= pX1[conf[0]]
            elif x == 0:    res *= getP(conf[i-L], conf[i])
            elif y == 0:    res *= getP(conf[i-1], conf[i])
            else:           res *= getP(conf[i], conf[i-1], conf[i-L])
    return res

# Driver function that gets the permutations & computes the conditional probability P(Xf | Xe) = P(Xf, Xe) / P(Xe).
def main(model, param, trgt, cond):
    if model == chain:  combs = genCombs(param)
    elif model == tree: combs = genCombs(2 ** param - 1)
    else:               combs = genCombs(param * param)
    return calcJoint(combs, {**trgt, **cond}, model) / calcJoint(combs, cond, model)


print('::: CHAIN :::')
model = chain
param = 15
trgt = {5:1}
cond = {}
print('P(X5=1):', main(model, param, trgt, cond))
cond = {1:1}
print('P(X5=1 | X1=1):', main(model, param, trgt, cond))
cond = {1:1, 10:1}
print('P(X5=1 | X1=1, X10=1):', main(model, param, trgt, cond))
cond = {1:1, 10:1, 15:0}
print('P(X5=1 | X1=1, X10=1, X15=0):', main(model, param, trgt, cond))
print()

print('::: SMALL TREE :::')
model = tree
param = 4
trgt = {8:1}
cond = {}
print('P(X8=1):', main(model, param, trgt, cond))
cond = {12:1}
print('P(X8=1 | X12=1):', main(model, param, trgt, cond))
cond = {12:1, 7:1}
print('P(X8=1 | X12=1, X7=1):', main(model, param, trgt, cond))
cond = {12:1, 7:1, 15:0}
print('P(X8=1 | X12=1, X7=1, X15=0):', main(model, param, trgt, cond))
print()

print('::: SMALL GRID :::')
model = grid
param = 4
trgt = {6:1}
cond = {}
print('P(X6=1):', main(model, param, trgt, cond))
cond = {16:0}
print('P(X6=1 | X16=0):', main(model, param, trgt, cond))
cond = {16:0, 1:0}
print('P(X6=1 | X16=0, X1=0):', main(model, param, trgt, cond))
cond = {16:0, 1:0, 15:0}
print('P(X6=1 | X16=0, X1=0, X15=0):', main(model, param, trgt, cond))