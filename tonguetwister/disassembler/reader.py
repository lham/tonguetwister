import logging

from tonguetwister.disassembler.chunk import UndefinedChunk, Chunk
from tonguetwister.disassembler.errors import UnexpectedChunkClass
from tonguetwister.disassembler.mappings.four_cc import CHUNK_MAP
from tonguetwister.lib.byte_block_io import ByteBlockIO

logger = logging.getLogger('tonguetwister.file_disassembler.reader')
logger.setLevel(logging.DEBUG)


def extract_chunk(stream: ByteBlockIO,
                  address: int,
                  expected_chunk_class: Chunk.__class__ = None,
                  ignore_parse_check: bool = False) -> Chunk:
    four_cc, data_address, data = _extract_chunk_data(stream, address)
    chunk_stream = ByteBlockIO(data)
    chunk = _parse_chunk(four_cc, address, chunk_stream)

    if expected_chunk_class is not None and not isinstance(chunk, expected_chunk_class):
        raise UnexpectedChunkClass(chunk, expected_chunk_class)

    if not ignore_parse_check and not chunk_stream.is_depleted():
        logger.warning(f'{four_cc}: Unprocessed data remains for stream:\n'
                       f'{chunk_stream.get_processed_bytes_string()}\n'
                       f'{chunk_stream.get_unprocessed_bytes_array()}')
        raise RuntimeError()

    return chunk


def _extract_chunk_data(stream: ByteBlockIO, position: int) -> (str, int, bytes):
    stream.seek(position)

    four_cc = stream.string_raw(4)
    chunk_length = stream.uint32()
    chunk_data_address = stream.tell()
    chunk_data = stream.read_bytes(chunk_length)

    _strip_padding_from_uneven_chunk(stream, chunk_length, four_cc, chunk_data_address)

    return four_cc, chunk_data_address, chunk_data


def _parse_chunk(four_cc: str, address: int, stream: ByteBlockIO) -> Chunk:
    if four_cc in CHUNK_MAP:
        return CHUNK_MAP[four_cc].parse(stream, address, four_cc)

    logger.warning(f'Could not find a mapping for the four_cc "{four_cc}"')

    return UndefinedChunk.parse(stream, address, four_cc)


def _strip_padding_from_uneven_chunk(stream: ByteBlockIO, chunk_length: int, four_cc: str, address: int):
    # TODO: When should we strip padding?
    if chunk_length % 2 != 0:
        padding = stream.uint8()
        # if padding != 0:
        #    raise RuntimeError(f'Padding is non-zero for {four_cc} at {address}')
