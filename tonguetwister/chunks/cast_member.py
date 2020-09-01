from collections import OrderedDict
from ..lib.helper import splat_ordered_dict

class CastMember(object):

  MEDIA_TYPES = (
      '', '', '', 'field', '', '', '', '', 'shape', 
      '', '', 'script', '', '', '', '', '', '', '')

  def __init__(self, stream):
    stream.set_big_endian()
    self.__parse_chunk_header(stream)
    self.__parse_media(stream)

  @property
  def header(self):
    return self._header

  @property
  def media_type(self):
    return self._header['media_type']

  @property
  def member(self):
    return self._member

  def __parse_chunk_header(self, stream):
    self._header = OrderedDict()
    self._header['media_type']    = stream.uint32()
    self._header['data_length']   = stream.uint32()
    self._header['footer_length'] = stream.uint32()

  def __parse_media(self, stream):
    dl = self.header['data_length']
    fl = self.header['footer_length']

    if self.MEDIA_TYPES[self.media_type] == 'field':
      self._member = FieldMember(stream, dl, fl)
    elif self.MEDIA_TYPES[self.media_type] == 'shape':
      self._member = ShapeMember(stream, dl, fl)
    elif self.MEDIA_TYPES[self.media_type] == 'script':
      self._member = ScriptMember(stream, dl, fl)
    else:
      print('WARNING: Unknown media type (%d).' % self.media_type)
      self._member = None
      stream.read_bytes()

  def __repr__(self):
    if self.media_type == 11:
      return '    %s:\n%s' % (self.MEDIA_TYPES[self.media_type], repr(self.member))
    else:
      return ''


class FieldMember(object):
  
  def __init__(self, stream, data_length, footer_length):
    self.__parse_data(stream, data_length)
    self.__parse_footer(stream, footer_length)

  def __parse_data(self, stream, data_length):
    self._data = OrderedDict()
    if data_length > 0:
      self._data['u1']  = stream.uint32()
      self._data['u2']  = stream.uint32()
      self._data['u3']  = stream.uint32()
      self._data['u4']  = stream.uint32()
      self._data['u5']  = stream.uint32()
      self._data['u6']  = stream.uint32()
      self._data['u7']  = stream.uint32()
      self._data['u8']  = stream.uint32()
      self._data['u9']  = stream.uint16()
      self._data['u10'] = stream.uint32()
      self._data['u11'] = stream.uint32()
      self._data['u12'] = stream.uint32()
      self._data['u13'] = stream.uint32()
      self._data['u14'] = stream.uint32()
      self._data['u15'] = stream.uint32()
      self._data['u16'] = stream.uint32()
      self._data['u17'] = stream.uint32()
      self._data['u18'] = stream.uint32()

      self._data['text_length'] = stream.uint8()
      self._data['text']        = stream.string(self._data['text_length'])

  def __parse_footer(self, stream, footer_length):
    self._footer = OrderedDict()
    if footer_length > 0:
      self._footer['c1']  = (stream.uint16(), stream.uint16(), stream.uint16())
      self._footer['c2']  = (stream.uint16(), stream.uint16(), stream.uint16())
      self._footer['c3']  = (stream.uint16(), stream.uint16(), stream.uint16())
      self._footer['u1']  = stream.uint8()
      self._footer['u2']  = stream.uint8()
      self._footer['u3']  = stream.uint8()
      self._footer['u4']  = stream.uint8()
      self._footer['u5']  = stream.uint8()
      self._footer['u6']  = stream.uint8()
      self._footer['u7']  = stream.uint8()
      self._footer['u8']  = stream.uint8()
      self._footer['u9']  = stream.uint8()
      self._footer['u10'] = stream.uint8()
      self._footer['u11'] = stream.uint8()

  def __repr__(self):
    msg = '      Data: %s\n' % splat_ordered_dict(self._data)
    msg += '    Footer: %s\n' % splat_ordered_dict(self._footer)
    return msg


