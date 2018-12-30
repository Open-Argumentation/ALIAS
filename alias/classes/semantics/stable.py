from alias.classes.matrix import Matrix
from alias.classes.semantics import BaseExtension


class Stable(BaseExtension):
    def verify_solution(self, solution: list, arguments: dict, matrix: Matrix):
        return self.__is_stable_extension(solution, arguments)
        pass

    def __is_stable_extension(self, solution, arguments: dict):
        if set(self.__get_attacks_of_set(solution, arguments)) == (set(arguments).symmetric_difference(set(solution))):
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
