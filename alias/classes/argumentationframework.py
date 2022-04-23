from collections import OrderedDict, defaultdict
import matplotlib.pyplot as plt
import networkx as nx

from alias.classes.solvers import ExtensionType
from alias.classes.matrix import Matrix
from alias.classes.argument import Argument
from alias.classes.semantics.extensionManager import ExtensionManager
from alias.classes.solvers.solverManager import SolverManager


class ArgumentationFramework(object):

    def __init__(self, name):
        self.name = name  # Name of the framework
        self.arguments = OrderedDict()  # collection of all arguments in the framework
        self.mapping = {}
        self.attacks = []  # collection of all attacks in the framework
        self._matrix = None  # matrix representation of the framework
        self.__extensionManager = ExtensionManager()
        self.__solverManager = SolverManager()

    @property
    def matrix(self):
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

    def __contains__(self, arg):
        return arg in self.arguments

    def __iter__(self):
        return iter(self.arguments)

    def __getitem__(self, arg):
        return self.arguments[arg]

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
        self.__solverManager.dirty = True

    def get_args_count(self):
        return len(self.arguments)

    def get_attacks_count(self):
        return len(self.attacks)

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
        self.__solverManager.dirty = True

    def get_attackers(self, argument):
        assert self.__contains__(argument)
        argument: Argument = self.arguments[argument]
        return argument.attacked_by

    def __get_graph(self):
        graph = nx.DiGraph()
        for n in self.arguments.keys():
            graph.add_node(n)
        for n in self.attacks:
            graph.add_edge(n[0], n[1])
        return graph

    def draw_graph(self):
        """
        Method to draw directed graph of the argumentation framework
        :return:
        """
        graph = self.__get_graph()
        pos = nx.spring_layout(graph, k=0.30, iterations=20)
        nx.draw_networkx_nodes(graph, pos)
        nx.draw_networkx_labels(graph, pos)
        nx.draw_networkx_edges(graph, pos)
        plt.show()

    def get_stable_extension(self):
        return self.__solverManager.get_extension(ExtensionType.STABLE, self.arguments, self.attacks, self.matrix)

    def get_some_stable_extension(self):
        return self.__solverManager.get_some_extension(ExtensionType.STABLE, self.arguments, self.attacks, self.matrix)

    def get_complete_extension(self):
        return self.__solverManager.get_extension(ExtensionType.COMPLETE, self.arguments, self.attacks, self.matrix)

    def get_some_complete_extension(self):
        return self.__solverManager.get_some_extension(ExtensionType.COMPLETE, self.arguments, self.attacks, self.matrix)

    def get_preferred_extension(self):
        return self.__solverManager.get_extension(ExtensionType.PREFERRED, self.arguments, self.attacks, self.matrix)

    def get_some_preferred_extensions(self):
        return self.__solverManager.get_some_extension(ExtensionType.PREFERRED, self.arguments, self.attacks, self.matrix)

    def is_credulously_accepted(self, extension: ExtensionType, argument):
        return self.__solverManager.is_credulously_accepted(extension, self.arguments, self.attacks, argument, self.matrix)

    def is_skeptically_accepted(self, extension: ExtensionType, argument):
        return self.__solverManager.is_skeptically_accepted(extension, self.arguments, self.attacks, argument, self.matrix)
