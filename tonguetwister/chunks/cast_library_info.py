from collections import OrderedDict
from ..lib.helper import splat_ordered_dict

class CastLibraryInfo(object):
  
  def __init__(self, stream):
    stream.set_big_endian()
    self.__parse_chunk_header(stream)
    self.__parse_body(stream)

  @property
  def header(self):
    return self._header

  @property
  def body(self):
    return self._body

  def __parse_chunk_header(self, stream):
    self._header = OrderedDict()
    self._header['u1']          = stream.uint32()
    self._header['skip_length'] = stream.uint16()
    self._header['ux']          = stream.read_bytes(2*self._header['skip_length'])
    self._header['u2']          = stream.uint32()
    self._header['u3']          = stream.uint32()
    self._header['body_length'] = stream.uint32()

  def __parse_body(self, stream):
    self._body = OrderedDict()
    self._body['u1']          = stream.read_bytes(20)
    self._body['text_length'] = stream.uint8()
    self._body['text']        = stream.string(self._body['text_length'])
    stream.read_pad(1)

  def __repr__(self):
    msg = '    Header: %s\n' % splat_ordered_dict(self.header)
    msg += '      Body: %s\n' % splat_ordered_dict(self.body)
    return msg

