class Color:
    def __init__(self, name, r, g, b):
        self.name = name
        self.r = r
        self.g = g
        self.b = b

    def __str__(self):
        return "{0} - ({1},{2},{3})".format(self.name, self.r, self.g, self.b)
