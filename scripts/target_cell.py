class TargetCell:
    def __init__(self, loon,  r, c):
        self.loon = loon
        self.r = r
        self.c = c

    def covered(self, satellites):
        for satellite in satellites:
            if satellite.in_simulation():
                return ((satellite.r  - self.r)**2 +
                 (min(abs(satellite.c - self.c), self.loon.C - abs(satellite.c - self.c)))**2) <= self.loon.V**2
        return False