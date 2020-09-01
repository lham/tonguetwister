from ..lib.byte_block_io import ByteBlockIO
from data.opcode import OPCode
from data.operators import *

def detokenize(bytecode):
  operators = []
  stream = ByteBlockIO(bytecode)
  while not stream.is_depleted():
    addr = stream.tell()

    # Find class for the current byte
    opcode = OPCode(addr, stream.uint8())
    klass = globals()[opcode.class_name]

    args = []
    if opcode.value < 0x40:  # single-byte instruction
      pass
    elif opcode.value < 0x80:  # two-byte instruction
      args.append(stream.uint8())
    else:  # three-byte instruction
      args.append(stream.uint8())
      args.append(stream.uint8())

    # Instanciate operator
    operators.append(klass(opcode, *args))
    print operators[-1].raw_detokenize_string()

  return operators


