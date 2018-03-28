from collections import defaultdict
import numpy
from scipy import sparse
from itertools import combinations


class Matrix(object):
    def __init__(self, arguments=[], attacks=[], mapping=True):
        """
        Object constructor
        :param arguments: List of arguments objects
        :param attacks: List of attacks
        """
        self._mapping = mapping
        self._arguments = None
        self._matrix = self.__create_matrix(arguments, attacks)

    @property
    def shape(self):
        return self._matrix.shape

    @property
    def to_dense(self):
        return self._matrix.todense()

    def __create_matrix(self, arguments, attacks):
        """
        Method used to create the matrix for the argumentation framework
        :return:
        """
        if self._mapping:
            return sparse.coo_matrix(([1] * len(attacks), ([arguments[v[0]].mapping for v in attacks],
                                                       [arguments[v[1]].mapping for v in attacks])),
                                     shape=(len(arguments), len(arguments)))
        else:
            self._arguments = {v: arguments.index(v) for v in arguments}
            return sparse.coo_matrix(([1] * len(attacks), ([self._arguments[v[0]] for v in attacks],
                                                           [self._arguments[v[1]] for v in attacks])),
                                     shape=(len(arguments), len(arguments)))

    def get_sub_matrix(self, rows, columns):
        """
        Gets submatrix from the main matrix based on the rows and columns provided
        :param rows: indexes of rows to be included
        :param columns: indexes of columns to be included
        :return: sub matrix of original matrix limited to rows and columns provided
        """
        return (self._matrix.todense()[list(rows), :])[:, list(columns)]

    def get_sub_blocks_with_zeros(self):
        """
        Method to generate all sub blocks from original matrix where all values are 0's. Not efficient
        :return: list of sets of indexes for matrix where values in corresponding rows/columns are 0's
        """
        my_matrix = self.to_dense
        my_return = []
        test = defaultdict(set)
        zeros = numpy.where(my_matrix == 0)
        for k, v in zip(zeros[0], zeros[1]):
            test[k].add(v)
        for v in range(0, my_matrix.shape[0]):
            possible_combinations = combinations(range(my_matrix.shape[0]), v + 1)
            for comb in possible_combinations:
                my_sets = [test[x] for x in comb]
                intersection = set(comb).intersection(*my_sets)
                if len(intersection) == len(comb):
                    my_return.append(list(intersection))
        return my_return

    def get_mappings(self):
        if self._arguments is not None:
            return self._arguments

    def is_set_conflict_free(self, set_to_test):
        matrix_to_test = self.get_sub_matrix(set_to_test, set_to_test)
        if len(numpy.where(matrix_to_test == 1)[0]) > 0:
            return False
        return True
