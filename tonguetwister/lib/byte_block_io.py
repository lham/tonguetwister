import logging
from collections import OrderedDict
from contextlib import contextmanager
from io import BytesIO
from struct import unpack

logger = logging.getLogger('tonguetwister.lib.byte_block_io')
logger.setLevel(logging.DEBUG)


class ByteBlockIO:
    ENCODING = 'latin-1'  # Assumed
    BIG_ENDIAN = '>'
    LITTLE_ENDIAN = '<'

    def __init__(self, byte_block, endianess=LITTLE_ENDIAN):
        self.stream = BytesIO(byte_block)
        self.endianess = endianess
        self.total_bytes_processed = 0
        self.total_bytes = len(byte_block)
        self.byte_is_unprocessed = [True] * self.total_bytes

    def reset(self):
        self.stream.seek(0)
        self.total_bytes_processed = 0
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
                logger.warning(f'Byte at address 0x{addr+i:x} ({addr+i}) already read')

    def _parse_value(self, _type, n_bytes, endianess):
        endianess = self.endianess if endianess is None else endianess
        return unpack(endianess + _type, self._read(n_bytes))[0]

    def uint32(self, endianess=None):
        return self._parse_value('I', 4, endianess)

    def int32(self, endianess=None):
        return self._parse_value('i', 4, endianess)

    def uint16(self, endianess=None):
        return self._parse_value('H', 2, endianess)

    def int16(self, endianess=None):
        return self._parse_value('h', 2, endianess)

    def uint8(self, endianess=None):
        return self._parse_value('B', 1, endianess)

    def int8(self, endianess=None):
        return self._parse_value('b', 1, endianess)

    def float(self, endianess=None):
        return self._parse_value('f', 4, endianess)

    def double(self, endianess=None):
        return self._parse_value('d', 8, endianess)

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

    def auto_property_list(self, prop_reader_cls, offset_addr, n_offsets, n_items_per_sub_list=0, sub_list_prefix=''):
        """
        Read a property list from the stream.

        Arguments:
            prop_reader_cls:      The property reader, which may define parsers for the different properties
            offset_addr:          Address where the offsets are located
            n_offsets:            The number of offsets to read
            n_items_per_sub_list: If there are a number of items/sub-properties per property list, set this higher than
                                  zero to enable sub property lists
            sub_list_prefix:      If n_items_per_sub_list is larger than zero, this prefix will be used as kes for the
                                  sub lists.

        """
        prop_reader = prop_reader_cls()
        use_sub_lists = n_items_per_sub_list > 0
        prop_list = OrderedDict()

        # If we don't have sub lists in the property list, just use the main prop_list as the current sub list
        if use_sub_lists:
            sub_list = None
            n_sub_lists = (n_offsets - 1) // n_items_per_sub_list
        else:
            sub_list = prop_list
            n_sub_lists = 1

        # Initialize read
        data_addr = offset_addr + n_offsets * 4
        offset = self.uint32()

        for prop_id in range(n_offsets - 1):
            # Maybe update sub list
            if use_sub_lists:
                sub_list_id = prop_id // n_sub_lists
                prop_id = prop_id % n_sub_lists

                if prop_id == 0:
                    prop_list[f'{sub_list_prefix}{sub_list_id}'] = sub_list = OrderedDict()

            # Read the property
            next_offset = self.uint32()
            with self.offset_context(data_addr + offset):
                data = prop_reader.read(prop_id, self, next_offset - offset)
                sub_list.update(data)

            offset = next_offset

        # Set the pointer after the data
        self.seek(data_addr + offset)

        return prop_list
