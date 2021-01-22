import logging

from tonguetwister.disassembler.chunkparser import ChunkParser
from tonguetwister.disassembler.errors import UnexpectedChunkClass, InvalidDirectorFile
from tonguetwister.disassembler.mappings.chunks import ChunkType
from tonguetwister.disassembler.resources import ChunkResource, ResourceEngine
from tonguetwister.lib.stream import ByteBlockIO
from tonguetwister.xformat.movie import MovieFormat
from tonguetwister.xformat.rect import Rect

logger = logging.getLogger('tonguetwister.file_disassembler.file_disassembler')
logger.setLevel(logging.DEBUG)


class FileDisassembler:
    ADDRESS_RIFX = 0x00  # The rifx chunk is always found at address 0, it's how we identify the file
    ADDRESS_IMAP = 0x0c  # The initial map is always located right after the rifx chunk (actually inside the chunk data)

    def __init__(self, filename=None, silent=False):
        self.stream = None
        self.resources = ResourceEngine()
        self.movie = MovieFormat()

        if filename is not None:
            self.load_file(filename)

    def load_file(self, filename):
        with open(filename, 'rb') as f:
            try:
                logger.info(f'Reading file {filename}...')
                self.stream = ByteBlockIO(f.read())
                self._parse_rifx()
            except UnexpectedChunkClass:
                raise InvalidDirectorFile()

    def unpack(self):
        logger.info('Unpacking RIFX director file')
        self.stream.reset()

        self._parse_initial_map()
        self._parse_memory_map()
        self._parse_resources()
        self._parse_relationships()

        self._build_xformat()

    def _parse_rifx(self):
        resource = ChunkResource(ResourceEngine.RESOURCE_ID_RIFX, ChunkType.RIFX, self.ADDRESS_RIFX)
        resource.parse_chunk(self.stream, True)
        self.resources.insert(resource)

    def _parse_initial_map(self):
        resource = ChunkResource(ResourceEngine.RESOURCE_ID_IMAP, ChunkType.InitialMap, self.ADDRESS_IMAP)
        resource.parse_chunk(self.stream)
        self.resources.insert(resource)

    def _parse_memory_map(self):
        address = self.resources.initial_map.mmap_address
        resource = ChunkResource(ResourceEngine.RESOURCE_ID_MMAP, ChunkType.MemoryMap, address)
        resource.parse_chunk(self.stream)
        self.resources.insert(resource)

    def _parse_resources(self):
        for index, entry in enumerate(self.resources.memory_map.entries):
            if entry.four_cc == ChunkType.Free.four_cc or entry.four_cc == ChunkType.Junk.four_cc:
                continue

            if index > ResourceEngine.RESOURCE_ID_MMAP:
                resource = ChunkResource.from_memory_map_entry(index, entry)
                resource.parse_chunk(self.stream)
                self.resources.insert(resource)

    def _parse_relationships(self):
        self.resources.build_relationships()

    def get_resource(self, chunk: ChunkParser, as_chunk=True):
        return self.get_resource_by_id(chunk.resource.resource_id, as_chunk)

    def get_resource_by_id(self, resource_id: int, as_chunk=True):
        resource = self.resources[resource_id]
        return self._chunk_or_resource(resource, as_chunk)

    def get_linked_resource(self, parent: ChunkParser, child_type: ChunkType, as_chunk=True):
        return self.get_linked_resource_by_id(parent.resource.resource_id, child_type, as_chunk)

    def get_linked_resource_by_id(self, parent_resource_id, child_type: ChunkType, as_chunk=True):
        resource = self.resources.lookup_child_resource(parent_resource_id, child_type)
        return self._chunk_or_resource(resource, as_chunk)

    @staticmethod
    def _chunk_or_resource(resource, as_chunk):
        if as_chunk and resource is not None:
            return resource.chunk

        return resource

    def reverse_lookup_parent_resource_id(self, chunk: ChunkParser):
        return self.resources.reverse_lookup_parent_id(chunk.resource.resource_id, chunk.resource.chunk_type)

    @property
    def chunk_resources(self):
        return self.resources.to_list()

    def _build_xformat(self):
        # Parse data from director config
        # self.movie.info.stage_rect = Rect(**self.director_config.stage_rect)

        # self._parse_move_cast_libs  # MCsL
        # self._parse_cast_sort_order()  # Sord
        # self._parse_score()  # VWSC
        # TODO: FCOL (Favorite colors)
        # TODO: VWFI (FileInfo)
        # TODO: GRID (Guides and Grid)
        # TODO: FXmp (Font map)
        pass

    @property
    def director_config(self):
        # return self.resources.get_director_config_chunk()
        pass

    # @property
    # def namelist(self) -> Union[LingoNamelist, None]:
    #     namelists = [chunk for _, chunk in self.chunks if isinstance(chunk, LingoNamelist)]
    #     if len(namelists) == 0:
    #         return None
    #     if len(namelists) > 1:
    #         print('Warning: More than one namelist')
    #     return namelists[0]
