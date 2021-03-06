from tonguetwister.disassembler.chunks.bitmap_data import BitmapData
from tonguetwister.disassembler.chunks.cast_member import CastMember
from tonguetwister.disassembler.chunks.castmembers.palette import PaletteCastMember
from tonguetwister.lib.stream import ByteBlockIO
from tonguetwister.lib.helper import assert_data_value


class BitmapCastMember(CastMember):
    @classmethod
    def _parse_member_data(cls, stream: ByteBlockIO, length):
        if length == 0:
            return None

        data = {}

        # These are assumed to be skips / reserved
        data['skip_length'] = stream.uint32()
        n_skip_reads = int(data['skip_length'] / 4) - 1  # Subtract 1 for self
        for i in range(n_skip_reads):
            data[f'skip_{i}'] = stream.uint32()

        # Real data
        data['n_props'] = stream.uint16()

        prop_lengths = [stream.uint32() for _ in range(data['n_props'] + 1)]  # We will x[i+1] - x[i], thus 1 extra val

        # Iterate to save the lengths
        for i, prop_length in enumerate(prop_lengths[:-1]):
            data[f'prop_{i}_length'] = prop_lengths[i + 1] - prop_length

        # Iterate again to save the data
        for i, prop_length in enumerate(prop_lengths[:-1]):
            real_prop_length = prop_lengths[i + 1] - prop_length

            if real_prop_length == 0:
                data[f'prop_{i}_data'] = b''
            elif i == 1:
                data[f'prop_{i}_data_member_name'] = stream.string_auto()
            elif i == 2:
                data[f'prop_{i}_data_ext_path'] = stream.string_auto()
            elif i == 3:
                data[f'prop_{i}_data_ext_filename'] = stream.string_auto()
            elif i == 16:
                data[f'prop_{i}_data_ext_formatname'] = stream.string_auto()
            else:
                data[f'prop_{i}_data'] = value = stream.read_bytes(real_prop_length); #assert_data_value(value, b'')

        return data

    @classmethod
    def _parse_member_footer(cls, stream: ByteBlockIO, length):
        if length == 0:
            return None

        data = {}

        data['bytes_per_image_row'] = stream.uint16() & 0x7fff  # Why are we using this mask?
        data['top'] = stream.int16()
        data['left'] = stream.int16()
        data['bottom'] = stream.int16()
        data['right'] = stream.int16()
        data['u1'] = stream.uint8(); assert_data_value(data['u1'], 0)
        data['u2'] = stream.uint8(); assert_data_value(data['u2'], 0)
        data['?number_of_image_ops'] = stream.uint16(ByteBlockIO.LITTLE_ENDIAN)  # Not a 1-1 mapping of ops done?
        data['paint_window_offset_y'] = stream.int16(ByteBlockIO.LITTLE_ENDIAN)
        data['paint_window_offset_x'] = stream.int16(ByteBlockIO.LITTLE_ENDIAN)
        data['registration_point_y'] = stream.int16()
        data['registration_point_x'] = stream.int16()

        if stream.is_depleted():
            # This happens if it's a 1-bit bitmap, set the values manually
            data['?import_options'] = 0
            data['bit_depth'] = 1
            data['?use_cast_palette'] = -1
            data['palette'] = None
        else:
            data['?import_options'] = stream.uint8(); assert_data_value(data['?import_options'], [0, 8])  # 8 = dither
            data['bit_depth'] = stream.uint8()
            data['?use_cast_palette'] = stream.int16();  assert_data_value(data['?use_cast_palette'], [-1, 0])
            # Above: -1 if first cast? otherwise 0?
            data['palette'] = stream.int16()  # Refers to predefined palette < 0, otherwise a cast member

        return data

    @property
    def name(self):
        return self._body['prop_1_data_member_name']

    @property
    def is_linked(self):
        return 'prop_2_data_ext_path' in self._body and len(self._body['prop_2_data_ext_path']) > 0

    @property
    def external_file(self):
        if not self.is_linked:
            return ''

        # TODO: The path separator must depend on os version somehow
        return f"{self._body['prop_2_data_ext_path']}\\{self._body['prop_3_data_ext_filename']}"

    @property
    def width(self):
        return self._footer['right'] - self._footer['left']

    @property
    def height(self):
        return self._footer['bottom'] - self._footer['top']

    @property
    def bit_depth(self):
        return self._footer['bit_depth']

    @property
    def palette(self):
        if self.bit_depth > 8:
            return None

        if self._footer['?use_cast_palette'] >= 0:
            print('Warning: Cast palette not implemented, using a predefined palette')

        return PaletteCastMember.get_predefined_palette(self.bit_depth, self._footer['palette'])

    @property
    def palette_name(self):
        if self.bit_depth > 8:
            return 'None'
        elif self._footer['?use_cast_palette'] < 0:
            return PaletteCastMember.get_predefined_palette_name(self.bit_depth, self._footer['palette'])
        else:
            return 'Unable to parse palette cast member name'

    def image_data(self, bitmap_data_chunk: BitmapData):
        if not isinstance(bitmap_data_chunk, BitmapData):
            print('Warning: Trying to load image data of a chunk that is not BitmapData')
            return []

        return bitmap_data_chunk.unpack(
            self.width,
            self.height,
            self.bit_depth,
            self._footer['bytes_per_image_row'],
            self.palette
        )
