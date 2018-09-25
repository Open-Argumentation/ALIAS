from scipy import sparse


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
        return (self._matrix.todense()[rows, :])[:, columns]
