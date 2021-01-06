import logging
import pprint

from tonguetwister.disassembler.chunks.cast_key_map import CastKeyMapEntry
from tonguetwister.disassembler.chunk import Chunk
from tonguetwister.disassembler.chunks.rifx import Rifx
from tonguetwister.disassembler.errors import \
    UnexpectedChunkClass, \
    InvalidDirectorFile, \
    BadResourceCollection, \
    BadRelationCollection
from tonguetwister.disassembler.chunks.initial_map import InitialMap
from tonguetwister.disassembler.chunks.memory_map import MemoryMap
from tonguetwister.disassembler.reader import extract_chunk
from tonguetwister.disassembler.resources import ResourceCollection, Resource
from tonguetwister.lib.byte_block_io import ByteBlockIO

logger = logging.getLogger('tonguetwister.file_disassembler.disassembler')
logger.setLevel(logging.DEBUG)


class FileDisassembler:
    def __init__(self, filename=None, silent=False):
        self.stream = None
        self.resources = ResourceCollection()
        self.data_mapping = {}

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
        self._parse_relations()
        # self._parse_config()  # VWCF or DRCF (DRCF is the later name, from around v6 or so)
        # self._parse_move_cast_libs  # MCsL
        # self._parse_cast_sort_order()  # Sord
        # self._parse_score()  # VWSC
        # TODO: FCOL (Favorite colors)
        # TODO: VWFI (FileInfo)
        # TODO: GRID (Guides and Grid)
        # TODO: FXmp (Font map)

    def _parse_chunk(self, address, resource_id, expected_chunk_class, ignore_parse_check=False):
        chunk = extract_chunk(self.stream, address, expected_chunk_class, ignore_parse_check)
        self.resources.append(Resource.from_chunk(chunk, resource_id, address))

    def _parse_rifx(self):
        address = 0  # The rifx chunk is always found at address 0, it's how we identify the file
        self._parse_chunk(address, 0, Rifx, True)

    def _parse_initial_map(self):
        address = 12  # The initial map is always located right after the rifx chunk (actually inside the chunk data)
        self._parse_chunk(address, 1, InitialMap)

    def _parse_memory_map(self):
        address = self.resources.get_initial_map_chunk().mmap_address
        self._parse_chunk(address, 2, MemoryMap)

    def _parse_resources(self):
        for i, entry in enumerate(self.resources.get_memory_map_chunk().entries):
            if not entry.is_active():
                continue

            logger.debug(f'Extracting mmap entry {i:3d}: [{entry.four_cc}]'
                         f' at 0x{entry.address:08x}'
                         f' -> {entry.get_class().__name__}')

            if self.resources.find_by_address(entry.address) is not None:
                self._validate_preparsed_resource(self.resources.find_by_address(entry.address), entry, i)
            else:
                self._parse_chunk(entry.address, i, entry.get_class())

    def _parse_relations(self):
        for entry in self.resources.get_key_map_chunk().entries:
            if not entry.is_active():
                continue

            if (entry.parent_resource_id, entry.four_cc) in self.data_mapping:
                logger.error(f'A data resource for ({entry.parent_resource_id}, {entry.four_cc}) already exist!')
                raise BadRelationCollection()
            else:
                self._validate_mapping_entry(entry)
                self.data_mapping[(entry.parent_resource_id, entry.four_cc)] = self.resources.find_by_resource_id(
                    entry.child_resource_id
                )

        pprint.pprint(self.data_mapping)

    def get_mapped_data_chunk(self, parent: Chunk, four_cc: str):
        parent_resource = self.resources.find_by_address(parent.address)  # TODO: save a reference chunk.resource?
        data_resource = self.data_mapping[(parent_resource.resource_id, four_cc)]

        return data_resource.chunk

    @property
    def chunks(self):
        return [(resource.chunk_address, resource.chunk) for resource in self.resources.all()]

    @staticmethod
    def _validate_preparsed_resource(resource, mmap_entry, resource_id):
        validations = [
            resource.resource_id == resource_id,
            resource.chunk.four_cc == mmap_entry.four_cc,
            resource.chunk_address == mmap_entry.address,
            resource.active
        ]

        if not all(validations):
            raise BadResourceCollection()

    def _validate_mapping_entry(self, entry: CastKeyMapEntry):
        # TODO: Can't validate parent exist yet, since those resources are not parsed at this point...
        validations = [
            # self.resources.find_by_resource_id(entry.parent_resource_id) is not None,
            self.resources.find_by_resource_id(entry.child_resource_id) is not None,
            self.resources.find_by_resource_id(entry.child_resource_id).chunk.four_cc == entry.four_cc,
            entry.is_active()
        ]

        if not all(validations):
            raise BadRelationCollection()
