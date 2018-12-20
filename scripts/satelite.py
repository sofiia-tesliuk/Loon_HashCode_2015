import random


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

    def possible_distance_to_target(self, alt, current_r, current_c):
        possible_move = self.loon.movement_grids[alt - 1].next_position(current_r, current_c)
        if possible_move[0] is not None:
            return self.loon.distance(possible_move[0], possible_move[1],
                                      self.target_cell.r, self.target_cell.c)
        return float('inf')

    def next_move(self):
        if self.in_simulation():
            i_next = self._random_till_reaching_target_cell()
            self.altitude += i_next
            next_move = self.loon.movement_grids[self.altitude - 1].next_position(self.r, self.c)
            self.r = next_move[0]
            self.c = next_move[1]
            return i_next
        return 0

    def _random_till_reaching_target_cell(self):
        """
        Algorithm #4
        """
        if self.cover_target_cell(self.target_cell):
            i_next = self._best_current_choice()
        else:
            i_next = self._random_move()
        return i_next

    def _random_move(self):
        """
        Algorithm #3
        """
        possible_moves = []
        if self.altitude > 1:
            possible_moves.append(-1)
        if self.altitude < self.loon.A:
            possible_moves.append(1)
        return random.choice(possible_moves)

    def _best_current_choice(self):
        """
        Algorithm #1
        """
        min_d = self.possible_distance_to_target(self.altitude, self.r, self.c)
        i_min = 0
        if self.altitude > 1:
            if self.possible_distance_to_target(self.altitude - 1, self.r, self.c) < min_d:
                min_d = self.possible_distance_to_target(self.altitude - 1, self.r, self.c)
                i_min = -1
        if self.altitude < self.loon.A:
            if self.possible_distance_to_target(self.altitude + 1, self.r, self.c) < min_d:
                i_min = 1
        return i_min

    def _best_deep_move(self, deep_of_move):
        """
        Algorithm #2
        """
        def _best_next_move(current_altitude, current_r, current_c, current_depth):
            if current_depth == 1:
                min_d = self.possible_distance_to_target(current_altitude, current_r, current_c)
                i_min = 0
                if current_altitude > 1:
                    if self.possible_distance_to_target(current_altitude - 1, current_r, current_c) < min_d:
                        min_d = self.possible_distance_to_target(current_altitude - 1, current_r, current_c)
                        i_min = -1
                if current_altitude < self.loon.A:
                    if self.possible_distance_to_target(current_altitude + 1, current_r, current_c) < min_d:
                        i_min = 1
                return i_min, min_d
            else:
                next_r, next_c = self.loon.movement_grids[current_altitude - 1].next_position(current_r, current_c)
                i_0, d_0 = _best_next_move(current_altitude, next_r, next_c, current_depth - 1)
                if current_altitude > 1:
                    next_r, next_c = self.loon.movement_grids[current_altitude - 2].next_position(current_r, current_c)
                    i_1, d_1 = _best_next_move(current_altitude - 1, next_r, next_c, current_depth - 1)
                    if d_1 < d_0:
                        i_0 = i_1
                        d_0 = d_1
                if current_altitude < self.loon.A:
                    next_r, next_c = self.loon.movement_grids[current_altitude].next_position(current_r, current_c)
                    i_1, d_1 = _best_next_move(current_altitude + 1, next_r, next_c, current_depth - 1)
                    if d_1 < d_0:
                        i_0 = i_1
                        d_0 = d_1
                return i_0, d_0

        i, d = _best_next_move(self.altitude, self.r, self.c, deep_of_move)
        return i
