from io import BytesIO
from struct import unpack


class ByteBlockIO:
    ENCODING = 'latin-1'  # Assumed
    BIG_ENDIAN = '>'
    LITTLE_ENDIAN = '<'

    def __init__(self, byte_block):
        self.stream = BytesIO(byte_block)
        self.endianess = self.LITTLE_ENDIAN
        self.total_bytes_processed = 0
        self.total_bytes = len(byte_block)
        self.byte_is_unprocessed = [True] * self.total_bytes

    def _read(self, n_bytes=-1):
        word = self.stream.read(n_bytes)
        if len(word) != n_bytes:
            raise BufferError(f'Unable to read {n_bytes} bytes from the stream')

        self.total_bytes_processed += n_bytes
        self._mark_bytes_as_read(n_bytes)

        return word

    def _mark_bytes_as_read(self, n_bytes):
        addr = self.stream.tell() - n_bytes

        for i in range(n_bytes):
            if self.byte_is_unprocessed[addr + i]:
                self.byte_is_unprocessed[addr + i] = False
            else:
                print(f'WARNING: Byte at address {addr + i} already read')

    def uint32(self):
        return unpack(self.endianess + 'I', self._read(4))[0]

    def uint16(self):
        return unpack(self.endianess + 'H', self._read(2))[0]

    def uint8(self):
        return unpack(self.endianess + 'B', self._read(1))[0]

    def float(self):
        return unpack(self.endianess + 'f', self._read(4))[0]

    def double(self):
        return unpack(self.endianess + 'd', self._read(8))[0]

    def string(self, size):
        word = self._read(size).decode(self.ENCODING)
        if self.endianess == self.LITTLE_ENDIAN:
            return word[::-1]
        else:
            return word

    def read_bytes(self, size=-1):
        if size < 0:
            size = self.size() - self.tell()
        return self._read(size)

    def read_pad(self, size):
        return self.read_bytes(size)

    def size(self):
        return self.total_bytes

    def tell(self):
        return self.stream.tell()

    def seek(self, addr, direction=0):
        return self.stream.seek(addr, direction)

    def is_depleted(self):
        return self.total_bytes_processed >= self.total_bytes

    def set_big_endian(self):
        self.endianess = self.BIG_ENDIAN

    def set_little_endian(self):
        self.endianess = self.LITTLE_ENDIAN

    def get_processed_bytes_string(self):
        return f'Used bytes: {self.total_bytes_processed}/{self.total_bytes}'

    def get_unprocessed_bytes_array(self):
        return [i for (i, x) in enumerate(self.byte_is_unprocessed) if x]
