import ntpath
from collections import OrderedDict, defaultdict
from operator import itemgetter

from memory_profiler import profile
from scipy import sparse
import sys
import networkx as nx
import matplotlib.pyplot as plt
import numpy
from sortedcontainers import SortedList

from alias.classes import Matrix, Argument, Framework, SymmetricArguments


class ArgumentationFramework(object):

    def __init__(self, name):
        self.name = name  # Name of the framework
        self.frameworks = {}  # Dictionary of the sub frameworks
        self.arguments = OrderedDict()  # collection of all arguments in the framework
        self.attacks = []  # collection of all attacks in the framework
        self._matrix = None  # matrix representation of the framework
        self._args_to_defence_sets = defaultdict(list)

    @property
    def matrix(self):
        if self._matrix is None:
            self._matrix = Matrix(self.arguments, self.attacks)
        return self._matrix

    def __str__(self):
        """
        String representation of the Argumentation Framework
        :return: 
        """
        my_string = 'Argumentation Framework: \n'
        my_string += 'Argument\tAttacks\tAttacked by\n'
        for a in self.arguments:
            my_string += a
            my_string += '\t'
            my_string += '|'
            for att in self.arguments[a].attacking:
                my_string += att + ', '
            my_string += '\t|'
            for att in self.arguments[a].attacked_by:
                my_string += att + ', '
            my_string += '|\n'
        return my_string

    def add_argument(self, arg):
        """
        Method to add argument to argumentation framework
        :param arg: Name of the argument to be added
        :return:
        """
        if arg not in self.arguments:
            counter = len(self.arguments)
            self.arguments[arg] = Argument(arg, counter)

    def get_argument_from_mapping(self, mapping):
        """
        Method to get argument name from the mapping in the matrix
        :param mapping: row/column index in the matrix representation of the AF
        :return: 
        """
        for v in self.arguments:
            if self.arguments[v].mapping == mapping:
                return self.arguments[v].name
        return None

    def __get_keys(self, value):
        """
        Method to get all keys from arguments dict which have value 'value'
        :param value: value to find
        :return: 
        """
        my_return = []
        for k, v in self.arguments.items():
            if v == value:
                my_return.append(k)
        return my_return

    def add_attack(self, attack):
        """
        Method to add attack to argumentation framework
        :param attacker: argument that attacks 'attacked'
        :param attacked: argument attacked by 'attacker'
        :return:
        """
        attacker = attack[0]
        attacked = attack[1]
        if attacker not in self.arguments:
            self.add_argument(attacker)
        if attacked not in self.arguments:
            self.add_argument(attacked)
        self.attacks.append((attacker, attacked))
        self.arguments[attacker].attacking.append(attacked)
        self.arguments[attacked].attacked_by.append(attacker)

    def draw_graph(self):
        """
        Method to draw directed graph of the argumentation framework
        :return:
        """
        graph = nx.DiGraph()

        for n in self.arguments.keys():
            graph.add_node(n)
        for n in self.attacks:
            graph.add_edge(n[0], n[1])
        pos = nx.spring_layout(graph, k=0.30, iterations=20)
        nx.draw_networkx_nodes(graph, pos)
        nx.draw_networkx_labels(graph, pos)
        nx.draw_networkx_edges(graph, pos)
        plt.show()

    def get_arguments_not_attacked(self):
        # TODO This won't work in the current setup - dict of arguments does not hold argument objects
        not_attacked = []
        for arg in self.arguments:
            if not self.arguments.get(arg).attacked_by:
                not_attacked.append(arg)
        return not_attacked

    def get_grounded_labelling(self):
        """
        TODO Needs to be reviewed in terms of the matrix
        Generate Grounded labelling
        :return: 
        """
        in_set = set(self.get_arguments_not_attacked())
        out_set = set()
        test = True
        grounded_ext = {
            'in': in_set.copy(),
            'out': set(),
            'undec': set()
        }

        while test:
            grounded_ext_copy = grounded_ext.copy()

            for arg in in_set:
                for next_arg in self.arguments.get(arg).attacking:
                    if set(self.arguments[next_arg].attacked_by).issubset(grounded_ext['in']):
                        out_set.add(next_arg)

            for arg in in_set:
                grounded_ext['in'].add(arg)
            in_set.clear()

            for arg in out_set:
                for next_arg in self.arguments.get(arg).attacking:
                    if set(self.arguments[next_arg].attacked_by).issubset(grounded_ext['out']):
                        in_set.add(next_arg)

            for arg in out_set:
                grounded_ext['out'].add(arg)
            out_set.clear()

            if grounded_ext == grounded_ext_copy:
                test = False

            for arg in self.arguments:
                if arg not in grounded_ext['in'] and arg not in grounded_ext['out']:
                    grounded_ext['undec'].add(arg)
        return grounded_ext

    def get_stable_extension(self):
        """
        Method to test if can get stable extensions only from the list of rows/columns in matrix where value is 0
        :return:
        """
        # TODO Should remove all elements which are not attacked nor attacking any other element first
        my_return = []
        test = self.get_conflict_free_sets()
        for v in test.solutions:
            if self.is_stable_extension(v):
                my_return.append(set(v))
        return my_return

    def is_stable_extension(self, args):
        """
        Verifies if the provided argument(s) are stable extension using matrix
        :param framework: subframework of the Argumentation framework
        :param args: list of arguments to be checked
        :return: True if the provided arguments are a stable extension, otherwise False
        """
        # This is commented out as using zero sub blocks from matrix
        if args:
            my_labels = [self.arguments[x].mapping for x in args]
            my_column_vertices = self.matrix.get_sub_matrix(set(my_labels), [x for x in
                                                                          set(range(len(
                                                                              self.arguments))).symmetric_difference(
                                                                              my_labels)])
            a = my_column_vertices.sum(axis=0).tolist()
            for row in my_column_vertices.sum(axis=0).tolist():
                for v in row:
                    if v == 0:
                        return False
            return True
        return False

    # @profile
    def get_conflict_free_sets(self):
        """
        Method to generate maximal conflict free sets of argumentation framework
        :return:
        """
        done_attacks = []
        my_return = ConflictFree(list(self.arguments.keys()))
        self.attacks.sort(key=itemgetter(0))
        for attack in self.attacks:
            already_done = False
            if [attack[1], attack[0]] in done_attacks:
                already_done = True
            if not already_done:
                my_return.add(attack)
                done_attacks.append(list(attack))
        return my_return

    def get_complete_extension(self):
        """
        Method to geterate complete extension for the argumentation framework
        :return: list of sets of complete extension
        """
        my_return = []
        for v in self.__get_maximal_admissible_sets():
            if self.__is_complete_extension(v):
                my_return.append(set(v))
        t = self.__get_minimal_admissible_sets()
        for v in self.__get_minimal_admissible_sets():
            if self.__is_complete_extension(v):
                my_return.append(set(v))
        return my_return

    def __is_complete_extension(self, args):
        """
        Method to check if the given set is a complete extension, based on the properties of the matrix
        :param args: list of arguments to be checked
        :return: True if set is a complete extension
        """
        if args:
            arguments_to_check = [self.arguments[x].mapping for x in self.arguments if x not in args and x not in self.get_attacks_of_set(args)]
            if not arguments_to_check:
                return True
            else:
                my_column_vertices = self.matrix.get_sub_matrix(arguments_to_check, arguments_to_check)
                for row in my_column_vertices.sum(axis=0).tolist():
                    for v in row:
                        if v == 0:
                            return False
                return True
        return False

    def __build_admissible_sets_from_minimal_sets(self, minimal_admissible_sets):
        for v in minimal_admissible_sets:
            print(v)

    """
    Those methods are based on dungAF implementation
    """
    def __get_minimal_admissible_sets(self):
        defence_sets = []
        for arg in self.arguments:
            if arg not in self.arguments:
                return None;
            elif arg not in self._args_to_defence_sets:
                self.__get_admissible_set_from_argument(arg, defence_sets, [])
        return defence_sets

    def __get_admissible_set_from_argument(self, arg, defence_sets, checked_arguments=[], is_in=True):
        checked_arguments.append(arg)

        if self.arguments[arg].attacked_by:
            if set(self.arguments[arg].attacking).intersection(set(self.arguments[arg].attacked_by)) == set(self.arguments[arg].attacked_by) and is_in:
                defence_sets.append([arg])

            for attacker in self.arguments[arg].attacked_by:
                if attacker not in self.arguments[arg].attacking:
                    possible_solutions = defence_sets
                    if is_in:
                        self.__get_admissible_set_from_argument(attacker, possible_solutions, checked_arguments, False)
                    else:
                        self.__get_admissible_set_from_argument(attacker, possible_solutions, checked_arguments, True)
        elif is_in:
            defence_sets.append([arg])
            return

    def __get_maximal_admissible_sets(self):
        """
        Return list of the maximal admissible sets from the argumentation framework
        :return:
        """
        maximal_conflict_free = self.get_conflict_free_sets()
        for v in maximal_conflict_free.solutions:
            if set(self.get_attackers_of_set(v)).issubset(self.get_attacks_of_set(v)):
                yield v


    def get_defence_set_around_argument_helper_dungAF(self, current_arg, args_list=[], candidate_solution=[]):
        accumulated_candidate_solutions = []
        relevant_candidate_solutions = []
        self_defensive_candidate_solutions = []

        on_pro_arg = len(args_list) % 2 == 0

        if on_pro_arg and current_arg in self.arguments[current_arg].attacking:
            return None

        args_list.append(current_arg)

        if on_pro_arg:
            if candidate_solution:
                for v in candidate_solution:
                    v.append(current_arg)
            else:
                candidate_solution.append([current_arg])
        else:
            accumulated_candidate_solutions = []

        for attacker in self.arguments[current_arg].attacked_by:
            if attacker not in args_list:
                relevant_candidate_solutions = []
                if on_pro_arg:
                    self_defensive_candidate_solutions = []
                for solution in candidate_solution:
                    if on_pro_arg:
                        t = self.arguments[attacker].attacked_by
                        # print('------------------')
                        # print(set(t))
                        # print(solution)
                        # print(set(t).intersection(set(solution)))

                        if t and len(set(t).intersection(set(solution))) == 0:
                            relevant_candidate_solutions.append(solution)
                        else:
                            self_defensive_candidate_solutions.append(solution)
                    else:
                        to_test = []
                        for v in solution:
                            to_test.append(self.arguments[v].mapping)
                        to_test.append(self.arguments[attacker].mapping)
                        if self.matrix.is_set_conflict_free(to_test):
                            relevant_candidate_solutions.append(solution)

                candidate_solution = self.get_defence_set_around_argument_helper_dungAF(attacker, args_list, relevant_candidate_solutions)

                if on_pro_arg:
                    for v in self_defensive_candidate_solutions:
                        candidate_solution.append(v)
                    # remove all non-minimal members of can-sols
                    if not candidate_solution:
                        return
                else:
                    for v in candidate_solution:
                        accumulated_candidate_solutions.append(v)
                    # remove all non-minimal members of accumulated_candidate_solutions

        if not on_pro_arg:
            if self.arguments[current_arg].attacked_by:
                candidate_solution = accumulated_candidate_solutions
            else:
                candidate_solution = []

        args_list.remove(current_arg)
        return candidate_solution

    def get_attacks_of_set(self, arg_set):
        """
        Generates the list of all attacks of the given set
        :param arg_set:
        :return:
        """
        return [x[1] for x in self.attacks if x[0] in arg_set]

    def get_attackers_of_set(self, arg_set):
        """
        Generates the list of all attackers of the given set
        :param arg_set:
        :return:
        """
        return [x[0] for x in self.attacks if x[1] in arg_set]

"""
Those objects are used to create maximal conflict free sets
"""
class ConflictFree(object):
    def __init__(self, arguments):
        self.solutions = set()
        self.solutions.add(frozenset(arguments))

    def add(self, attack):
        elements = [x for x in self.solutions if set(list(attack)) < x or set(list(attack)) == x]
        for v in elements:
            self.solutions.remove(v)
            self.solutions.add(frozenset(set(list(v)) - set([attack[1]])))
            self.solutions.add(frozenset(set(list(v)) - set([attack[0]])))
