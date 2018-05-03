import time
from collections import defaultdict


class MaximalConflictFreeCollection(object):
    def __init__(self):
        self.arguments = defaultdict(set)
        self.conflict_free_sets = defaultdict(set)
        self._count = 0

    def add_arguments(self, arguments):
        """
        Adds collection of arguments to first dictionary
        :param arguments: list of arguments
        :return:
        """
        for arg in arguments:
            self.arguments[arg] = set()

    def add_attack(self, attack):
        """
        Adds an attack to create a maximal conflict free sets
        :param attack: tuple representing an attack
        :return:
        """
        print('Adding attack ' + '(' + str(attack[0]) + ', ' + str(attack[1]) + ')')
        start = time.time()
        if not self.conflict_free_sets:
            self.conflict_free_sets[self._count] = set(list(self.arguments.keys()))
            for arg in self.arguments:
                self.arguments[arg] |= set([self._count])

        attacker = attack[0]
        attacked = attack[1]

        sets_to_be_modified = self.arguments[attacker].intersection(self.arguments[attacked])
        print(str(len(sets_to_be_modified)) + ' to be modified')
        for s in sets_to_be_modified:
            """ copy the set to be modified """
            copy_of_set = self.conflict_free_sets[s].copy()

            """ remove attacked argument from the original and update it's record in arguments dictionary """
            self.conflict_free_sets[s] = set(self.conflict_free_sets[s]) - set([attacked])
            self.arguments[attacked] = set(self.arguments[attacked]) - set([s])

            """ create a new list of arguments without attacker and update affected arguments records """
            self._count += 1
            new_set = copy_of_set - set([attacker])
            self.conflict_free_sets[self._count] = new_set
            for arg in new_set:
                self.arguments[arg].add(self._count)
        end = time.time()
        print('Attack added in ' + str(end - start) + ' seconds')

    def get_conflict_free_sets(self):
        for k, v in self.conflict_free_sets.items():
            yield v
