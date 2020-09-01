from struct import unpack
from StringIO import StringIO

class ByteBlockIO(object):
  BIG_ENDIAN = '>'
  LITTLE_ENDIAN = '<'

  def __init__(self, byte_block):
    self.stream = StringIO(byte_block)
    self.endianess = self.LITTLE_ENDIAN
    self.n_processed_bytes = 0
    self.stream_size = len(byte_block)
    self.byte_is_unprocessed = [True] * self.stream_size

  def __read(self, n=-1):
    word = self.stream.read(n)
    
    if len(word) != n:
      raise BufferError('Unable to read %d bytes from the stream.' % n)
    else:
      self.n_processed_bytes += n

      addr = self.stream.tell() - n
      for i in xrange(0, n):
        if self.byte_is_unprocessed[addr+i]:
          self.byte_is_unprocessed[addr+i] = False
        else:
          print 'WARNING: Reading byte already read: %d' % (addr+i)

      return word

  def uint32(self):
    return unpack(self.endianess + 'I', self.__read(4))[0]

  def uint16(self):
    return unpack(self.endianess + 'H', self.__read(2))[0]

  def uint8(self):
    return unpack(self.endianess + 'B', self.__read(1))[0]
  
  def float(self):
    return unpack(self.endianess + 'f', self.__read(4))[0]

  def double(self):
    return unpack(self.endianess + 'd', self.__read(8))[0]

  def string(self, size):
    word = self.__read(size)
    if self.endianess == self.LITTLE_ENDIAN:
      return word[::-1]
    else:
      return word

  def read_bytes(self, size=-1):
    if size < 0:
      size = self.size() - self.tell()
    return self.__read(size)

  def read_pad(self, size):
    return self.read_bytes(size)

  def size(self):
    return self.stream_size

  def tell(self):
    return self.stream.tell()

  def seek(self, addr, direction=0):
    return self.stream.seek(addr, direction)

  def is_depleted(self):
    return self.n_processed_bytes >= self.stream_size

  def set_big_endian(self):
    self.endianess = self.BIG_ENDIAN

  def set_little_endian(self):
    self.endianess = self.LITTLE_ENDIAN

  def n_processed_bytes_string(self):
    return 'Used bytes: %d/%d' % (self.n_processed_bytes, self.stream_size)

  def unprocessed_bytes(self):
    return [i for i, x in enumerate(self.byte_is_unprocessed) if x]
