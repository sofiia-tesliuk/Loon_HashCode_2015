from scripts.target_cell import TargetCell
from scripts.movement_grid import MovementGrid
from scripts.satelite import Satellite
from scripts.drawer import Drawer
from tqdm import tqdm
import random


class Loon:
    def __init__(self, data_path, visualise):
        self.visualise = visualise
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
        print("Parsing data.")
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

            random.shuffle(self.target_cells)

            for i in range(self.B):
                try:
                    self.satellites.append(Satellite(self, self.target_cells[i]))
                except IndexError:
                    self.satellites.append(Satellite(self, None))

            data = data[self.TCells + 3:]

            for i in range(self.A):
                wind = [[int(x) for x in y] for y in data[i * self.R: (i + 1)*self.R]]
                wind = [[(row[i*2], row[i*2 + 1]) for i in range(len(row) // 2)] for row in wind]
                self.movement_grids.append(MovementGrid(self, wind))

    def distance(self, r, c, u, v):
        return (r  - u)**2 + (min(abs(c - v), self.C - abs(c - v)))**2

    def update_score(self):
        for target_cell in self.target_cells:
            self.score += int(target_cell.covered())

    def simulation(self):
        print("Simulation.")
        for satellite in self.satellites:
            satellite.launch()
        self.update_score()
        if self.visualise:
            self.drawer.draw(self.score)
            input("Current step: 0\tScore -> {}".format(self.score))

        with open('../data/output/out.out', 'w') as file:
            for i in tqdm(range(self.T)):
                for j, satellite in enumerate(self.satellites):
                    moved = satellite.next_move()
                    file.write("{} ".format(moved))
                file.write("\n")

                self.update_score()
                if self.visualise:
                    try:
                        if i % 25 == 0:
                            self.drawer.redraw(self.satellites, self.score)
                            input("\nCurrent step: {}\tScore -> {}".format(i, self.score))
                    except ZeroDivisionError:
                        pass

            if self.visualise:
                self.drawer.redraw(self.satellites, self.score)

        satellites_in_simulation = sum([satellite.in_simulation() for satellite in self.satellites])
        print("\nFinal score: {}, which corresponds to {} % coverage.\n"
              "Satellites in simulation: {}, from {}, which correspond to {}%."
              .format(self.score, round(self.score/self.T/len(self.target_cells)*100, 2), satellites_in_simulation,
                      len(self.satellites), round(satellites_in_simulation/len(self.satellites)*100, 2)))
