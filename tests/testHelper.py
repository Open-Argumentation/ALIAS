class TestHelper(object):

    @staticmethod
    def read_solution_from_file(file):
        return set(frozenset(line.split()) for line in open(file))

    @staticmethod
    def assert_lists_equal(expected, actual):
        equal = True
        for x in expected:
            if x not in actual:
                equal = False
        if not equal:
            error = 'Lists are not equal. Expected ' + str(expected) + ', actual: ' + str(actual) + '\n'
            if len(actual) < len(expected):
                error += 'Solution missing following items: ' + str(expected - actual)
            else:
                error += 'Solution has additional items: ' + str(actual - expected)

            error += '\nExpected has ' + str(len(expected)) + ' items, Actual has ' + str(len(actual)) + ' items.'
            raise AssertionError(error)

