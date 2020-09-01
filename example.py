"""
Example useage of the TongueTwister module.

Call with:
  python example.py <link/to/folder/data.cst> <script_number_to_decompile> <function_number_to_decompile>
"""
import sys
from tonguetwister.parser import RifxParser
from tonguetwister.lingo_decompiler import Decompiler

def main(filename, script_number, function_number):
  # Unpack a cst file.
  data = RifxParser(filename)
  data.unpack()

  # Extract a specific lingo script
  script = data.lingo_scripts.items()[script_number][1]
  namelist = data.namelist
  function = script.functions[function_number]

  # Decompile the lingo script
  Decompiler().twist_to_pseudo(function, namelist, script)

if __name__ == '__main__':
  filename = sys.argv[1]
  script_number = int(sys.argv[2])
  function_number = int(sys.argv[3])

  main(filename, script_number, function_number)
