import argparse
from tonguetwister.parser import RifxParser
from tonguetwister.lingo_decompiler import Decompiler


def main(filepath, script_number, function_number):
    # Unpack a cst file.
    data = RifxParser(filepath)
    data.unpack()

    # Extract a specific lingo script
    script = data.lingo_scripts.items()[script_number][1]
    namelist = data.namelist
    function = script.functions[function_number]

    # Decompile the lingo script
    Decompiler().to_pseudo_code(function, namelist, script)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('filepath', type=str, help='A director data file path, e.g. link/to/folder/data.cst')
    parser.add_argument('script_number', metavar='script-number', type=int, help='The script number to decompile')
    parser.add_argument('function_number', metavar='function-number', type=int, help='The function number to decompile')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    main(args.filepath, args.script_number, args.function_number)
