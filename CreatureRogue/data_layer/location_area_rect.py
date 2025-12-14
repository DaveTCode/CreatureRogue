class LocationAreaRect:
    def __init__(self, location_area_id: int, x1: int, y1: int, x2: int, y2: int):
        self.location_area_id = location_area_id
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def __str__(self):
        return f"{self.location_area_id} - ({self.x1},{self.y1}),({self.x2},{self.y2})"
