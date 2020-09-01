from collections import Sequence, OrderedDict

class LingoNamelist(Sequence):

  def __init__(self, stream):
    stream.set_big_endian()
    self.__parse_chunk_header(stream)
    self.__parse_records(stream)

  @property
  def header(self):
    return self._header

  def __parse_chunk_header(self, stream):
    self._header = OrderedDict()
    self._header['u1']             = stream.uint32()
    self._header['u2']             = stream.uint32()
    self._header['chunk_length']   = stream.uint32()
    self._header['chunk_length_2'] = stream.uint32()
    self._header['header_length']  = stream.uint16()
    self._header['n_records']      = stream.uint16()

  def __parse_records(self, stream):
    self.records = [None] * self.header['n_records']
    for i, _ in enumerate(self.records):
      text_length     = stream.uint8()
      self.records[i] = stream.string(text_length)

  def __repr__(self):
    # Header
    msg = ('[unknown1: %2d, unknown2: %2d, '
           'chunk-len1: %3d, chunk-len2: %3d, '
           'header-len: %2d n_records: %2d]\n')
    ret_msg = msg % tuple(self.header.values())
    
    # Records
    for i, name in enumerate(self.records):
      ret_msg += '%s%-4d: %s\n' % ('    ', i, name)

    return ret_msg

  def __str__(self):
    return str(self.records)

  def __getitem__(self, i):
    return self.records[i]

  def __len__(self):
    return len(self.records)



