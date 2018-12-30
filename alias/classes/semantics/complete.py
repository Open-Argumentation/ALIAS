import numpy

from alias.classes.matrix import Matrix
from alias.classes.semantics import BaseExtension


class Complete(BaseExtension):
    def verify_solution(self, solution, arguments, matrix):
        yield self.__is_complete_extension(solution, arguments, matrix)

    @staticmethod
    def __is_complete_extension(solution, arguments, matrix: Matrix):
        my_result = False
        if solution:
            args_to_check = [arguments[x].mapping for x in set(arguments.keys()) - set(solution)]
            args_mappings = [arguments[x].mapping for x in solution]
            my_column_vertices = matrix.get_sub_matrix(args_mappings, args_to_check)
            my_row_vertices = matrix.get_sub_matrix(args_to_check, args_to_check)

            my_sum_column_vertices = my_column_vertices.sum(axis=0).tolist()
            my_sum_row_vertices = my_row_vertices.sum(axis=0).tolist()

            sub_block = []
            counter = 0
            for v in zip(my_sum_row_vertices[0], my_sum_column_vertices[0]):
                if v[1] == 0:
                    sub_block.append(counter)
                    if v[0] < 1:
                        return False
                counter += 1

            test = numpy.where(my_row_vertices == 1)
            counter = 0

            check = {}
            for v in test[0]:
                if test[1][counter] in sub_block and my_sum_column_vertices[0][v] != 0 and test[1][counter] not in check:
                    check[test[1][counter]] = False
                else:
                    check[test[1][counter]] = True
                counter += 1
            my_result = False if False in check.values() else True
        return my_result
