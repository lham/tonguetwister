from collections import OrderedDict, Sequence
from ..lib.helper import splat_ordered_dict

class CastAssociationMap(Sequence):

  def __init__(self, stream):
    stream.set_big_endian()
    self.__parse_records(stream)

  def __parse_records(self, stream):
    self._records = []
    while stream.tell() < stream.size():
      self._records.append(OrderedDict())
      self._records[-1]['mmap_idx'] = stream.uint32()

  def __getitem__(self, i):
    return self._records[i]

  def __len__(self):
    return len(self._records)

  def __repr__(self):
    msg = 'Associations\n'
    for i, record in enumerate(self._records):
      msg += '    %4d: %s\n' % (i, splat_ordered_dict(record))
    return msg
