from collections import OrderedDict, Sequence
from ..lib.helper import splat_ordered_dict

class LingoContext(Sequence):

  def __init__(self, stream):
    stream.set_big_endian()
    self.__parse_chunk_header(stream)
    self.__parse_records(stream)

  def __parse_chunk_header(self, stream):
    self._context = OrderedDict()
    self._context['u1'] = stream.uint32()
    self._context['u2'] = stream.uint32()
    self._context['n_scripts'] = stream.uint32()
    self._context['n_scripts_2'] = stream.uint32()
    self._context['records_offset'] = stream.uint16()
    self._context['record_length'] = stream.uint16()
    self._context['u4'] = stream.uint16()
    self._context['u5'] = stream.uint16()
    self._context['lnam_id'] = stream.uint32()
    self._context['n_used?'] = stream.uint16()
    self._context['u6'] = stream.uint16()
    self._context['first_empty_slot_idx'] = stream.uint16()
    self._context['u7'] = stream.uint16()
    self._context['u8'] = stream.uint16()
    self._context['u9'] = stream.uint16()
    stream.read_bytes(56)

  def __parse_records(self, stream):
    stream.seek(self.header['records_offset'])
    self._records = [None] * self.header['n_scripts']
    for i, _ in enumerate(self._records):
      self._records[i] = OrderedDict()
      self._records[i]['script_number'] = (stream.uint8(), stream.uint8(), stream.uint8(), stream.uint8())
      self._records[i]['mmap_idx'] = stream.uint32()
      self._records[i]['u2'] = stream.uint16()
      self._records[i]['u3'] = stream.uint16()

  @property
  def header(self):
    return self._context

  def __getitem__(self, i):
    return self._records[i]

  def __len__(self):
    return len(self._records)

  def __repr__(self):
    msg = '    Header:%s\n' % splat_ordered_dict(self.header)
    for i, record in enumerate(self._records):
      msg += '    %2d: %s\n' % (i, splat_ordered_dict(record))
    return msg
