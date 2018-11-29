from scripts.loon import Loon


def main(path):
    ln = Loon(path)
    ln.simulation()


main('../data/example.txt')