from collections import OrderedDict, Sequence

class MemoryMap(Sequence):

  def __init__(self, stream):
    self.__parse_chunk_header(stream)
    self.__parse_records(stream)

  @property
  def header(self):
    return self._header

  def __parse_chunk_header(self, stream):
    self._header = OrderedDict()
    self._header['header_length']       = stream.uint16()
    self._header['record_length']       = stream.uint16()
    self._header['n_four_cc_available'] = stream.uint32()
    self._header['n_four_cc_used']      = stream.uint32()
    self._header['u1']                  = stream.uint32()
    self._header['u2']                  = stream.uint32()
    self._header['first_empty_idx']     = stream.uint32()  # Free pointer

  def __parse_records(self, stream):
    self._records = [None] * self.header['n_four_cc_available']
    for i, _ in enumerate(self._records):
      self._records[i] = OrderedDict()
      self._records[i]['active']          = i < self.header['n_four_cc_used']
      self._records[i]['four_cc']         = stream.string(4)
      self._records[i]['block_length']    = stream.uint32()
      self._records[i]['block_address']   = stream.uint32()
      self._records[i]['protected_flag']  = stream.uint32()
      self._records[i]['u1']              = stream.uint32()

  def __getitem__(self, i):
    return self._records[i]

  def __len__(self):
    return len(self._records)

  def __repr__(self):
    msg = '    Header: %s\n' % ', '.join('%s: %s' % (k, v) for k, v in self.header.iteritems())
    for i, record in enumerate(self._records):
      msg += '    %4d: %s\n' % (i, ', '.join('%s: %s' % (k, v) for k, v in record.iteritems()))
    return msg
