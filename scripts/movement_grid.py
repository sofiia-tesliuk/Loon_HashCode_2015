class MovementGrid:
    def __init__(self, loon, wind):
        self.loon = loon
        # [0] -- a, [1] -- b
        self.wind = wind

    def _a(self, r, c):
        try:
            return self.wind[r][c][0]
        except IndexError:
            pass

    def _b(self, r, c):
        try:
            return self.wind[c][r][1]
        except IndexError:
            pass

    def next_position(self, r, c):
        if 0 <= r + self._a(r, c) <= self.loon.R:
            return r + self._a(r, c), (c + self._b(r, c)) % self.loon.C
        return None, None