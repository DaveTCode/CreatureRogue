class Region:
    def __init__(self, region_id, identifier, name: str):
        self.id = region_id
        self.identifier = identifier
        self.name = name

    def __str__(self):
        return self.name
