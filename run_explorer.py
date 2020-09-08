import argparse

from tonguetwister.gui.director_cast_explorer import DirectorCastExplorer
from tonguetwister.file_disassembler import FileDisassembler


def main(filepath):
    # Unpack a cst file
    file_disassembler = FileDisassembler(silent=True)
    file_disassembler.load_file(filepath)
    file_disassembler.unpack()

    # Run the GUI
    gui = DirectorCastExplorer(file_disassembler)
    gui.run()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('filepath', type=str, help='A director data file path, e.g. link/to/folder/data.cst')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    main(args.filepath)
