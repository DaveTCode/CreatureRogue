class Location:
    def __init__(self, identifier, name: str, region):
        self.region = region
        self.identifier = identifier
        self.name = name

    def __str__(self):
        return self.name
