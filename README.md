# TongueTwister
A file disassembler for programs created in Macromedia Director. It is also a decompiler for Lingo bytecode, the script
language used in Director. Finally it is also an attempt to document the data format used by Director.

The project is initially targeting Macromedia Director version 6.5.

# Current state of the project
The development is somewhat inactive at the moment. The current focus is to improve the Lingo parser, as well as writing
a gui for development.



# Usage
To see the decompilation of a single script, run:

    python example.py <link/to/folder/data.cst> <script_number> <function_number>

Initially try with `script_number = 0` and `function_number = 0` and experiment from there.

# Technologies
Written in python 3.

# License
[MIT License](./LICENSE)
