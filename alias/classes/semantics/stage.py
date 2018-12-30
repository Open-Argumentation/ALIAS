from alias.classes.semantics import BaseExtension


class Stage(BaseExtension):
    def __init__(self):
        super(Stage, self).__init__()
        self.__root_args = []

    def get_extension(self, args, attacks, solver):
        root_args = self.__get_root_args(args)
        # if no argument is fixed then Stage extension does not exist
        if len(root_args) == 0:
            return []

        pass

    def __get_root_args(self, args: dict):
        my_return = []
        for arg in args.values():
            if not arg.is_attacked:
                my_return.append(arg)
        return my_return
