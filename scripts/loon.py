from scripts.target_cell import TargetCell
from scripts.movement_grid import MovementGrid
from scripts.satelite import Satellite
from scripts.drawer import Drawer


class Loon:
    def __init__(self, data_path):
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
        self.drawer = Drawer(self.target_cells, self.satellites, self.C, self.R, self.V)

    def _parse_data(self, filename):
        with open(filename, 'r') as file:
            lines = file.readlines()
            data = list(map(lambda x: x.strip('\n').split(), lines))
            self.R = int(data[0][0])
            self.C = int(data[0][1])
            self.A = int(data[0][2])

            self.TCells = int(data[1][0])
            self.V = int(data[1][1])
            self.B = int(data[1][2])
            self.T = int(data[1][3])

            self.start_cell_r = int(data[2][0])
            self.start_cell_c = int(data[2][1])

            for i in range(self.TCells):
                self.target_cells.append(TargetCell(self, int(data[i + 3][0]), int(data[i + 3][1])))

            for i in range(self.B):
                try:
                    self.satellites.append(Satellite(self, self.target_cells[i]))
                except IndexError:
                    self.satellites.append(Satellite(self, None))

            data = data[self.TCells + 3:]

            for i in range(self.A):
                wind = [[int(x) for x in y] for y in data[i * self.R: (i + 1)*self.R]]
                self.movement_grids.append(MovementGrid(self, wind))

    def distance(self, r, c, u, v):
        return (r  - u)**2 + (min(abs(c - v), self.C - abs(c - v)))**2

    def simulation(self):
        self.drawer.draw(self.score)
        for satellite in self.satellites:
            satellite.launch()

        for i in range(self.T):
            for satellite in self.satellites:
                satellite.next_move()
                print('\tSatellite {}, alt: {}'.format(i, (lambda x: x.altitude if x.r is not None else None)(satellite)))

            for target_cell in self.target_cells:
                self.score += int(target_cell.covered())
            input("Current step: {}\tScore -> {}".format(i, self.score))
            self.drawer.redraw(self.satellites, self.score)




