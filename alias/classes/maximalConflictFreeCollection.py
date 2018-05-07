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

    def add_attack1(self, attack):
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
            new_set_without_attacked = set(self.conflict_free_sets[s]) - set([attacked])
            if new_set_without_attacked not in self.conflict_free_sets.values():
                self.conflict_free_sets[s] = new_set_without_attacked
                self.arguments[attacked] = set(self.arguments[attacked]) - set([s])
            else:
                self.conflict_free_sets.pop(s)
                for arg in self.conflict_free_sets[s]:
                    self.arguments[arg] = set(self.arguments[attacked]) - set([s])

            """ create a new list of arguments without attacker and update affected arguments records """
            new_set_without_attacker = copy_of_set - set([attacker])
            if new_set_without_attacker not in self.conflict_free_sets.values():
                self._count += 1
                self.conflict_free_sets[self._count] = new_set_without_attacker
                for arg in new_set_without_attacker:
                    self.arguments[arg].add(self._count)

        end = time.time()
        print('Attack added in ' + str(end - start) + ' seconds')

    def add_argument_and_attacks1(self, argument, attacking):
        attacker = argument
        attacked = attacking

        if attacked:
            # if there are no conflict free sets created yet, just create two of them and add the attack
            if not self.conflict_free_sets:
                self.conflict_free_sets[self._count].add(attacker)
                self.arguments[attacker].add(self._count)
                self._count += 1

                self.conflict_free_sets[self._count] |= set(attacked)
                for v in attacked:
                    self.arguments[v].add(self._count)
                self._count += 1

            else:
                attacker_affected_sets = set(range(self._count)) - self.arguments[attacker]
                att = set()
                for v in attacked:
                    att |= self.arguments[v]
                attacked_affected_sets = set(range(self._count)) - att
                to_be_modified = attacker_affected_sets.intersection(attacked_affected_sets)
                for s in to_be_modified:
                    copy_of_set = self.conflict_free_sets[s].copy()
                    self.conflict_free_sets[s].add(attacker)
                    self.arguments[attacker].add(s)

                    self.conflict_free_sets[self._count] = copy_of_set.union(set(attacked))
                    for v in attacked:
                        self.arguments[v].add(self._count)

                    self._count += 1


    def add_argument_and_attacks(self, argument, attacking):
        print('Adding argument ' + str(argument) + ' and it\'s attacks ' + str(attacking))
        start = time.time()
        if not self.conflict_free_sets:
            self.conflict_free_sets[self._count] = set(list(self.arguments.keys()))
            for arg in self.arguments:
                self.arguments[arg] |= set([self._count])

        if set(argument).issubset(set(attacking)):
            for v in self.arguments[argument]:
                self.conflict_free_sets[v] = self.conflict_free_sets[v] - set([argument])
            self.arguments[argument] = set()

        if attacking:
            for conflict_free_set in self.arguments[argument].copy():
                copy_of_set = self.conflict_free_sets[conflict_free_set].copy()
                elements_affected = copy_of_set.intersection(attacking)
                if elements_affected:
                    new_set_without_attacking = copy_of_set - elements_affected
                    if new_set_without_attacking not in self.conflict_free_sets.values():
                        self.conflict_free_sets[conflict_free_set] = new_set_without_attacking
                        for arg in elements_affected:
                            self.arguments[arg] = self.arguments[arg] - set([conflict_free_set])
                    else:
                        self.conflict_free_sets.pop(conflict_free_set)
                        for arg in copy_of_set:
                            self.arguments[arg] = self.arguments[arg] - set([conflict_free_set])

                    new_set_without_argument = copy_of_set - set([argument])
                    if new_set_without_argument not in self.conflict_free_sets.values():
                        self._count += 1
                        self.conflict_free_sets[self._count] = new_set_without_argument
                        for v in new_set_without_argument:
                            self.arguments[v].add(self._count)

        end = time.time()
        print('Argument added in ' + str(end - start) + ' seconds')
        print('length of conflict free sets is ' + str(len(self.conflict_free_sets)))


    def get_conflict_free_sets(self):
        for k, v in self.conflict_free_sets.items():
            yield v
