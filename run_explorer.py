import argparse
import logging
import os
from pathlib import Path

# TODO: Change to using kivy.config?
os.environ["KIVY_NO_ARGS"] = '1'
#os.environ['KIVY_NO_CONSOLELOG'] = '0'

from tonguetwister.gui.director_cast_explorer import DirectorCastExplorer
from tonguetwister.lib.logger import setup_logger


def main(base_dir, filename):
    setup_logger(logging.DEBUG)

    gui = DirectorCastExplorer(base_dir, filename)
    gui.run()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base-dir', type=str, default=str(Path.home()),
                        help='The initial directory shown in the load file dialog')
    parser.add_argument('--filepath', type=str, default=None,
                        help='A director data filename to load on startup, e.g. link/to/folder/data.cst')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    main(args.base_dir, args.filepath)
