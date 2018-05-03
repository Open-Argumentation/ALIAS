import time

from tables import *

class ArgumentTable(IsDescription):
    id = Int64Col()
    name = StringCol(16)

class ConflictFreeTable(IsDescription):
    id = Int64Col()

class ArgumentConflictFreeBridgeTable(IsDescription):
    argId = Int64Col()
    conflictFreeId = Int64Col()
    active = BoolCol()

class Store(object):
    def __init__(self):
        self._h5file = open_file('alias.h5', mode='w', title='Alias')
        self._group = self._h5file.create_group('/', 'detector', 'info')
        self._arg_table = self._h5file.create_table(self._group, 'args', ArgumentTable, 'Arguments')
        self._conflict_free_table = self._h5file.create_table(self._group, 'conflictFree', ConflictFreeTable, 'Conflict Free Sets')
        self._argument_conflict_free_table = self._h5file.create_table(self._group, 'readout', ArgumentConflictFreeBridgeTable, 'Bridge Table')
        self._lists_count = 0
        self._attack_count = 0

    def add_argument(self, arg):
        """
        Adds argument to the h5file store
        :param arg: argument object
        :return:
        """
        argument_table = self._arg_table.row
        argument_table['id'] = arg.mapping
        argument_table['name'] = arg.name
        argument_table.append()
        self._arg_table.flush()

    def setup_conflict_free_sets(self):
        conflict_free_table = self._conflict_free_table.row
        conflict_free_table['id'] = 0
        conflict_free_table.append()
        self._conflict_free_table.flush()
        for arg in self._arg_table:
            bridge_table = self._argument_conflict_free_table.row
            bridge_table['argId'] = arg['id']
            bridge_table['conflictFreeId'] = 0
            bridge_table['active'] = 1
            bridge_table.append()
        self._lists_count += 1
        self._argument_conflict_free_table.flush()

    def add_attack(self, attack):
        self._attack_count += 1
        # print(self._attack_count)
        # get ids of arguments from the attack
        start = time.time()
        condition1 = "name == b'" + attack[0] + "'"
        condition2 = "name == b'" + attack[1] + "'"
        arg1 = [x['id'] for x in self._arg_table.where(condition1)][0]
        arg2 = [x['id'] for x in self._arg_table.where(condition2)][0]
        end = time.time()
        # print('args ids fetched in '+ str(end - start))

        # get lists that have those arguments
        start = time.time()
        condition1 = "argId == " + str(arg1)
        condition2 = "argId == " + str(arg2)
        arg1lists = [x['conflictFreeId'] for x in self._argument_conflict_free_table.where(condition1) if x['active'] == 1]
        arg2lists = [x['conflictFreeId'] for x in self._argument_conflict_free_table.where(condition2) if x['active'] == 1]
        end = time.time()
        # print('lists with those arguments fetched in ' + str(end - start))

        #get lists that have both of the arguments
        start = time.time()
        to_be_updated_lists = list(set(arg1lists).intersection(set(arg2lists)))
        end = time.time()
        # print('filtere lists in ' + str(end - start))

        start = time.time()
        # iterate through lists to be updated
        for v in to_be_updated_lists:
            # create new set of arguments without the attacker
            condition = "conflictFreeId == " + str(v)
            args = [x['argId'] for x in self._argument_conflict_free_table.where(condition)]
            self._lists_count += 1
            x = time.time()
            for arg in args:
                if arg != arg1:
                    bridge_table = self._argument_conflict_free_table.row
                    bridge_table['argId'] = arg
                    bridge_table['conflictFreeId'] = self._lists_count
                    bridge_table['active'] = 1
                    bridge_table.append()

            y = time.time()
            # print('args grabbed in ' + str(y - x))
            # remove attacked argument from the original list
            condition = "(argId == " + str(arg2) + ") & (conflictFreeId == " + str(v) + ")"
            for row in self._argument_conflict_free_table.where(condition):
                row['active'] = 0
                row.update()

        end = time.time()
        # print(str(len(to_be_updated_lists)) + ' lists updated in ' + str(end - start))
        # print(str(len(to_be_updated_lists)) + ' for total of ' + str(self._lists_count))

        self._argument_conflict_free_table.flush()

    def get_conflict_free_args(self):
        for x in range(self._lists_count):
            args = [x['argId'] for x in self._argument_conflict_free_table.where("(conflictFreeId == " + str(x) + ") & active == 1 ")]
            my_return = []
            for arg in args:
                my_return.append([x['name'] for x in self._arg_table.where("id == " + str(arg))][0].decode('utf-8'))
            yield my_return
