import logging
from collections import OrderedDict

from tonguetwister.chunks.chunk import Chunk
from tonguetwister.data.inks import INKS
from tonguetwister.lib.byte_block_io import ByteBlockIO
from tonguetwister.lib.helper import grouper, chunk, assert_data_value
from tonguetwister.lib.logger import log_expected_trailing_bytes
from tonguetwister.lib.property_reader import PropertyReader, property_reader

logger = logging.getLogger('tonguetwister.VWSC_Score')
logger.setLevel(logging.INFO)


class ScorePropertyReader(PropertyReader):
    @property_reader(0)
    def frame_data(self, stream):
        data = OrderedDict()
        data['block_length'] = stream.int32()
        data['header_length'] = stream.int32()
        data['u1'] = stream.int32()
        data['u2'] = stream.int16()
        data['bytes_per_sprite'] = stream.int16()
        data['n_channels'] = stream.int16()
        data['u3'] = stream.int16()

        # This is a list of frames. Each frame contains a dict of what changes occurred since the last frame (and where)
        data['frames'] = frames = []

        next_frame_address = data['header_length']
        while stream.tell() < data['block_length']:
            frame = {}
            frame_length = stream.uint16()
            logger.debug(f'Frame {len(frames):3d}: -> 0x{frame_length:04x}')
            next_frame_address += frame_length

            while stream.tell() != next_frame_address:
                change_length = stream.uint16()
                change_addr = stream.uint16()
                frame[change_addr] = stream.read_bytes(change_length)
                logger.debug(
                    f'             '
                    f'{change_length:4d} bytes at 0x{change_addr:04x} ({change_addr:4d}): '
                    f'{grouper(frame[change_addr], 4)}'
                )

            frames.append(frame)

        if not stream.is_depleted():
            _bytes = stream.read_bytes()
            log_expected_trailing_bytes(logger, _bytes, 'FrameData')

        return data, False

    @property_reader(1)
    def sprite_order_data(self, stream):
        data = OrderedDict()
        data['n_sprites'] = stream.uint32()

        sprite_indices = [stream.uint32() for _ in range(data['n_sprites'])]
        data['offset_indices_in_order_of_appearance'] = sprite_indices

        # Define a reader for each sprite span index
        for sprite_index in sprite_indices:
            self.register(sprite_index, f'sprite_span_{sprite_index}', self.sprite_span)

        return data, False

    @staticmethod
    def sprite_span(stream):
        props = OrderedDict()
        props['frame_start'] = stream.uint32()
        props['frame_end'] = stream.uint32()
        props['u1'] = stream.uint32()
        props['u2'] = stream.uint32()
        props['channel'] = stream.uint32()
        props['u3'] = stream.int32()
        props['u4'] = stream.int32()
        props['u5'] = stream.uint32()
        props['u6'] = stream.uint32()
        props['u7'] = stream.uint32()
        props['u8'] = stream.uint32()

        i = 0
        while not stream.is_depleted():
            props[f'keyframe_{i}'] = stream.int32()
            i += 1

        return props, False


