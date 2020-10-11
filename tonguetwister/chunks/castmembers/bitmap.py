from collections import OrderedDict

from tonguetwister.chunks.bitmap_data import BitmapData
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
        data['?import_options'] = stream.uint8(); assert_data_value(data['?import_options'], [0, 8])  # 8 = dither
        data['bit_depth'] = stream.uint8()
        data['?use_cast_palette'] = stream.int16();  assert_data_value(data['?use_cast_palette'], [-1, 0])
        # Above: -1 if first cast? otherwise 0?
        data['palette'] = stream.int16()  # Refers to default palette if bit depth < 0, otherwise a cast member

        return data

    @property
    def name(self):
        return self.body['prop_1_data_member_name']

    @property
    def width(self):
        return self.footer['right'] - self.footer['left']

    @property
    def height(self):
        return self.footer['bottom'] - self.footer['top']

    @property
    def bit_depth(self):
        return self.footer['bit_depth']

    @property
    def palette(self):
        return PaletteCastMember.get_predefined_palette(self.bit_depth, self.footer['palette'])

    @property
    def palette_name(self):
        if self.footer['?use_cast_palette'] < 0:
            return PaletteCastMember.get_predefined_palette_name(self.bit_depth, self.footer['palette'])
        else:
            return 'Unable to parse palette cast member name'

    def has_alpha_channel(self):
        return self.bit_depth == 32  # TODO: This is probably true for 16-bit as well?

    def image_data(self, bitmap_data: BitmapData):
        if self.bit_depth == 32:
            image_data = bitmap_data.decode_32bit_rle_data(self.width, self.height)
        elif self.bit_depth == 16:
            raise RuntimeError('16-bit bitmaps not implemented yet')
        elif self.bit_depth == 8:
            image_data = bitmap_data.decode_8bit_rle_data(self.palette)
        elif self.bit_depth == 4:
            raise RuntimeError('4-bit bitmaps not implemented yet')
        elif self.bit_depth == 2:
            raise RuntimeError('2-bit bitmaps not implemented yet')
        else:
            raise RuntimeError(f'{self.bit_depth} is an invalid bit depth')

        return self._reorder_image_data(image_data)

    def _reorder_image_data(self, image_data):
        # Bitmaps are read from bottom-row to top-row. We thus need to swap the positions of all rows
        # https://medium.com/sysf/bits-to-bitmaps-a-simple-walkthrough-of-bmp-image-format-765dc6857393
        for i in range(int(self.height / 2)):
            lower_start = self.width * i
            lower_stop = self.width * (i + 1)
            upper_start = self.width * (self.height - i - 1)
            upper_stop = self.width * (self.height - i)

            row_lower = image_data[lower_start:lower_stop]
            row_upper = image_data[upper_start:upper_stop]

            image_data[lower_start:lower_stop] = row_upper
            image_data[upper_start:upper_stop] = row_lower

        # Flatten the array of color tuples to construct a byte array
        return bytes([color_byte for rgb_tuple in image_data for color_byte in rgb_tuple])
