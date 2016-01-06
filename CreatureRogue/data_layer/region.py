class Region:
    def __init__(self, id, identifier, name):
        self.id = id
        self.identifier = identifier
        self.name = name

    def __str__(self):
        return self.name
