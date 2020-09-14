from collections import OrderedDict

from tonguetwister.chunks.castmembers.core import SpecificCastMember
from tonguetwister.chunks.castmembers.palette import PaletteCastMember
from tonguetwister.lib.byte_block_io import ByteBlockIO
from tonguetwister.lib.helper import assert_data_value


class BitmapCastMember(SpecificCastMember):
    @classmethod
    def _parse_member_data(cls, stream: ByteBlockIO, length):
        if length == 0:
            return None

        data = OrderedDict()

        # These are assumed to be skips
        data['skip_length'] = stream.uint32()
        n_skip_reads = int(data['skip_length'] / 4) - 1  # Subtract 1 for self
        for i in range(n_skip_reads):
            data[f'skip_{i}'] = stream.uint32()

        # Real data
        data['n_props'] = stream.uint16()

        prop_lengths = [stream.uint32() for _ in range(data['n_props'] + 1)]  # We compute x[i+1] - x[i], thus +1 values
        for i, prop_length in enumerate(prop_lengths[:-1]):
            data[f'prop_{i}_length'] = prop_lengths[i+1] - prop_length

        for i, prop_length in enumerate(prop_lengths[:-1]):  # New loop
            real_prop_length = prop_lengths[i + 1] - prop_length

            if i == 1:  # Cast Member name
                data[f'prop_{i}_data_member_name'] = stream.string_auto()
            elif i == 2:
                data[f'prop_{i}_data_ext_path'] = stream.string_auto()
            elif i == 3:
                data[f'prop_{i}_data_ext_filename'] = stream.string_auto()
            elif i == 16:
                data[f'prop_{i}_data_ext_formatname'] = stream.string_auto()
            else:
                data[f'prop_{i}_data'] = value = stream.read_bytes(real_prop_length); assert_data_value(value, b'')

        return data

    @classmethod
    def _parse_member_footer(cls, stream: ByteBlockIO, length):
        if length == 0:
            return None

        data = OrderedDict()

        data['?width'] = stream.uint16() & 0x7fff  # What are we doing here? Also, this seems to be wrong..
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
        data['?import_options'] = stream.uint8(); assert_data_value(data['?import_options'], [0, 8])  # 8 = dither
        data['bit_depth'] = stream.uint8()
        data['?use_cast_palette'] = stream.int16();  assert_data_value(data['?use_cast_palette'], [-1, 0])
        # Above: -1 if first cast? otherwise 0?
        data['palette'] = stream.int16()  # Refers to default palette if bit depth < 0, otherwise a cast member
        data['+palette_name'] = PaletteCastMember.get_palette_name(data['bit_depth'], data['palette'])

        return data
