class Node(object):
    def __init__(self, name='root', level=0):
        self.name = name
        self.children = []
        self.level = level