class VideoWorksScore(Chunk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.sprite_span_store = {}
        self.sprite_store = {}
        self.notation = {}

        self._generate_sprite_spans()
        self._generate_notation()

    @classmethod
    def _parse_header(cls, stream: ByteBlockIO):
        header = OrderedDict()

        header['chunk_length'] = stream.uint32()
        header['u1'] = stream.int32()  # Always 0xfffffffd / (-3)
        header['header_length'] = stream.uint32()  # Always 12 ?
        header['count1'] = stream.uint32()
        header['count2'] = stream.uint32()
        header['u2'] = stream.uint32()

        header.update(stream.auto_property_list(
            ScorePropertyReader,
            header['header_length'] + 12,  # 4 bytes for each of: [chunk_length, u2, header_length]
            header['count2']
        ))

        header['remaining_data'] = stream.read_bytes()
        header['remaining_data-bytes'] = grouper(header['remaining_data'], 4)

        if len(header['remaining_data']) > 0:
            logger.warning(f'Unprocessed data remaining ({len(header["remaining_data"])} bytes)')

        return header

    @staticmethod
    def _parse_sprite_data(byte_string):
        stream = ByteBlockIO(byte_string, ByteBlockIO.BIG_ENDIAN)

        data = OrderedDict()
        data['u_all'] = grouper(byte_string, 4)
        data['u1'] = stream.int8(); assert_data_value(data['u1'], [0x10, 0x00])

        i = stream.uint8()  # The two first bits here are flags
        data['?keyframe'] = (i >> 7) & 1
        data['trails'] = (i >> 6) & 1
        data['ink_type'] = i & 0x3f

        data['u2'] = stream.uint8(); assert_data_value(data['u2'], [0x00, 0xff])  # bg?
        data['u3'] = stream.uint8(); assert_data_value(data['u3'], [0x00, 0xff])  # fg?
        data['u4'] = stream.int16(); assert_data_value(data['u4'], [0x00, 0x0001])  # sprite type?

        data['cast_member_index'] = stream.int16()

        data['u5'] = stream.int16(); assert_data_value(data['u5'], 0x0000)

        data['sprite_span_index'] = stream.int16()
        data['y'] = stream.int16()
        data['x'] = stream.int16()
        data['height'] = stream.int16()
        data['width'] = stream.int16()

        i = stream.int8()
        data['moveable'] = (i >> 7) & 1
        data['editable'] = (i >> 6) & 1

        data['blend'] = stream.uint8()

        i = stream.int8()
        data['?is_sprite_span_tail'] = (i >> 7) & 1
        data['u6a_flag'] = (i >> 6) & 1; assert_data_value(data['u6a_flag'], 0)
        data['u6b_flag'] = (i >> 5) & 1; assert_data_value(data['u6b_flag'], 0)
        data['?has_blend'] = (i >> 4) & 1
        data['u6c_value'] = i & 0xf; assert_data_value(data['u6c_value'], 0)
        data['u7'] = stream.int8(); assert_data_value(data['u7'], 0)

        return data

    def _generate_sprite_spans(self):
        for index in self.header['sprite_order_data']['offset_indices_in_order_of_appearance']:
            self.sprite_span_store[index] = SpriteSpan(self.header[f'sprite_span_{index}'])

    def _generate_notation(self):
        n_bytes_per_sprite = self.header['frame_data']['bytes_per_sprite']
        current_frame = [0] * self.number_of_bytes_per_frame

        for frame_no, frame in enumerate(self.header['frame_data']['frames']):
            for index, byte_list in frame.items():
                current_frame[index:index + len(byte_list)] = list(byte_list)

            for channel_no, sprite_byte_list in enumerate(chunk(current_frame, n_bytes_per_sprite)):
                sprite_byte_string = bytes(sprite_byte_list)
                if sprite_byte_string not in self.sprite_store:
                    self.sprite_store[sprite_byte_string] = self._read_sprite(frame_no, channel_no, sprite_byte_string)

                self.notation[(frame_no, channel_no)] = self.sprite_store[sprite_byte_string]

    def _read_sprite(self, frame_no, channel_no, data):
        if data[0] == 0:
            if not all(x == 0 for x in data):
                logger.warning(
                    f'Found an empty sprite with non-zero data '
                    f'in channel {channel_no}, frame {frame_no}: {grouper(data, 4)}'
                )

            return EmptySprite()
        elif channel_no == 0:
            return EmptySprite()
        elif channel_no == 1:
            return EmptySprite()
        elif channel_no == 2:
            return EmptySprite()
        elif channel_no == 3:
            return EmptySprite()
        elif channel_no == 4:
            return EmptySprite()
        elif channel_no == 5:
            return EmptySprite()
        else:
            return Sprite(self._parse_sprite_data(data), self.sprite_span_store)

    def sprite_at(self, frame_no, channel_no):
        return self.notation[(frame_no, channel_no)]

    @property
    def highest_channel_used(self):
        highest = 0
        for (_, channel_no), sprite in self.notation.items():
            if not isinstance(sprite, EmptySprite) and channel_no > highest:
                highest = channel_no

        return highest

    @property
    def number_of_channels(self):
        return self.header['frame_data']['n_channels']

    @property
    def number_of_frames(self):
        return len(self.header['frame_data']['frames'])

    @property
    def number_of_bytes_per_frame(self):
        return self.header['frame_data']['bytes_per_sprite'] * self.number_of_channels

    def text_representation_frames(self, offset=0, length=None, use_min_height=False):
        if length is None:
            length = self.number_of_bytes_per_frame

        output = ''
        frame_number_width = len(str(self.number_of_frames))
        byte_number_width = len(str(offset + length if not use_min_height else self.number_of_bytes_per_frame))

        # Add index numbers
        numbers = [[] for _ in range(byte_number_width)]
        for frame_no in range(offset, offset + length):
            number_string = format(frame_no, f'0{len(numbers)}d')
            for i in range(len(numbers)):
                numbers[i].append(number_string[i])

        for i in range(len(numbers)):
            output += f"{' ' * frame_number_width}   {'  '.join(numbers[i])}\n"

        # Add frame changes
        for frame_no, frame in enumerate(self.header['frame_data']['frames'], 1):
            current_frame = [None] * self.number_of_bytes_per_frame
            # Apply the current frame changes
            for index, _bytes in frame.items():
                current_frame[index:index + len(_bytes)] = list(_bytes)

            # Format the string
            byte_string = ''
            partial = []
            for byte in current_frame[offset:offset + length]:
                if byte is None:
                    if len(partial) > 0:
                        byte_string += grouper(bytes(partial), 2) + ' '
                        partial = []
                    byte_string += '   '
                else:
                    partial.append(byte)

            # Display
            frame_no_string = format(frame_no, f'0{frame_number_width}d')
            output += f'{frame_no_string}: {byte_string}\n'

        return output


class Sprite:
    def __init__(self, data, sprite_spans):
        self._data = data
        self.sprite_span = sprite_spans[data['sprite_span_index']]

    @property
    def x(self):
        return self._data['x']

    @property
    def y(self):
        return self._data['y']

    @property
    def width(self):
        return self._data['width']

    @property
    def height(self):
        return self._data['height']

    @property
    def ink(self):
        return INKS[self._data['ink_type']]  # TODO: Convert to actual ink

    @property
    def blend(self):
        return round((0xff - self._data['blend']) / 0xff, 2)

    @property
    def moveable(self):
        return self._data['moveable'] == 1

    @property
    def editable(self):
        return self._data['editable'] == 1

    @property
    def trails(self):
        return self._data['trails'] == 1

    @property
    def cast_member(self):
        return self._data['cast_member_index']  # TODO: fetch


class EmptySprite:
    sprite_span = None


class SpriteSpan:
    def __init__(self, data):
        self._data = data

    @property
    def start(self):
        return self._data['frame_start'] - 1

    @property
    def end(self):
        return self._data['frame_end'] - 1

    @property
    def channel_no(self):
        return self._data['channel']

    @property
    def keyframes(self):
        return [v for k, v in self._data.items() if k.startswith('keyframe')]
