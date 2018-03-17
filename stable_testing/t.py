from collections import defaultdict
import itertools
import numpy

matrix = numpy.matrix('0 1 0 0; 1 0 1 0; 0 1 0 0; 0 1 0 0')

my_return = []
test = defaultdict(set)
zeros = numpy.where(matrix == 0)
for k, v in zip(zeros[0], zeros[1]):
    test[k].add(v)

for v in range(0, matrix.shape[0]):
    combinations = itertools.combinations(range(matrix.shape[0]), v+1)
    for comb in combinations:
        my_sets = [test[x] for x in comb]
        intersection = set(comb).intersection(*my_sets)
        if len(intersection) == len(comb):
            my_return.append(intersection)

print(my_return)


