from collections import OrderedDict
from contextlib import contextmanager
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

    def uint32(self, endianess=None):
        endianess = self.endianess if endianess is None else endianess
        return unpack(endianess + 'I', self._read(4))[0]

    def int32(self, endianess=None):
        endianess = self.endianess if endianess is None else endianess
        return unpack(endianess + 'i', self._read(4))[0]

    def uint16(self, endianess=None):
        endianess = self.endianess if endianess is None else endianess
        return unpack(endianess + 'H', self._read(2))[0]

    def int16(self, endianess=None):
        endianess = self.endianess if endianess is None else endianess
        return unpack(endianess + 'h', self._read(2))[0]

    def uint8(self, endianess=None):
        endianess = self.endianess if endianess is None else endianess
        return unpack(endianess + 'B', self._read(1))[0]

    def int8(self, endianess=None):
        endianess = self.endianess if endianess is None else endianess
        return unpack(endianess + 'b', self._read(1))[0]

    def float(self, endianess=None):
        endianess = self.endianess if endianess is None else endianess
        return unpack(endianess + 'f', self._read(4))[0]

    def double(self, endianess=None):
        endianess = self.endianess if endianess is None else endianess
        return unpack(endianess + 'd', self._read(8))[0]

    def string_raw(self, length, endianess=None):
        return self._string(length, endianess)

    def string_auto(self, endianess=None):
        length = self.uint8(endianess)
        string = self._string(length, endianess)
        _ = self.read_bytes(1)  # The null termination byte

        return string

    def _string(self, size, endianess=None):
        endianess = self.endianess if endianess is None else endianess
        word = self._read(size).decode(self.ENCODING)
        if endianess == self.LITTLE_ENDIAN:
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

    @staticmethod
    def bytes_to_16bit_word(byte_list, endianess):
        return unpack(endianess + 'H', bytes(byte_list))[0]

    @staticmethod
    def bytes_to_32bit_word(byte_list, endianess):
        return unpack(endianess + 'I', bytes(byte_list))[0]

    @contextmanager
    def offset_context(self, position):
        addr = self.stream.tell()

        try:
            self.stream.seek(position)
            yield
        finally:
            self.stream.seek(addr)

    def auto_property_list(self, prop_reader, offset_addr, n_offsets, n_items_per_sub_list=0, item_prefix=''):
        prop_list = OrderedDict()

        # If we don't have sub lists in the property list, just use the main prop_list as the current sub list
        if n_items_per_sub_list == 0:
            sub_list = prop_list
            n_sub_lists = 1
        else:
            sub_list = None
            n_sub_lists = (n_offsets - 1) // n_items_per_sub_list

        # Initialize read
        data_addr = offset_addr + n_offsets * 4
        offset = self.uint32()

        for prop_id in range(n_offsets - 1):
            # Maybe update sub list
            if n_items_per_sub_list > 0 and prop_id % n_sub_lists == 0:
                prop_list[f'{item_prefix}{prop_id // n_sub_lists}'] = sub_list = OrderedDict()

            # Read the property
            next_offset = self.uint32()
            with self.offset_context(data_addr + offset):
                if n_items_per_sub_list > 0:
                    prop_id = prop_id % n_sub_lists

                data = prop_reader.read(prop_id, self, next_offset - offset)
                sub_list.update(data)

            offset = next_offset

        return prop_list
