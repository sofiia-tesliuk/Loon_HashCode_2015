class TargetCell:
    def __init__(self, loon,  r, c):
        self.loon = loon
        self.r = r
        self.c = c

    def covered(self, satellites):
        for satellite in satellites:
            if satellite.in_simulation():
                return self.loon.distance(satellite.r, satellite.c, self.r, self.c) <= self.loon.V**2
        return False