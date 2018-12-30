from abc import ABC, abstractmethod
from alias.classes.solvers.extensionType import ExtensionType


class BaseSolver(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def solve(self, extension: ExtensionType, args: dict, attacks: list):
        pass
