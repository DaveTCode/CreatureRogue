class LocationAreaRect:
    def __init__(self, location_area_id, x1, y1, x2, y2):
        self.location_area_id = location_area_id
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def __str__(self):
        return "{0} - ({1},{2}),({3},{4})".format(self.location_area_id, self.x1, self.y1, self.x2, self.y2)