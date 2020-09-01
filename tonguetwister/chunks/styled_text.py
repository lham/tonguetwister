from collections import Sized, Sequence, OrderedDict
from ..lib.helper import grouper

class StyledText(Sized):

  def __init__(self, stream):
    stream.set_big_endian()
    self.__parse_chunk_header(stream)
    self.__parse_text(stream)
    self.__parse_styles(stream)

  @property
  def header(self):
    return self._header

  @property
  def text(self):
    return self._text

  @property
  def styles(self):
    return self._styles

  def __parse_chunk_header(self, stream):
    self._header = OrderedDict()
    self._header['header_length'] = stream.uint32()
    self._header['text_length']   = stream.uint32()
    self._header['style_length']  = stream.uint32()

  def __parse_text(self, stream):
    self._text = stream.string(self.header['text_length'])

  def __parse_styles(self, stream):
    self._header['n_styles'] = stream.uint16()
    self._styles = TextStyles(stream, self.header['n_styles'])

  def __len__(self):
    return self._header['text_length']

  def __str__(self):
    return '("%s", %s)' % (self.text, self.styles)

  def __repr__(self):
    msg = ''
    msg += 'Text size: %s\n' % len(self)
    msg += repr(self.styles)
    return msg


class TextStyles(Sequence):

  def __init__(self, stream, n_styles):
    self._styles = [None] * n_styles
    for i, _ in enumerate(self._styles):
      self._styles[i] = TextStyle(stream)

  def __getitem__(self, i):
    return self._styles[i]

  def __len__(self):
    return len(self._styles)

  def __str__(self):
    return str(self._styles)

  def __repr__(self):
    msg = '    Styles:\n'
    for i, record in enumerate(self._styles):
      msg += '      style%2d: %s\n' % (i, record)
    return msg


class TextStyle(object):

  def __init__(self, stream):
      self._record = OrderedDict()
      self._record['u0']      = stream.uint16()
      self._record['offset']  = stream.uint32()
      self._record['u1']      = stream.uint16()
      self._record['u2']      = stream.uint16()
      self._record['u3']      = stream.uint32()
      r = stream.uint16()
      g = stream.uint16()
      b = stream.uint16()
      self._record['rgb']     = (r, g, b)

  @property
  def rgb(self):
    return self._record['rgb']

  def __str__(self):
    return '(' + ', '.join('%s: %s' % (k, v) for k, v in self._record.iteritems()) + ')' 
