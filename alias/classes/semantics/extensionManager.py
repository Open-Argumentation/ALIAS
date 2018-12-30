from alias.classes.solvers import ExtensionType
from alias.classes.semantics.complete import Complete
from alias.classes.semantics.preferred import Preferred
from alias.classes.semantics.stable import Stable


class ExtensionManager(object):
    def __init__(self):
        self.extensions = {
            ExtensionType.COMPLETE: Complete(),
            ExtensionType.PREFERRED: Preferred(),
            ExtensionType.STABLE: Stable(),
        }
