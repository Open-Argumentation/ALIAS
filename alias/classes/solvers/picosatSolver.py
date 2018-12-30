import pycosat
from collections import Counter
from operator import itemgetter

from alias.classes.solvers import BaseSolver, ExtensionType


class PicosatSolver(BaseSolver):
    def __init__(self):
        super().__init__()
        self.arguments = dict()
        self.attack_clauses = []
        self.attacks = []
        self.mapping = dict()

    def solve(self, extension: ExtensionType, args: dict, attacks: list):
        self.arguments = args
        self.attacks = attacks
        self.__get_attack_clauses()
        self.__get_mappings()
        yield self.__get_conflict_free_sets()

    def __get_clauses_for_no_attacks(self):
        my_return = []
        for k, arg in self.arguments.items():
            if not arg.is_attacking and not arg.is_attacked:
                my_return.append((arg.clause_mapping,))
        return my_return

    def __get_conflict_free_sets(self):
        self.attack_clauses.sort(key=itemgetter(0, 1), reverse=True)
        self.attacks.sort(key=itemgetter(0, 1), reverse=False)
        all_clauses = self.__get_admissible_cnf()
        all_clauses = self.__remove_duplicate_clauses(all_clauses)
        for clause in all_clauses:
            for solution in pycosat.itersolve(clause):
                mapped_sol = []
                for value in solution:
                    if value > 0:
                        mapped_sol.append(self.mapping[value])
                yield mapped_sol

    def __remove_duplicate_clauses(self, all_clauses):
        c = Counter(map(tuple, all_clauses))
        duplicates = [(k, v) for k, v in c.items() if v > 1]
        for duplicate in duplicates:
            for _ in range(duplicate[1] - 1):
                all_clauses.remove(list(duplicate[0]))
        return all_clauses

    def __get_admissible_cnf(self):
        all_clauses = []
        no_attacks = self.__get_clauses_for_no_attacks()

        def to_cnf(value):
            clauses = []
            name = self.mapping[value]
            clauses.append((value,))

            self.__get_next_defence_arg(name, clauses, [])
            # if len(self.arguments[name].attacking) == 0 and len(self.arguments[name].attacked_by) == 0:
            clauses = clauses + self.attack_clauses + no_attacks
            if len(clauses) > 0:
                all_clauses.append(clauses)

        for k in self.arguments:
            to_cnf(self.arguments[k].clause_mapping)

        return all_clauses

    def __get_next_defence_arg(self, name, clauses, pathx=[]):
        path = pathx
        if name in path:
            return
        path.append(name)
        if self.arguments[name].attacking:
            # clauses.append((self.arguments[name].clause_mapping,))
            for att in self.arguments[name].attacking:
                # if att in path:
                #     return
                path_att = path.copy()
                path_att.append(att)
                if (-self.arguments[att].clause_mapping,) not in clauses:
                    clauses.append((-self.arguments[att].clause_mapping,))
                if self.arguments[att].attacking:
                    for next_att in self.arguments[att].attacking:
                        if next_att not in path and\
                                next_att != name and next_att not in self.arguments[name].attacking and \
                                (-self.arguments[name].clause_mapping, self.arguments[next_att].clause_mapping) not in clauses and \
                                (-self.arguments[next_att].clause_mapping, self.arguments[name].clause_mapping) not in clauses:
                            t = (self.arguments[name].clause_mapping, -self.arguments[next_att].clause_mapping)
                            clauses.append(t)
                            path_def = path_att.copy()
                            path_def.append(next_att)
                            self.__get_next_defence_arg(next_att, clauses, path_def.copy())
        else:
            return

    def __get_attack_clauses(self):
        for att in self.attacks:
            attacker = att[0]
            attacked = att[1]
            if (-self.arguments[attacked].clause_mapping, -self.arguments[attacker].clause_mapping) not in self.attack_clauses:
                self.attack_clauses.append((-self.arguments[attacker].clause_mapping, -self.arguments[attacked].clause_mapping))

    def __get_mappings(self):
        for arg in self.arguments.values():
            self.mapping[arg.clause_mapping] = arg.name
        pass

