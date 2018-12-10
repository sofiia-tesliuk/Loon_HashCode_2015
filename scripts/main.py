from scripts.loon import Loon


def main(path):
    ln = Loon(path, False)
    ln.simulation()



main('../data/input/loon_r70_c300_a8_radius7_saturation_250.in')
#main('../data/input/example.in')
#main('../data/input/own_example.in')

