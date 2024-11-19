import argparse
import csv
import os

from a_mst import A_MST

CWD = os.getcwd()


def write(source, values, append=False):
    mode = "a" if append else "w"
    with open(source, mode, newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow([x for x in values])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source")
    args = parser.parse_args()

    paths = []

    path = os.path.join(CWD, args.source)
    if os.path.isfile(path):
        _, ext = os.path.splitext(path)
        assert ext.lower() == ".txt"

        paths.append(path)

    else:
        for directory, _, names in os.walk(os.path.join(CWD, args.source)):
            for name in names:
                _, ext = os.path.splitext(name)
                if ext.lower() == ".txt":
                    paths.append(os.path.join(directory, name))

    headers = ["cost", "nodes", "cpu", "real"]

    write("A_MST.csv", headers)

    for path in paths:
        with open(path, "r") as source:
            N = int(source.readline())
            A = [[float(x) for x in source.readline().split(" ")] for _ in range(N)]

            cpu, real, nodes, cost = A_MST(N, A)
            write("A_MST.csv", [cost, nodes, cpu, real], append=True)


if __name__ == "__main__":
    main()
