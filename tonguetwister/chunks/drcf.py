from collections import OrderedDict
from ..lib.helper import splat_ordered_dict

class DRCF(object):

  def __init__(self, stream):
    stream.set_big_endian()
    self._drcf = OrderedDict()
    self._drcf['chunk_length'] = stream.uint16()
    self._drcf['u1']           = stream.read_bytes()

  @property
  def values(self):
    return self._drcf

  def __repr__(self):
    return splat_ordered_dict(self.values)
