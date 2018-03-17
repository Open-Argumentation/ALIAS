class TestHelper(object):

    @staticmethod
    def read_solution_from_file(file):
        return [set(line.split()) for line in open(file)]

    @staticmethod
    def assertListsEqual(expected, actual):
        equal = True
        for x in expected:
            if x not in actual:
                equal = False
        if not equal:
            raise AssertionError('Lists are not equal')