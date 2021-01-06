# TongueTwister

A file disassembler for programs created in Macromedia Director. It is also a decompiler for Lingo bytecode, the script
language used in Director. Finally, it is also an attempt to document the data format used by Director.

The project is initially targeting Macromedia Director version 6.5.

**The project is still in development**

# Format documentation

The documentation for the Director 6.5 file formats can be found
at [./docs/format-spec/readme.md](./docs/format-spec/readme.md).

# Setup

The project is written in **python 3.8**. It is recommended to use a virtual environment when running the project
locally.

Begin by installing/updating the following pip-packages:

    pip install -U pip setuptools pip-tools

Then run

    pip-sync requirements.txt

to install all dependencies.

# Usage

This package can be used in two ways:

1. Run the GUI program and explore director files visually. Run

        python run_explorer.py

   with the optional arguments
    <dl>
      <dt>--filepath path/to/file.dir</dt>
      <dd>Specify a file to preload</dd>
      <dt>--basedir path/to/basedir/</dt>
      <dd>Specify the default directory to show when opening the file explorer inside the program.</dd>
    </dl>

2. Use the library from python directly:

        from tonguetwister.disassembler.file_disassembler import FileDisassembler

        file_disassembler = FileDisassembler()
        file_disassembler.load_file(filename)
        file_disassembler.unpack()

**"Legacy"**

Previously you could only unpack lingo scripts, thus the following script currently exist for legacy reasons.

To see the decompilation of a single script, run:

    python example.py <link/to/folder/data.cst> <script_number> <function_number>

Initially try with `script_number = 0` and `function_number = 0` and experiment from there.

# Related projects, inspiriation and data sources

See this [link](./docs/format-spec/readme.md#sources) inside the format specification.

# License

[MIT License](./LICENSE)
