import pycosat
from collections import OrderedDict, defaultdict, Counter
from operator import itemgetter

import matplotlib.pyplot as plt
import networkx as nx

from alias.classes import Matrix, Argument



class ArgumentationFramework(object):

    def __init__(self, name):
        self.name = name  # Name of the framework
        self.arguments = OrderedDict()  # collection of all arguments in the framework
        self.mapping = {}
        self.attacks = []  # collection of all attacks in the framework
        self._matrix = None  # matrix representation of the framework
        self._args_to_defence_sets = defaultdict(list)
        self.attack_clauses = []

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
            self.arguments[arg] = Argument(arg, counter, counter+1)
            self.mapping[counter+1] = arg

    def add_attack(self, attack):
        """
        Method to add attack to argumentation framework
        :param attack: tuple of attack
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
        # check if the reverse clause is not already present
        if (-self.arguments[attacked].clause_mapping, -self.arguments[attacker].clause_mapping) not in self.attack_clauses:
            self.attack_clauses.append((-self.arguments[attacker].clause_mapping, -self.arguments[attacked].clause_mapping))
        # self._store.add_attack((attacker, attacked))

    def draw_graph(self):
        """
        Method to draw directed graph of the argumentation framework
        :return:
        """
        def get_graph():
            graph = nx.DiGraph()
            for n in self.arguments.keys():
                graph.add_node(n)
            for n in self.attacks:
                graph.add_edge(n[0], n[1])
            return graph

        graph = get_graph()
        pos = nx.spring_layout(graph, k=0.30, iterations=20)
        nx.draw_networkx_nodes(graph, pos)
        nx.draw_networkx_labels(graph, pos)
        nx.draw_networkx_edges(graph, pos)
        plt.show()

    def get_stable_extension(self):
        """
        Method to test if can get stable extensions only from the list of rows/columns in matrix where value is 0
        :return:
        """
        result = set()
        conflict_free = self.get_conflict_free_sets()
        for x in conflict_free:
            if self.__is_stable_extension(x):
                result.add(frozenset(x))
        return result

    def __is_stable_extension(self, args):
        """
        Verifies if the provided argument(s) are stable extension using matrix
        :param args: list of arguments to be checked
        :return: True if the provided arguments are a stable extension, otherwise False
        """
        if set(self.__get_attacks_of_set(args)) == (set(self.arguments).symmetric_difference(set(args))):
            return True
        return False
    
    def get_complete_extension(self):
        result = set()
        conflict_free = self.get_conflict_free_sets()
        for x in conflict_free:
            if self.__is_complete_extension(x):
                result.add(frozenset(x))
        return result

    def __is_complete_extension(self, args):
        return False

    def get_preferred_extension(self):
        """
        Method to geterate complete extension for the argumentation framework
        :return: list of sets of complete extension
        """
        result = set()
        conflict_free = self.get_conflict_free_sets()
        for x in conflict_free:
            if self.__is_preferred_extension(x):
                result.add(frozenset(x))
        return result


    def __is_preferred_extension(self, args):
        """
        Method to check if the given set is a preferred extension, based on the properties of the matrix
        :param args: list of arguments to be checked
        :return: True if set is a preferred extension
        """
        if args:
            args_to_check = set(self.arguments.keys()) - set(args) - set(self.__get_attacks_of_set(args))
            arguments_to_check = [self.arguments[x].mapping for x in args_to_check]
            if not arguments_to_check:
                return True
            else:
                my_column_vertices = self.matrix.get_sub_matrix(arguments_to_check, arguments_to_check)
                sum_of_vertices = my_column_vertices.sum(axis=0).tolist()
                if 0 in sum_of_vertices:
                    return False
                return True
        return False

    def __get_attacks_of_set(self, arg_set):
        """
        Generates the list of all attacks of the given set
        :param arg_set:
        :return:
        """
        my_return = []
        for arg in arg_set:
            my_return += self.arguments[arg].attacking
        return my_return

    def __get_clauses_for_no_attacks(self):
        my_return = []
        for k, arg in self.arguments.items():
            if len(arg.attacking) ==0 and len(arg.attacked_by) == 0:
                my_return.append((arg.clause_mapping,))
        return my_return

    def get_conflict_free_sets(self):
        self.attack_clauses.sort(key=itemgetter(0,1), reverse=True)
        self.attacks.sort(key=itemgetter(0,1), reverse=False)
        all_clauses = self.__get_admissible_cnf()
        all_clauses = self.__remove_duplicate_clauses(all_clauses)
        for clause in all_clauses:
            for solution in pycosat.itersolve(clause):
                mapped_sol = []
                for value in solution:
                    if value > 0:
                        mapped_sol.append(self.mapping[value])
                yield mapped_sol

    def __remove_duplicate_clauses(self, all_clauses):
        c = Counter(map(tuple, all_clauses))
        duplicates = [(k, v) for k, v in c.items() if v > 1]
        for duplicate in duplicates:
            for _ in range(duplicate[1] - 1):
                all_clauses.remove(list(duplicate[0]))
        return all_clauses

    def __get_admissible_cnf(self):
        all_clauses = []
        no_attacks = self.__get_clauses_for_no_attacks()

        def to_cnf(value):
            clauses = []
            name = self.mapping[value]
            clauses.append((value,))

            self.__get_next_defence_arg(name, clauses, [])
            # if len(self.arguments[name].attacking) == 0 and len(self.arguments[name].attacked_by) == 0:
            clauses = clauses + self.attack_clauses + no_attacks
            if len(clauses) > 0:
                all_clauses.append(clauses)

        for k in self.arguments:
            to_cnf(self.arguments[k].clause_mapping)

        return all_clauses

    def __get_next_defence_arg(self, name, clauses, pathx=[]):
        path = pathx
        if name in path:
            return
        path.append(name)
        if self.arguments[name].attacking:
            # clauses.append((self.arguments[name].clause_mapping,))
            for att in self.arguments[name].attacking:
                # if att in path:
                #     return
                path_att = path.copy()
                path_att.append(att)
                if (-self.arguments[att].clause_mapping,) not in clauses:
                    clauses.append((-self.arguments[att].clause_mapping,))
                if self.arguments[att].attacking:
                    for next_att in self.arguments[att].attacking:
                        if next_att not in path and\
                                next_att != name and next_att not in self.arguments[name].attacking and \
                                (-self.arguments[name].clause_mapping, self.arguments[next_att].clause_mapping) not in clauses and \
                                (-self.arguments[next_att].clause_mapping, self.arguments[name].clause_mapping) not in clauses:
                            t = (self.arguments[name].clause_mapping, -self.arguments[next_att].clause_mapping)
                            clauses.append(t)
                            path_def = path_att.copy()
                            path_def.append(next_att)
                            self.__get_next_defence_arg(next_att, clauses, path_def.copy())
        else:
            return
