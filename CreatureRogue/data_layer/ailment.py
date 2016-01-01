class Ailment:
    """
    An ailment can be applied to a creature.

    TODO: Very little by way of implementation here at the moment, just enough to store the information
    """

    def __init__(self, ailment_id: int, name: str):
        self.ailment_id = ailment_id
        self.name = name

    def __str__(self):
        return self.name
