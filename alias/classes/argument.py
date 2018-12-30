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

    def is_attacked(self):
        return len(self.attacked_by) > 0

    def is_attacking(self):
        return len(self.attacking) > 0
