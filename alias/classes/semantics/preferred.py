from alias.classes.matrix import Matrix
from alias.classes.semantics import BaseExtension


class Preferred(BaseExtension):

    def verify_solution(self, solution: list, arguments: dict, matrix: Matrix):
        return self.__is_preferred_extension(solution, arguments, matrix)

    def __is_preferred_extension(self, solution, arguments, matrix):
        """
        Method to check if the given set is a preferred extension, based on the properties of the matrix
        :param solution: list of arguments to be checked
        :return: True if set is a preferred extension
        """
        if solution:
            args_to_check = set(arguments.keys()) - set(solution) - set(self.__get_attacks_of_set(solution, arguments))
            arguments_to_check = [arguments[x].mapping for x in args_to_check]
            if not arguments_to_check:
                return True
            else:
                my_column_vertices = matrix.get_sub_matrix(arguments_to_check, arguments_to_check)
                sum_of_vertices = my_column_vertices.sum(axis=0).tolist()[0]
                for v in sum_of_vertices:
                    if v == 0:
                        return False
            return True
        return False

    def __get_attacks_of_set(self, arg_set, arguments):
        """
        Generates the list of all attacks of the given set
        :param arg_set:
        :return:
        """
        my_return = []
        for arg in arg_set:
            my_return += arguments[arg].attacking
        return my_return