class ShapeMember(object):
  
  def __init__(self, stream, data_length, footer_length):
    self.__parse_data(stream, data_length)
    self.__parse_footer(stream, footer_length)

  def __parse_data(self, stream, data_length):
    self._data = OrderedDict()
    if data_length > 0:
      self._data['u1']  = stream.uint32()
      self._data['u2']  = stream.uint32()
      self._data['u3']  = stream.uint32()
      self._data['u4']  = stream.uint32()
      self._data['u5']  = stream.uint32()
      self._data['u6']  = stream.uint32()
      self._data['u7']  = stream.uint32()
      self._data['u8']  = stream.uint32()

      self._data['u9']  = stream.uint16()
      self._data['u10'] = stream.uint16()
      self._data['u11'] = stream.uint16()
      self._data['u12'] = stream.uint16()
      self._data['u13'] = stream.uint16()
      self._data['u14'] = stream.uint16()
      self._data['record_length'] = stream.uint16()
      self._data['text_length']   = stream.uint8()
      self._data['text']          = stream.string(self._data['text_length'])
      self._data['null_term']     = stream.uint8()

  def __parse_footer(self, stream, footer_length):
    self._footer = OrderedDict()
    if footer_length > 0:
      self._footer['u1']  = stream.uint16()
      self._footer['u2']  = stream.uint16()
      self._footer['u3']  = stream.uint16()
      self._footer['u4']  = stream.uint16()
      self._footer['u5']  = stream.uint16()
      self._footer['u6']  = stream.uint16()
      self._footer['u7']  = stream.uint8()
      self._footer['u8']  = stream.uint8()
      self._footer['u9']  = stream.uint8()
      self._footer['u10'] = stream.uint8()
      self._footer['u11'] = stream.uint8()

  def __repr__(self):
    msg = '      Data: %s\n' % splat_ordered_dict(self._data)
    msg += '    Footer: %s\n' % splat_ordered_dict(self._footer)
    return msg


class ScriptMember(object):
  
  def __init__(self, stream, data_length, footer_length):
    self.__parse_data(stream, data_length)
    self.__parse_footer(stream, footer_length)

  def __parse_data(self, stream, data_length):
    self._data = OrderedDict()
    if data_length > 0:
      self._data['u1']  = stream.uint32()

      self._data['script_number'] = (stream.uint8(), stream.uint8(), stream.uint8(), stream.uint8())
      self._data['u6']  = stream.uint32()
      self._data['u7']  = stream.uint32()

      self._data['script_id']  = stream.uint32()
      self._data['u9']  = stream.uint32()
      self._data['u10'] = stream.uint32()
      self._data['u11'] = stream.uint32()

      self._data['u12'] = stream.uint16()
      self._data['u13'] = stream.uint32()
      self._data['u14'] = stream.uint32()
      self._data['u15'] = stream.uint32()
      self._data['u16'] = stream.uint32()
      self._data['u17'] = stream.uint32()
      self._data['u18'] = stream.uint32()
      self._data['u19'] = stream.uint32()
      self._data['u20'] = stream.uint32()
      self._data['u21'] = stream.uint32()
      self._data['u22'] = stream.uint32()
      self._data['u23'] = stream.uint32()
      self._data['u24'] = stream.uint32()
      self._data['u25'] = stream.uint32()
      self._data['u26'] = stream.uint32()

      self._data['u27'] = stream.uint32()
      if self._data['u15'] > 0:
        self._data['text_length']   = stream.uint8()
        self._data['text']          = stream.string(self._data['text_length'])
        self._data['null_term']     = stream.uint8()

      self._data['u28'] = stream.uint8()
      self._data['u29'] = stream.uint8()
      self._data['u30'] = stream.uint8()
      self._data['u31'] = stream.uint8()
      self._data['u32'] = stream.uint8()
      self._data['u33'] = stream.uint8()
      self._data['u34'] = stream.uint8()
      self._data['u35'] = stream.uint8()

  def __parse_footer(self, stream, footer_length):
    self._footer = OrderedDict()
    if footer_length > 0:
      self._footer['u1']  = stream.uint8()
      self._footer['u2']  = stream.uint8()

  def __repr__(self):
    msg = '      Data: %s\n' % splat_ordered_dict(self._data)
    #msg = '      Data: '# % self._data.values()
    #for k, v in self._data.iteritems():
    #  if k[0] == 'u':
    #    msg += '%3d, ' % v
    #msg +='\n'

    msg += '    Footer: %s\n' % splat_ordered_dict(self._footer)
    #msg += '    Footer: %s\n' % self._footer.values()
    return msg
