class Argument(object):

    def __init__(self, name, mapping=0, clause_mapping=0):
        self.name = name
        self.attacking = []
        self.attacked_by = []
        self.mapping = mapping
        self.clause_mapping = clause_mapping

    def add_attack(self, attacked):
        self.attacking.append(attacked)

    def add_attacker(self, attacker):
        self.attacked_by.append(attacker)

