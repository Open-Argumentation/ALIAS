import pycosat
import sys
from _ast import alias
from collections import OrderedDict, defaultdict, Counter
from operator import itemgetter

# import matplotlib.pyplot as plt
import networkx as nx

from alias.classes import Matrix, Argument
from alias.classes.maximalConflictFreeCollection import MaximalConflictFreeCollection



class ArgumentationFramework(object):

    def __init__(self, name):
        self.name = name  # Name of the framework
        self.frameworks = {}  # Dictionary of the sub frameworks
        self.arguments = OrderedDict()  # collection of all arguments in the framework
        self.mapping = {}
        self.attacks = []  # collection of all attacks in the framework
        self._matrix = None  # matrix representation of the framework
        self._args_to_defence_sets = defaultdict(list)
        self.attack_clauses = []
        # self._store = Store()

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
            # self._store.add_argument(self.arguments[arg])


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
        if [-self.arguments[attacked].clause_mapping, -self.arguments[attacker].clause_mapping] not in self.attack_clauses:
            self.attack_clauses.append((-self.arguments[attacker].clause_mapping, -self.arguments[attacked].clause_mapping))
        # self._store.add_attack((attacker, attacked))

    def draw_graph(self):
        """
        Method to draw directed graph of the argumentation framework
        :return:
        """
        graph = self.get_graph()
        pos = nx.spring_layout(graph, k=0.30, iterations=20)
        nx.draw_networkx_nodes(graph, pos)
        nx.draw_networkx_labels(graph, pos)
        nx.draw_networkx_edges(graph, pos)
        # plt.show()

    def get_arguments_not_attacked(self):
        not_attacked = []
        for k, arg in self.arguments:
            if len(arg).attacked_by == 0:
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
        result = set()
        for x in self.get_conflict_free_sets():
            if self.is_stable_extension(x):
                result.add(frozenset(x))
        return result

    def is_stable_extension(self, args):
        """
        Verifies if the provided argument(s) are stable extension using matrix
        :param args: list of arguments to be checked
        :return: True if the provided arguments are a stable extension, otherwise False
        """
        if set(self.get_attacks_of_set(args)) == (set(self.arguments).symmetric_difference(set(args))):
            return True
        return False
    
    def get_complete_extension(self):
        # for conflict_free in self.get_conflict_free_sets():
        return []

    def get_preferred_extension(self):
        """
        Method to geterate complete extension for the argumentation framework
        :return: list of sets of complete extension
        """
        result = set()
        for conflict_free in self.get_conflict_free_sets():
            if self.__is_preferred_extension(conflict_free):
                result.add(frozenset(conflict_free))
        return result


    def __is_preferred_extension(self, args):
        """
        Method to check if the given set is a preferred extension, based on the properties of the matrix
        :param args: list of arguments to be checked
        :return: True if set is a preferred extension
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

    def get_attacks_of_set(self, arg_set):
        """
        Generates the list of all attacks of the given set
        :param arg_set:
        :return:
        """
        my_return = []
        for arg in arg_set:
            my_return += self.arguments[arg].attacking
        return my_return
        # return [x[1] for x in self.attacks if x[0] in arg_set]

    def get_attackers_of_set(self, arg_set):
        """
        Generates the list of all attackers of the given set
        :param arg_set:
        :return:
        """
        return [x[0] for x in self.attacks if x[1] in arg_set]

    def test_of_parallel_dictionaries1(self):
        print('test')
        count = 0
        self.attacks.sort(key=itemgetter(0, 1))
        conflict_free_collection = MaximalConflictFreeCollection()
        conflict_free_collection.add_arguments(self.arguments)
        for attack in self.attacks:
            count += 1
            print('adding attack ' + str(count) + '/' +str(len(self.attacks)))
            conflict_free_collection.add_attack(attack)

        my_return = conflict_free_collection.get_conflict_free_sets()
        for v in my_return:
            if self.is_stable_extension(v):
                print(v)

    def test_of_parallel_dictionaries(self):
        conflict_free_collection = MaximalConflictFreeCollection(self.get_graph())
        for arg in self.arguments:
            conflict_free_collection.add_argument_object(self.arguments[arg])
        conflict_free_collection.create_max_conflict_free_sets()


        output = set()
        my_return = conflict_free_collection.get_conflict_free_sets()
        for v in my_return:
            if self.is_stable_extension(v):
                output.add(frozenset(v))
        return output

    def get_graph(self):
        graph = nx.DiGraph()
        for n in self.arguments.keys():
            graph.add_node(n)
        for n in self.attacks:
            graph.add_edge(n[0], n[1])
        return graph

    def get_clauses_for_no_attacks(self):
        my_return = []
        for k, arg in self.arguments.items():
            if len(arg.attacking) ==0 and len(arg.attacked_by) == 0:
                my_return.append((arg.clause_mapping,))
        return my_return

    def get_conflict_free_sets(self):
        all_clauses = self.__get_admissible_cnf()
        c = Counter(map(tuple, all_clauses))
        duplicates = [k for k, v in c.items() if v > 1]
        for duplicate in duplicates:
            all_clauses.remove(list(duplicate))
        print(len(all_clauses))
        for clause in all_clauses:
            for solution in pycosat.itersolve(clause):
                mapped_sol = []
                for value in solution:
                    if value > 0:
                        mapped_sol.append(self.mapping[value])
                # print(mapped_sol)
                yield mapped_sol

    def __get_admissible_cnf(self):
        all_clauses = []
        no_attacks = self.get_clauses_for_no_attacks()

        def to_cnf(value):
            clauses = []
            name = self.mapping[value]
            self.__get_next_defence_arg(name, clauses)
            if len(self.arguments[name].attacking) == 0 and len(self.arguments[name].attacked_by) == 0:
                clauses.append((self.arguments[name].clause_mapping,))
            clauses = clauses + self.attack_clauses + no_attacks
            all_clauses.append(clauses)

        for k in self.arguments:
            to_cnf(self.arguments[k].clause_mapping)

        print(len(all_clauses))
        return all_clauses

    def __get_next_defence_arg(self, name, clauses, path=[]):
        path = path
        path.append(name)
        if self.arguments[name].attacking:
            for att in self.arguments[name].attacking:
                if self.arguments[att].attacking:
                    for next_att in self.arguments[att].attacking:
                        if next_att not in path and\
                                next_att != name and next_att not in self.arguments[name].attacking and \
                                {-self.arguments[name].clause_mapping,
                                 self.arguments[next_att].clause_mapping} not in clauses:
                            t = (self.arguments[name].clause_mapping, -self.arguments[next_att].clause_mapping)
                            clauses.append(t)
                            self.__get_next_defence_arg(next_att, clauses, path)
        else:
            return