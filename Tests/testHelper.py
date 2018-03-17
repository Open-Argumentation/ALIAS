class TestHelper(object):

    @staticmethod
    def read_solution_from_file(file):
        return [set(line.split()) for line in open(file)]
