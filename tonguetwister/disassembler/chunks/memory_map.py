from tonguetwister.disassembler.chunkparser import EntryMapChunkParser, InternalEntryParser
from tonguetwister.lib.stream import ByteBlockIO


class MemoryMapEntry(InternalEntryParser):
    endianess = ByteBlockIO.LITTLE_ENDIAN

    public_data_attrs = ['four_cc', 'chunk_length', 'chunk_address']

    @classmethod
    def parse_data(cls, stream: ByteBlockIO):
        data = {}

        data['four_cc'] = stream.string_raw(4)
        data['chunk_length'] = stream.uint32()
        data['chunk_address'] = stream.uint32()
        data['u1'] = stream.uint16()
        data['u2'] = stream.uint16()
        data['u3'] = stream.uint16()
        data['u4'] = stream.uint16()

        return data


class MemoryMap(EntryMapChunkParser):
    entry_class = MemoryMapEntry
    endianess = ByteBlockIO.LITTLE_ENDIAN

    @classmethod
    def parse_header(cls, stream: ByteBlockIO):
        header = {}
        header['header_length'] = stream.uint16()
        header['entry_length'] = stream.uint16()
        header['allocated_array_elements'] = stream.uint32()
        header['used_array_elements'] = stream.uint32()
        header['?junk_entry_position'] = stream.int32()
        header['u1'] = stream.int32()
        header['?free_entry_position'] = stream.int32()

        return header
