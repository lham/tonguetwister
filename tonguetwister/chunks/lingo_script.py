from collections import Sized, Sequence, OrderedDict
from ..lib.helper import grouper

class LingoScript(object):

  def __init__(self, stream):
    stream.set_big_endian()
    self.__parse_chunk_header(stream)
    self.__parse_properties(stream)
    self.__parse_globals(stream)
    self.__parse_functions(stream)
    self.__parse_literals(stream)
    self.__parse_u9(stream)

  @property
  def header(self):
    return self._chunk_header

  @property
  def properties(self):
    return self._properties

  @property
  def globals(self):
    return self._globals
 
  @property
  def functions(self):
    return self._functions
  
  @property
  def literals(self):
    return self._literals

  @property
  def u9(self):
    return self._u9
   
  def __parse_chunk_header(self, stream):
    self._chunk_header = OrderedDict()
    self._chunk_header['u1']                   = stream.uint32()
    self._chunk_header['u2']                   = stream.uint32()
    self._chunk_header['chunk_length']         = stream.uint32()
    self._chunk_header['chunk_length_2']       = stream.uint32()
    self._chunk_header['chunk_header_length']  = stream.uint16()
    self._chunk_header['script_id']            = stream.uint16()
    self._chunk_header['u3']                   = stream.uint16()

    self._chunk_header['u4']                   = stream.uint32()
    self._chunk_header['u5']                   = stream.uint32()
    self._chunk_header['u6']                   = stream.uint32()
    self._chunk_header['u7']                   = stream.uint32()
    self._chunk_header['u8']                   = stream.uint32()
    self._chunk_header['u10']                  = stream.uint32()
    self._chunk_header['cast_member_assoc_id'] = stream.uint16()
    self._chunk_header['u11']                  = stream.uint16()

    self._chunk_header['n_u9']                 = stream.uint16()
    self._chunk_header['u9_offset']            = stream.uint32()

    self._chunk_header['u12']                  = stream.uint32()

    self._chunk_header['n_properties']             = stream.uint16()
    self._chunk_header['properties_offset']        = stream.uint32()
    self._chunk_header['n_globals']                = stream.uint16()
    self._chunk_header['globals_offset']           = stream.uint32()
    self._chunk_header['n_functions']              = stream.uint16()
    self._chunk_header['function_headers_offset']  = stream.uint32()
    self._chunk_header['n_literals']               = stream.uint16()
    self._chunk_header['literal_headers_offset']   = stream.uint32()
    
    self._chunk_header['literals_body_length']     = stream.uint32()
    self._chunk_header['literals_body_offset']     = stream.uint32()

  def __parse_properties(self, stream):
    stream.seek(self.header['properties_offset'], 0)

    self._properties = [None] * self.header['n_properties']
    for i, _ in enumerate(self._properties):
      self._properties[i] = stream.uint16()
  
  def __parse_globals(self, stream):
    stream.seek(self.header['globals_offset'], 0)

    self._globals = [None] * self.header['n_globals']
    for i, _ in enumerate(self._globals):
      self._globals[i] = stream.uint16()
      
  def __parse_functions(self, stream):
    self._functions = LingoFunctions(
        stream,
        self.header['function_headers_offset'],
        self.header['n_functions'])

  def __parse_literals(self, stream):
    self._literals = LingoFunctionLiterals(
        stream, 
        self.header['literal_headers_offset'],
        self.header['literals_body_offset'],
        self.header['n_literals'])

  def __parse_u9(self, stream):
    stream.seek(self.header['u9_offset'], 0)

    self._u9 = [None] * self.header['n_u9']
    for i, _ in enumerate(self._u9):
      self._u9[i] = stream.uint16()
    

  def __repr__(self):
    unknown_h = (
        self.header['u1'], self.header['u2'], self.header['u3'], self.header['u4'], 
        self.header['u5'], self.header['u6'], self.header['u7'], self.header['u8'], 
        self.header['u10'], self.header['u11'], self.header['u12'])

    msg = ''
    #msg += '    Unk_Headers: [' + ', '.join('%d' % (v) for v in unknown_h) + ']\n' 
    msg += '    Headers: [' + ', '.join('%s: %d' % (k, v) for k, v in self.header.iteritems()) + ']\n' 
    msg += '     Headers:    [' + ', '.join('%d' % (v) for k, v in self.header.iteritems()) + ']\n' 
    msg += '     Properties: ' + repr(self.properties) + '\n'
    msg += '     Globals:    ' + repr(self.globals) + '\n'
    msg += '     u9:         ' + repr(self.u9) + '\n'
    msg += repr(self.functions) + '\n'
    msg += repr(self.literals)

    return msg


class LingoFunctions(Sequence):
  
  def __init__(self, stream, headers_offset, n_records):
    header_length = 42

    self._records = [None] * n_records
    for i, _ in enumerate(self._records):
      offset = headers_offset + i*header_length
      self._records[i] = LingoFunction(stream, offset)

  def __getitem__(self, i):
    return self._records[i]

  def __len__(self):
    return len(self._records)

  def __repr__(self):
    msg = '     Functions:\n'
    for i, func in enumerate(self):
      msg += '       func%d:\n%s' % (i, repr(func))
    return msg
 

