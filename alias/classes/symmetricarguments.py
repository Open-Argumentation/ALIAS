import numpy
import sys

class SymmetricArguments(object):
    def __init__(self, arguments, matrix):
        self.clean = []
        self.combinations = []
        self.symmetric = dict()
        self.collection = []
        self.get_symmetric_arguments(arguments, matrix)
        sys.setrecursionlimit(1500)

    def get_symmetric_arguments(self, arguments, matrix):
        for arg in arguments.values():
            row = numpy.asarray(matrix.to_dense[arg.mapping, :])
            column = numpy.transpose(numpy.asarray(matrix.to_dense[:, arg.mapping]))
            if (row == column).all():
                args = []
                for x in numpy.where(row == 1)[1]:
                    t = self.get_argument_from_mapping(x, arguments)
                    if t in arg.attacking and t in arg.attacked_by:
                        args.append(t)
                if args:
                    self.symmetric[arg.name] = args
                else:
                    self.symmetric[arg.name] = []
                self.collection.append(arg.name)
        for k, v in self.symmetric.items():
            for i in v:
                if i not in self.symmetric.keys():
                    self.symmetric[k].remove(i)
        clean = self.generate_clean_args()
        self.combinations.append(clean)
        self.generate_remaining_combinations(clean)


    def get_argument_from_mapping(self, mapping, arguments):
        for v in arguments:
            if arguments[v].mapping == mapping:
                return arguments[v].name
        return None

    def generate_clean_args(self):
        clean = []
        for k in self.symmetric:
            if not self.symmetric[k]:
                clean.append(k)
        if clean:
            self.clean.append(clean)
        return clean

    def generate_remaining_combinations(self, clean):
        for_generation = set(self.collection) - set(clean)
        for arg in for_generation:
            partial_solution = []
            self.consider_arg_with_set(arg, for_generation, partial_solution)
            if self.clean:
                for v in self.clean:
                    t = set(partial_solution) | set(v)
                    self.combinations.append(list(t))
            else:
                self.combinations.append(partial_solution)

    def consider_arg_with_set(self, arg, to_be_considered, partial_solution):
        conflict = False
        for v in partial_solution:
            if arg in self.symmetric[v]:
                conflict = True
                break
        if not conflict:
            partial_solution.append(arg)
            to_be_considered = set(to_be_considered) - set(arg) - set(self.symmetric[arg])
            if to_be_considered:
                for v in to_be_considered:
                    self.consider_arg_with_set(v, to_be_considered, partial_solution)
