import argparse

from tonguetwister.gui.director_cast_explorer import DirectorCastExplorer
from tonguetwister.parser import RifxParser


def main(filepath):
    # Unpack a cst file
    parser = RifxParser(silent=True)
    parser.load_file(filepath)
    parser.unpack()

    # Run the GUI
    gui = DirectorCastExplorer(parser)
    gui.run()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('filepath', type=str, help='A director data file path, e.g. link/to/folder/data.cst')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    main(args.filepath)
