# noinspection PyUnresolvedReferences
from tonguetwister.decompiler.data.operators import *
from tonguetwister.decompiler.data.opcode import OPCode
from tonguetwister.lib.stream import ByteBlockIO


def detokenize(bytecode):
    operators = []
    stream = ByteBlockIO(bytecode)
    while not stream.is_depleted():
        addr = stream.tell()

        # Find class for the current byte
        opcode = OPCode(addr, stream.uint8())
        cls = globals()[opcode.class_name]

        args = pop_args(stream, opcode)

        # Instantiate operator
        operators.append(cls(opcode, *args))

    return operators


def pop_args(stream, opcode):
    args = []
    if opcode.is_single_byte_instruction():
        pass
    elif opcode.is_two_byte_instruction():
        args.append(stream.uint8())
    elif opcode.is_three_byte_instruction():
        args.append(stream.uint8())
        args.append(stream.uint8())

    return args
