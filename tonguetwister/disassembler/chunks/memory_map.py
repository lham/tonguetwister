from tonguetwister.disassembler.chunkparser import EntryMapChunkParser, InternalChunkEntryParser
from tonguetwister.lib.stream import ByteBlockIO


class MemoryMap(EntryMapChunkParser):
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

    @classmethod
    def parse_entries(cls, stream: ByteBlockIO, header):
        entries = [MemoryMapEntry.parse(stream) for _ in range(header['used_array_elements'])]

        # Read the allocated but unused array slots
        stream.read_bytes(header['entry_length'] * (header['allocated_array_elements'] - header['used_array_elements']))

        return entries


class MemoryMapEntry(InternalChunkEntryParser):
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

    def is_active(self):
        from tonguetwister.disassembler.mappings.chunks import ChunkType

        return self.four_cc != ChunkType.Free.four_cc and self.four_cc != ChunkType.Junk.four_cc
