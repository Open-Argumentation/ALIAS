from abc import ABC, abstractmethod

from alias.classes.matrix import Matrix


class BaseExtension(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def verify_solution(self, solution: list, arguments: dict, matrix: Matrix):
        pass
