from tonguetwister.disassembler.chunkparser import EntryMapChunkParser, InternalEntryParser
from tonguetwister.lib.stream import ByteBlockIO


class LingoContext(EntryMapChunkParser):
    @classmethod
    def parse_header(cls, stream: ByteBlockIO):
        header = {}
        header['u1'] = stream.uint32()
        header['u2'] = stream.uint32()
        header['n_scripts'] = stream.uint32()
        header['n_scripts_2'] = stream.uint32()
        header['records_offset'] = stream.uint16()
        header['record_length'] = stream.uint16()
        header['u4'] = stream.uint16()
        header['u5'] = stream.uint16()
        header['lnam_id'] = stream.uint32()
        header['n_used?'] = stream.uint16()
        header['u6'] = stream.uint16()
        header['first_empty_slot_idx'] = stream.uint16()
        header['u7'] = stream.uint16()
        header['u8'] = stream.uint16()
        header['u9'] = stream.uint16()
        stream.read_bytes(56)

        return header

    @classmethod
    def parse_entries(cls, stream: ByteBlockIO, header):
        stream.seek(header['records_offset'])
        return [ContextEntry.parse(stream) for _ in range(header['n_scripts'])]


class ContextEntry(InternalEntryParser):
    @classmethod
    def parse_data(cls, stream: ByteBlockIO):
        data = {}
        data['script_number'] = (stream.uint8(), stream.uint8(), stream.uint8(), stream.uint8())
        data['mmap_idx'] = stream.uint32()
        data['u2'] = stream.uint16()
        data['u3'] = stream.uint16()

        return data
