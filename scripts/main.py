from scripts.loon import Loon


def main(path):
    ln = Loon(path)
    ln.simulation()


main('../data/loon_r70_c300_a8_radius7_saturation_250.in')