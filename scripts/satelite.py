class Satellite:
    def __init__(self, loon, target_cell):
        self.loon = loon
        self.r = loon.start_cell_r
        self.c = loon.start_cell_c
        self.altitude = 0
        self.target_cell = target_cell

    def launch(self):
        if self.target_cell is not None:
            self.altitude = 1

    def launched(self):
        return self.altitude > 0

    def in_simulation(self):
        return (self.c is not None) and self.launched()

    def cover_target_cell(self, target_cell):
        if self.in_simulation():
            return self.loon.distance(self.r, self.c, target_cell.r, target_cell.c) <= self.loon.V**2
        return False

    def possible_distance_to_target(self, alt):
        possible_move = self.loon.movement_grids[alt - 1].next_position(self.r, self.c)
        if possible_move[0] is not None:
            return self.loon.distance(possible_move[0], possible_move[1],
                                      self.target_cell.r, self.target_cell.c)
        return float('inf')

    def next_move(self):
        if self.in_simulation():
            min_d = self.possible_distance_to_target(self.altitude)
            i_min = 0
            if self.altitude > 1:
                if self.possible_distance_to_target(self.altitude - 1) < min_d:
                    min_d = self.possible_distance_to_target(self.altitude - 1)
                    i_min = -1
            if self.altitude < self.loon.A:
                if self.possible_distance_to_target(self.altitude + 1) < min_d:
                    i_min = 1

            self.altitude += i_min
            next_move = self.loon.movement_grids[self.altitude - 1].next_position(self.r, self.c)
            self.r = next_move[0]
            self.c = next_move[1]
            return i_min
        return 0


