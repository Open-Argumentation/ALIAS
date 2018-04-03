from collections import defaultdict

from alias.classes import Node
import anytree as tl

class Tree(object):
    def __init__(self):
        self.level = 0
        self.levels = defaultdict(list)
        self.tree = tl.Node("root")
        self._args = {}
        self._root = tl.Node('root')
        self._args['root'] = 0
        tl.separator = ' -> '

    def add_node(self, attack):
        print(attack)
        if len(self._args) == 1:
            self.level += 1
            self.__add_attack(attack, self._root)
        else:
            if attack[0] not in self._args and attack[1] not in self._args:
                test = self.get_nodes_from_lowest_level()
                self.level += 1
                for x in test:
                    self.__add_attack(attack, x)
            else:
                a = self.get_nodes_from_lowest_level()
                b = self.get_nodes_from_lowest_level2(attack[0])
                test = set(self.get_nodes_from_lowest_level()) - set(self.get_nodes_from_lowest_level2(attack[0]))
                self.level += 1
                for x in test:
                    self.__add_attack(attack, x)

    def __add_attack(self, attack, parent):
        attacker = tl.Node(attack[0], parent=parent)
        self._args[attack[0]] = self.level
        attacked = tl.Node(attack[1], parent=parent)
        self._args[attack[1]] = self.level
        self.levels[self.level].append(attacker)
        self.levels[self.level].append(attacked)

    def get_lowest_level(self):
        if not self.level:
            return 0

    def get_nodes_from_lowest_level(self):
        """ This is if the argument does not exist in the tree """
        return [x.name for x in self.levels[self.level]]

    def get_nodes_from_lowest_level2(self, arg):
        """ This is when argument exists in the tree """
        if self._args[arg] != self.level:
            return [[node.name for node in children] for children in tl.LevelOrderGroupIter(self._root, filter_=lambda n: self._args[n.name] != self.level)]
        else:
            my_return = []
            for x in self.levels[self.level]:
                if x.name == str(arg):
                    my_return.append(x.name)
            return my_return


    def get_combinations(self, all_arguments):
        for x in self.levels[self.level]:
            to_be_excluded = []
            for v in x.path:
                to_be_excluded.append(v.name)
            yield set(all_arguments) - set(to_be_excluded)


    def show(self):
        for row in tl.RenderTree(self._root, childiter=reversed):
            print("%s%s" % (row.pre, row.node.name))

    def __get_all_nodes_for_arg(self, arg):
        for x in self.levels[self._args[arg]]:
            if x.name == arg:
                yield x