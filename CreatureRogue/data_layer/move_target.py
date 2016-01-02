class MoveTarget:
    def __init__(self, identifier: str, name: str, description: str):
        self.identifier = identifier
        self.name = name
        self.description = description

    def __str__(self):
        return self.name