from collections import Sequence, OrderedDict

class FontMap(Sequence):

  def __init__(self, stream):
    stream.set_big_endian()
    self.__parse_chunk_header(stream)
    self.__parse_record_headers(stream)
    self.__parse_font_data(stream)
    self.__parse_records(stream)

    stream.seek(60 + self._font_data['font_data_length'])
    stream.read_bytes()  # Rest is unknown

  @property
  def header(self):
    return self._header

  def __parse_chunk_header(self, stream):
    self._header = OrderedDict()
    self._header['u1']              = stream.uint32()
    self._header['records_length']  = stream.uint32()
    self._header['u2']              = stream.uint32()
    self._header['u3']              = stream.uint32()
    self._header['n_font_records']  = stream.uint32()
    self._header['n_font_headers']  = stream.uint32()
    self._header['u4']              = stream.uint16()
    self._header['u5']              = stream.uint16()
    self._header['u6']              = stream.uint32()
    self._header['u7']              = stream.uint32()

  def __parse_record_headers(self, stream):
    self._record_headers = [None] * self.header['n_font_headers']
    for i, _ in enumerate(self._record_headers):
      self._record_headers[i] = OrderedDict()
      self._record_headers[i]['offset'] = stream.uint32()
      self._record_headers[i]['u1']     = stream.uint16()
      self._record_headers[i]['u2']     = stream.uint16()

  def __parse_font_data(self, stream):
    self._font_data = OrderedDict()
    self._font_data['u8']                = stream.uint32()
    self._font_data['u9']                = stream.uint32()
    self._font_data['font_data_length']  = stream.uint32()
    self._font_data['total_body_length'] = stream.uint32()
    self._font_data['offset_to_fonts']   = stream.uint16()

  def __parse_records(self, stream):
    self._records = [None] * self.header['n_font_records']
    for i, _ in enumerate(self._records):
      offset = 60
      self._records[i] = Font(stream, self._record_headers[i], offset)

  def __getitem__(self, i):
    return self._records[i]

  def __len__(self):
    return len(self._records)

  def __repr__(self):
    msg = '    Header: %s\n' % ', '.join('%s: %s' % (k, v) for k, v in self.header.iteritems())
    msg += '    FHead: %s\n' % ', '.join('%s' % (v) for v in self._record_headers)
    msg += '    FData: %s\n' % ', '.join('%s: %s' % (k, v) for k, v in self._font_data.iteritems())
    for i, record in enumerate(self):
      msg += '        %2d: %s\n' % (i, record)
    return msg


class Font(object):

  def __init__(self, stream, header, records_offset):
    if header['offset'] >> 31 != 1:
      stream.seek(records_offset + header['offset'])
      self._name_length = stream.uint32()
      self._name        = stream.string(self._name_length)
      stream.read_pad(4 - ((4 + self._name_length) % 4))  # 4-byte aligned padding
    else:
      self._name = 'N/A'
      self._name_length = 0

    self._header = header

  @property
  def name(self):
    return self._name

  @property
  def header(self):
    return self._header

  def __str__(self):
    return '(%16s, %s)' % (self.name, ['%s: %s' % (k, v) for k, v in self.header.iteritems()])
