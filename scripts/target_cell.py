class TargetCell:
    def __init__(self, loon,  r, c):
        self.loon = loon
        self.r = r
        self.c = c

    def covered(self):
        for satellite in self.loon.satellites:
            if satellite.cover_target_cell(self):
                return True
        return False