class LingoFunction(object):

  def __init__(self, stream, header_offset):
    self.__parse_header(stream, header_offset)
    self.__parse_bytecode(stream)
    self.__parse_args(stream)
    self.__parse_locals(stream)
    self.__parse_u3(stream)
    self.__parse_u7(stream)

  @property
  def header(self):
    return self._header

  @property
  def bytecode(self):
    return self._bytecode

  @property
  def args(self):
    return self._args

  @property
  def locals(self):
    return self._locals

  @property
  def u3(self):
    return self._u3

  @property
  def u4(self):
    return self._u4

  @property
  def u7(self):
    return self._u7

  @property
  def name_id(self):
    return self.header['function_id']

  def __parse_header(self, stream, header_offset):
    stream.seek(header_offset, 0)
    self._header = OrderedDict()
    self._header['function_id']   = stream.uint16()
    self._header['u2']            = stream.uint16()

    self._header['record_length'] = stream.uint32()
    self._header['record_offset'] = stream.uint32()

    self._header['n_args']        = stream.uint16()
    self._header['args_offset']   = stream.uint32()
    self._header['n_locals']      = stream.uint16()
    self._header['locals_offset'] = stream.uint32()
    self._header['n_u3']          = stream.uint16()
    self._header['u3_offset']     = stream.uint32()

    self._header['u4']            = stream.uint16()
    self._header['u5']            = stream.uint16()
    self._header['u6']            = stream.uint16()

    self._header['n_u7']          = stream.uint16()
    self._header['u7_offset']     = stream.uint32()

  def __parse_bytecode(self, stream):
    stream.seek(self.header['record_offset'], 0)
    self._bytecode = stream.read_bytes(self.header['record_length'])
    stream.read_pad(self.header['record_length'] % 2)

  def __parse_args(self, stream):
    stream.seek(self.header['args_offset'], 0)

    self._args = [None] * self.header['n_args']
    for i, _ in enumerate(self._args):
      self._args[i] = stream.uint16()

  def __parse_locals(self, stream):
    stream.seek(self.header['locals_offset'], 0)

    self._locals = [None] * self.header['n_locals']
    for i, _ in enumerate(self._locals):
      self._locals[i] = stream.uint16()

  def __parse_u3(self, stream):
    stream.seek(self.header['u3_offset'], 0)

    self._u3 = [None] * self.header['n_u3']
    for i, _ in enumerate(self._u3):
      self._u3[i] = stream.uint16()

  def __parse_u7(self, stream):
    stream.seek(self.header['u7_offset'], 0)

    self._u7 = [None] * self.header['n_u7']
    for i, _ in enumerate(self._u7):
      self._u7[i] = stream.uint8()

    stream.read_pad(self.header['n_u7'] % 2)
  
  def __repr__(self):
    msg = ('          header: [%s]\n'
           '        bytecode: %s\n'
           '            args: %s\n'
           '          locals: %s\n'
           '              u3: %s\n'
           '              u7: %s\n')
    args = (
        ', '.join('%s: %d' % (k, v) for k, v in self.header.iteritems()), 
        grouper(self.bytecode, 128, True, 22), 
        self.args, 
        self.locals, 
        self.u3, 
        self.u7)
  
    return msg % args
 
   
class LingoFunctionLiterals(Sequence):
  
  def __init__(self, stream, headers_offset, records_offset, n_records):
    header_length = 8
    self._records = [None] * n_records

    for i, _ in enumerate(self._records):
      stream.seek(headers_offset + i*header_length)

      literal_type    = stream.uint32()
      literal_offset  = stream.uint32()

      self._records[i] = LingoFunctionLiteral(stream, records_offset, literal_type, literal_offset)
  
  def __getitem__(self, i):
    return self._records[i]
  
  def __len__(self):
    return len(self._records)
  
  def __str__(self):
    return '[' + ', '.join(self) + ']'
  
  def __repr__(self):
    msg = '     Literals:\n'
    for i, item in enumerate(self):
      msg += '        %4d: %s\n' % (i, item)
    return msg

class LingoFunctionLiteral(Sized):

  TYPE_STRING = 1
  TYPE_INT    = 4
  TYPE_DOUBLE = 9

  TYPES = ('', 'string', '', '', 'int', '', '', '', '', 'double')

  def __init__(self, stream, records_offset, literal_type, literal_offset):
    self._type = literal_type

    if self.TYPES[literal_type] == 'string':
      stream.seek(records_offset + literal_offset)

      self._length  = stream.uint32()
      self._value   = stream.string(self._length)
      stream.read_pad(self._length % 2)

    elif self.TYPES[literal_type] == 'int': 
      self._length = 4
      self._value = literal_offset

    elif self.TYPES[literal_type] == 'double':
      stream.seek(records_offset + literal_offset)

      self._length = stream.uint32()
      if self._length == 8:
        self._value = stream.double()
      else:
        self._value = stream.float()

    else:
      raise Exception('Literal type %d not implemented' % literal_type)

  @property
  def type(self):
    return self._type

  @property
  def value(self):
    return self._value

  def __len__(self):
    return self._length
  
  def __str__(self):
    return '(%6s, \'%s\')' % (self.TYPES[self.type], str(self._value).replace('\r', '\\r'))

  def __repr__(self):
    return self.__repr__()
