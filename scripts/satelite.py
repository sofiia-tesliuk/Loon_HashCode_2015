class Satellite:
    def __init__(self, loon, v):
        self.loon = loon
        self.r = loon.start_cell_r
        self.c = loon.start_cell_c
        self.altitude = 0

    def launched(self):
        return self.altitude > 0

    def in_simulation(self):
        return (self.c is not None) and self.launched()
