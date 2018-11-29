from scripts.target_cell import TargetCell
from scripts.movement_grid import MovementGrid
from scripts.satelite import Satellite


class Loon:
    def __init__(self, t, data_path):
        self.score = 0
        self.satellites = []
        self.target_cells = []
        self.movement_grids = []
        self.T = None
        self.R = None
        self.C = None
        self.A = None
        self.TCells = None
        self.V = None
        self.B = None
        self.start_cell_r = None
        self.start_cell_c = None
        self._parse_data(data_path)

    def _parse_data(self, filename):
        with open(filename, 'r') as file:
            lines = file.readlines()
            data = list(map(lambda x: x.strip('\n').split(), lines))
            self.R = data[0][0]
            self.C = data[0][1]
            self.A = data[0][2]

            self.TCells = data[1][0]
            self.V = data[1][1]
            self.B = data[1][2]
            self.T = data[1][3]

            self.start_cell_r = data[2][0]
            self.start_cell_c = data[2][1]

            for i in range(self.B):
                self.satellites.append(Satellite(self.V, self.start_cell_r, self.start_cell_c))

            for i in range(self.TCells):
                self.target_cells.append(TargetCell(data[i + 3][0], data[i + 3][1]))

            data = data[self.TCells + 3:]

            for i in range(self.A):
                self.movement_grids.append(MovementGrid(self.R, self.C, data[i * self.R: (i + 1)*self.R]))



