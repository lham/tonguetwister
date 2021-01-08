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

    def get_linked_resource(self, parent: ChunkParser, child_type: ChunkType, as_chunk=True):
        resource = self.resources.get_child_resource(parent.resource, child_type)

        return resource.chunk if as_chunk else resource

    @property
    def chunks(self):
        return [(resource.chunk_address, resource.chunk) for resource in self.resources.to_list()]

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

    # def _create_cast_lib(self):
    #     """
    #     Iterate the CAS*:
    #       Add CASt to cast library AS entry:
    #         i = mmap-index of CASt in mmap
    #         Lookup mmap[i], add CASt data to entry
    #
    #         k = mmap-index of key*(cast_mmap_idx=i)
    #         Lookup mmap[k] and add media type data to entry
    #     """
    #     pass
    #
    # @property
    # def lingo_scripts(self) -> list:
    #     return [chunk for _, chunk in self.chunks if isinstance(chunk, LingoScript)]
    #
    # @property
    # def namelist(self) -> Union[LingoNamelist, None]:
    #     namelists = [chunk for _, chunk in self.chunks if isinstance(chunk, LingoNamelist)]
    #     if len(namelists) == 0:
    #         return None
    #     if len(namelists) > 1:
    #         print('Warning: More than one namelist')
    #     return namelists[0]
