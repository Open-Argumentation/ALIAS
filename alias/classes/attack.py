class Attack(object):

    def __init__(self, attacker, attacked):
        self.attacker = attacker
        self.attacked = attacked

    def get_set(self):
        return set([self.attacker, self.attacked])
