from alias.classes import Argument, Attack, Matrix


class Framework(object):
    def __init__(self, counter):
        self.arguments = {}
        self.attacks = []
        self.counter = counter
        self._matrix = None

    @property
    def matrix(self):
        if self._matrix is None:
            self._matrix = Matrix(self.arguments, self.attacks)
        return self._matrix

    def add_argument(self, argument):
        """
        Method to add argument to argumentation framework
        :param argument: Name of the argument to be added
        :return:
        """
        if argument not in self.arguments:
            self.arguments[argument] = Argument(argument, len(self.arguments))

    def add_attack(self, attacker, attacked):
        """
        Method to add attack to argumentation framework
        :param attacker: argument that attacks 'attacked'
        :param attacked: argument attacked by 'attacker'
        :return:
        """
        attacker = self.arguments.get(attacker)
        attacked = self.arguments.get(attacked)
        if attacker.name not in self.arguments:
            self.add_argument(attacker)
        if attacked.name not in self.arguments:
            self.add_argument(attacked)
        attack = Attack(attacker.name, attacked.name)
        self.attacks.append((attacker.name, attacked.name))
        self.arguments.get(attacker.name).add_attack(attacked.name)
        self.arguments.get(attacked.name).add_attacker(attacker.name)

    def merge_framework(self, framework):
        """
        Method to merge two frameworks
        :param framework: framework to be merged
        :return:
        """
        self.arguments = {**framework.arguments}
        self.attacks = self.attacks + framework.attacks
        self.__remap_arguments()

    def __remap_arguments(self):
        counter = 0
        for a in self.arguments.values():
            a.mapping = counter
            counter += 1

    def merge_framework_through_attack(self, framework, attacker, attacked):
        """
        Method to merge two frameworks through attack
        :param framework: framework to be merged
        :param attacker: attacker from the attack
        :param attacked: attacked argument from the attack
        :return:
        """
        self.arguments = {**self.arguments, **framework.arguments}
        self.__remap_arguments()
        self.attacks = self.attacks + framework.attacks
        self.attacks.append(tuple([attacker, attacked]))

    def get_argument_from_mapping(self, mapping):
        for v in self.arguments:
            if self.arguments[v].mapping == mapping:
                return self.arguments[v].name
        return None


