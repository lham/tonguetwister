import logging

from tonguetwister.disassembler.chunkparser import UnknownChunkParser
from tonguetwister.disassembler.chunks.resource_key_table import ResourceKeyTable
from tonguetwister.disassembler.errors import BadMemoryMapEntry, ResourceAlreadyExists, ResourceNotLocated
from tonguetwister.disassembler.chunks.initial_map import InitialMap
from tonguetwister.disassembler.chunks.memory_map import MemoryMapEntry, MemoryMap
from tonguetwister.disassembler.mappings.chunks import ChunkType
from tonguetwister.lib.stream import ByteBlockIO

logger = logging.getLogger('tonguetwister.file_disassembler.resource_engine')
logger.setLevel(logging.DEBUG)


class Resource:
    def __init__(self, resource_id: int):
        self.resource_id = resource_id


class AbstractResource(Resource):
    INTERNAL_RESOURCE_ID = 1024


class ChunkResource(Resource):
    def __init__(self, resource_id: int, chunk_type: ChunkType, address: int):
        super().__init__(resource_id)

        self.chunk_type = chunk_type
        self.chunk_address = address
        self.chunk = None

        if self.chunk_type.parser == UnknownChunkParser:
            logger.warning(f'Chunk parser not implemented for [{self.chunk_type}]')

    def parse_chunk(self, stream: ByteBlockIO, ignore_check=False):
        logger.debug(f'Extracting chunk resource {self.resource_id:3d}: [{self.chunk_type}]'
                     f' at 0x{self.chunk_address:08x}'
                     f' -> {self.chunk_type.name}')

        chunk_stream = self._extract_chunk_stream(stream)

        self.chunk = self.chunk_type.parser.parse(chunk_stream)
        self.chunk.resource = self

        if not ignore_check and not chunk_stream.is_depleted():
            logger.warning(f'{self.chunk_type}: Unprocessed data remains for stream:\n'
                           f'{chunk_stream.get_processed_bytes_string()}\n'
                           f'{chunk_stream.get_unprocessed_bytes_array()}')
            raise RuntimeError()

    def _extract_chunk_stream(self, stream: ByteBlockIO) -> (str, int, bytes):
        stream.seek(self.chunk_address)

        four_cc = stream.string_raw(4)
        chunk_length = stream.uint32()

        if (stream.size() - stream.tell()) < chunk_length:
            # TODO: Hack to open some files... For some reason some RIFX chunk lengths are 1 byte too long?
            # TODO: Just read the remaining bytes :)
            chunk_data = stream.read_bytes(stream.size() - stream.tell())
        else:
            chunk_data = stream.read_bytes(chunk_length)

        # TODO: Mark padding as read?

        if four_cc != self.chunk_type.four_cc:
            raise BadMemoryMapEntry()

        return ByteBlockIO(chunk_data)

    @classmethod
    def from_memory_map_entry(cls, index: int, entry: MemoryMapEntry):
        return cls(index, ChunkType(entry.four_cc), entry.chunk_address)

    def __repr__(self):
        return f'<ChunkResource: {self.resource_id:03d}::{self.chunk_type.name}>'


class ResourceEngine:
    RESOURCE_ID_RIFX = 0
    RESOURCE_ID_IMAP = 1
    RESOURCE_ID_MMAP = 2
    RESOURCE_ID_KEY_TABLE = 3

    def __init__(self):
        self._resources = {}
        self._relationships = {}

    def insert(self, resource: Resource):
        self._resources[resource.resource_id] = resource

    def get_child_resource(self, parent_resource_id: int, child_chunk_type: ChunkType):
        primary_key = (parent_resource_id, child_chunk_type.four_cc)
        if primary_key not in self._relationships:
            return None

        return self._relationships[primary_key]

    def __getitem__(self, resource_id):
        if resource_id not in self._resources:
            raise ResourceNotLocated()

        return self._resources[resource_id]

    def build_relationships(self):
        for entry in self.resource_key_table.entries:
            ChunkType(entry.child_four_cc)  # Parse the chunk type as a means of validation

            if entry.primary_key in self._relationships:
                raise ResourceAlreadyExists()

            if entry.child_resource_id not in self._resources:
                raise ResourceNotLocated()

            self._relationships[entry.primary_key] = self._resources[entry.child_resource_id]

    @property
    def initial_map(self) -> InitialMap:
        return self[self.RESOURCE_ID_IMAP].chunk

    @property
    def memory_map(self) -> MemoryMap:
        return self[self.RESOURCE_ID_MMAP].chunk

    @property
    def resource_key_table(self) -> ResourceKeyTable:
        return self[self.RESOURCE_ID_KEY_TABLE].chunk

    def to_list(self):
        return self._resources.values()
