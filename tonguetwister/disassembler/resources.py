import logging
from typing import Optional

from tonguetwister.disassembler.chunks.resource_key_table import ResourceKeyTable
from tonguetwister.disassembler.chunk import Chunk
from tonguetwister.disassembler.chunks.director_config import DirectorConfig
from tonguetwister.disassembler.errors import ChunkNotFound
from tonguetwister.disassembler.chunks.initial_map import InitialMap
from tonguetwister.disassembler.chunks.memory_map import MemoryMapEntry, MemoryMap

logger = logging.getLogger('tonguetwister.file_disassembler.resources')
logger.setLevel(logging.DEBUG)


class Resource:
    def __init__(self,
                 resource_id: int,
                 active: bool,
                 chunk_address: Optional[int] = None,
                 chunk: Optional[Chunk] = None):
        self.resource_id = resource_id
        self.chunk = chunk
        self.chunk_address = chunk_address
        self.active = active

    @classmethod
    def from_memory_map_entry(cls, entry: MemoryMapEntry, chunk: Optional[Chunk] = None):
        return cls(entry.index, entry.is_active(), entry.address, chunk)

    @classmethod
    def from_chunk(cls, chunk: Chunk, resource_id: int, address: int):
        return cls(resource_id, True, address, chunk)


class ResourceCollection:
    def __init__(self):
        self._resources_by_resource_id = {}
        self._resources_by_address = {}
        self._resources_by_chunk_class = {}

    def append(self, resource: Resource):
        if resource.resource_id in self._resources_by_resource_id:
            logger.error(f'Overwriting resource id {resource.resource_id}')

        if resource.chunk_address in self._resources_by_address:
            logger.error(f'Overwriting address {resource.chunk_address}')

        if resource.chunk.__class__.__name__ in self._resources_by_chunk_class:
            logger.warning(f'Overwriting class {resource.chunk.__class__.__name__}')

        self._resources_by_resource_id[resource.resource_id] = resource
        self._resources_by_address[resource.chunk_address] = resource
        self._resources_by_chunk_class[resource.chunk.__class__.__name__] = resource

    def find_by_resource_id(self, resource_id: int) -> Optional[Resource]:
        if resource_id not in self._resources_by_resource_id:
            return None

        return self._resources_by_resource_id[resource_id]

    def find_by_address(self, address: int) -> Optional[Resource]:
        if address not in self._resources_by_address:
            return None

        return self._resources_by_address[address]

    def find_by_chunk_class(self, chunk_class: Chunk.__class__) -> Optional[Resource]:
        return self._resources_by_chunk_class[chunk_class.__name__]

    def _get_chunk(self, chunk_class: Chunk.__class__):
        resource = self.find_by_chunk_class(chunk_class)
        if resource is None or not isinstance(resource.chunk, chunk_class):
            raise ChunkNotFound(chunk_class)

        return resource.chunk

    def get_memory_map_chunk(self) -> MemoryMap:
        return self._get_chunk(MemoryMap)

    def get_initial_map_chunk(self) -> InitialMap:
        return self._get_chunk(InitialMap)

    def get_resource_key_table_chunk(self) -> ResourceKeyTable:
        return self._get_chunk(ResourceKeyTable)

    def get_director_config_chunk(self) -> DirectorConfig:
        return self._get_chunk(DirectorConfig)

    def all(self):
        return self._resources_by_address.values()
