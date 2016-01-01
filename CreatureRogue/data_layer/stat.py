class Stat:
    def __init__(self, name, short_name):
        self.name = name
        self.short_name = short_name

    def __str__(self):
        return self.name