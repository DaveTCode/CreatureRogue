class LocationAreaRectCollection:
    """
        This exists as a separate collection so that we could speed up
        searching by location using better data structures if required.

        To facilitate this all access must be through accessor functions
        not to data directly.
    """

    def __init__(self):
        self.by_id = {}

    def add_location_area_rect(self, rect):
        """
            Adds a new location rectangle to the object, will overwrite any
            existing that uses the same location area id.
        """
        self.by_id[rect.location_area_id] = rect

    def get_location_area_by_position(self, x, y):
        """
            Given x,y map coordinates, this function returns the location
            area which covers those.

            Note, that there is currently nothing policing location area
            overlaps so this will return the first such area.

            If no location area covers these coordinates then returns None.
        """
        for location_area_id, rect in self.by_id.items():
            if rect.x2 >= x >= rect.x1 and rect.y2 >= y >= rect.y1:
                return location_area_id

        return None
