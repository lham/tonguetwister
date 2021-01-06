from collections import OrderedDict

from tonguetwister.disassembler.chunk import Chunk
from tonguetwister.lib.byte_block_io import ByteBlockIO
from tonguetwister.lib.helper import grouper, twos_complement, flatten, chunk


class BitmapData(Chunk):
    DEFAULT_ALPHA = 255

    @classmethod
    def _parse_body(cls, stream: ByteBlockIO, header):
        data = OrderedDict()
        data['run_length_encoded_data'] = stream.read_bytes()
        data['byte_string'] = grouper(data['run_length_encoded_data'], 2)  # A formatted byte list for debug purposes

        return data

    def unpack(self, width, height, bit_depth, bytes_per_row, palette):
        """
        Unpack the color data saved in this chunk.
        """
        stream = ByteBlockIO(self.body['run_length_encoded_data'])

        return self.unpack_bitmap_data(stream, width, height, bit_depth, bytes_per_row, palette)

    @staticmethod
    def unpack_bitmap_data(stream, width, height, bit_depth, bytes_per_row, palette):
        """
        NB! This class/method is optimized for readability, not speed. Thus we do stuff like converting the four color
        bytes for a 32-bit image into a 32-bit word and the masking the colors back out (instead of just using the
        color bytes directly)
        """
        is_encoded = (stream.size() != bytes_per_row * height)

        words = []
        for _ in range(height):
            byte_list = BitmapData._read_row_byte_list(stream, is_encoded, bytes_per_row, bit_depth)
            words.extend(BitmapData._convert_byte_list_to_words(byte_list, width, bit_depth))

        if not stream.is_depleted():
            raise RuntimeError('Bitmap image decoder failed to parse image - there are unprocessed bytes remaining')

        return BitmapData._flip_image_rows(
            [BitmapData._convert_word_to_32bit_argb_tuples(word, palette, bit_depth) for word in words],
            width,
            height
        )

    @staticmethod
    def _read_row_byte_list(stream, is_encoded, bytes_per_row, bit_depth):
        if not is_encoded:
            return [stream.uint8() for _ in range(bytes_per_row)]

        # Unpack the next byte sequence according to the PackBits algorithm.
        # See https://en.wikipedia.org/wiki/PackBits
        byte_list = []
        while len(byte_list) < bytes_per_row:
            header_byte = stream.uint8()

            if header_byte < 0x80:
                length = header_byte + 1
                byte_list.extend([stream.uint8() for _ in range(length)])
            else:
                length = twos_complement(header_byte) + 1
                byte = stream.uint8()
                byte_list.extend([byte] * length)

        return BitmapData._reshape_decoded_byte_row(byte_list, bytes_per_row, bit_depth)

    @staticmethod
    def _reshape_decoded_byte_row(byte_list, bytes_per_row, bit_depth):
        if bit_depth == 32:
            return flatten(zip(*chunk(byte_list, bytes_per_row // 4)))
        elif bit_depth == 16:
            return flatten(zip(*chunk(byte_list, bytes_per_row // 2)))
        else:
            return byte_list

    @staticmethod
    def _convert_byte_list_to_words(byte_list, width, bit_depth):
        if bit_depth == 32:
            words = [ByteBlockIO.bytes_to_32bit_word(_bytes, ByteBlockIO.BIG_ENDIAN) for _bytes in chunk(byte_list, 4)]
        elif bit_depth == 16:
            words = [ByteBlockIO.bytes_to_16bit_word(_bytes, ByteBlockIO.BIG_ENDIAN) for _bytes in chunk(byte_list, 2)]
        else:
            words = flatten([BitmapData._convert_byte_to_sub_8bit_words(byte, bit_depth) for byte in byte_list])

        return words[:width]

    @staticmethod
    def _convert_byte_to_sub_8bit_words(byte, bit_depth):
        """
        Convert a byte into multiple 8, 4, 2, or 1-bit words depending on the bit depth.

        A byte 'x' has 8 bits as:

                0 1 2 3 4 5 6 7
            x = 0 1 2 3 4 5 6 7

        So for the different bit depths we are looking for the words made up of the follow bit indices:

            bit depth 1: [[0], [1], [2], [3], [4], [5], [6], [7]]
            bit depth 2: [[0, 1], [2, 3], [4, 5], [6, 7]]
            bit depth 4: [[0, 1, 2, 3], [4, 5, 6, 7]]
            bit depth 8: [[0, 1, 2, 3, 4, 5, 6, 7]]

        We can do this by first left-shifting to the index we want and then apply a mask to get the number of bits we
        want to extract. This becomes

            bit depth 1: [x << 7 & 0b00000001, x << 6 & 0b00000001, x << 5 & 0b00000001, x << 4 & 0b00000001,
                          x << 3 & 0b00000001, x << 2 & 0b00000001, x << 1 & 0b00000001, x << 0 & 0b00000001]
            bit depth 2: [x << 6 & 0b00000011, x << 4 & 0b00000011, x << 2 & 0b00000011, x << 0 & 0b00000011]
            bit depth 4: [x << 4 & 0b00001111, x << 0 & 0b00001111]
            bit depth 8: [x << 0 & 0b11111111]
        """
        n_bits = 2 ** bit_depth - 1
        n_words = 8 // bit_depth - 1

        return [(byte >> (i * bit_depth)) & n_bits for i in range(n_words, -1, -1)]

    @staticmethod
    def _convert_word_to_32bit_argb_tuples(word, palette, bit_depth):
        if bit_depth == 32:
            _, r, g, b = BitmapData._convert_32bit_word_to_32bit_argb(word)  # Ignore alpha, see below
        elif bit_depth == 16:
            r, g, b = BitmapData._convert_16bit_word_to_24bit_rgb(word)
        else:
            r, g, b = palette[word]

        # Director 6 doesn't seem to support an alpha value, but encodes a zero byte anyway. So we replace it with
        # the a default alpha instead
        return BitmapData.DEFAULT_ALPHA, r, g, b

    @staticmethod
    def _convert_16bit_word_to_24bit_rgb(word):
        """
        Convert a 16-bit word / uint16() to a (red, green, blue) tuple with 8 bits per channel.

        The 16 bit colors in Director are stored as three channels with 5 bits for each color. The leftmost byte is
        ignored. So the channels are ordered as (red, green, blue) with the bits of the 16-bit word 'x' being:

                0 1 2 3 4 5 6 7 8 9 a b c e d e
            x = _ r r r r r g g g g g b b b b b

        First recover each channel by using an appropriate mask and right-shift the value to get the 5-bit value:

            r = (x & 0x7c00) >> 10                              mask: 0b0111110000000000
            g = (x & 0x03e0) >>  5                              mask: 0b0000001111100000
            b = (x & 0x001f) >>  0                              mask: 0b0000000000011111

        To convert this to an 8-bit color value we append the middle 3 bits the 5-bit value to the end of said 5-bit
        value. The 3-bit value can be obtained in the same way as above, by masking and the right-shifting the 5-bit
        channel value. To append it we first left-shift the 5-bit value then doing a bitwise-or with the 3-bit value:

            r = (r << 3) | ((r & 0xf) >> 1)                     mask: 0b01110
            g = (g << 3) | ((g & 0xf) >> 1)                     mask: 0b01110
            b = (b << 3) | ((b & 0xf) >> 1)                     mask: 0b01110

        And then we got our 24-bit RGB tuple! However, we can simply these expressions to only use correct values
        directly from the original 16-bit word 'x'. Expanding the expressions above we get:

            r = (((x & 0x7c00) >> 10) << 3) | ((((x & 0x7c00) >> 10) & 0xf) >> 1)
            g = (((x & 0x03e0) >>  5) << 3) | ((((x & 0x03e0) >>  5) & 0xf) >> 1)
            b = (((x & 0x001f) >>  0) << 3) | ((((x & 0x001f) >>  0) & 0xf) >> 1)

        For the left-hand side of the bitwise-or we can just merge the shit operations and for the right-hand hand side
        we change the mask so that we pick the 3 correct bits directly for each channel and then just right-shift them
        into position. The bits would be ([2, 3, 4], [7, 8, 9], [c, e, d]) using the table above:

            r = ((x & 0x7c00) >> 7) | ((x & 0x3800) >> 11)      RHS-mask: 0b0011100000000000
            g = ((x & 0x03e0) >> 2) | ((x & 0x01c0) >> 6)       RHS-mask: 0b0000000111000000
            b = ((x & 0x001f) << 3) | ((x & 0x000e) >> 1)       RHS-mask: 0b0000000000001110
        """
        return (
            ((word & 0x7c00) >> 7) | ((word & 0x3800) >> 11),
            ((word & 0x03e0) >> 2) | ((word & 0x01c0) >> 6),
            ((word & 0x001f) << 3) | ((word & 0x000e) >> 1)
        )

    @staticmethod
    def _convert_32bit_word_to_32bit_argb(word):
        """
        Convert a 32-bit word / uint32() to a (alpha, red, green, blue) tuple with 8 bits per channel.

        This assumes 8 bits per channel with the channels ordered a, r, g, b from left to right. Simply mask 8 bits at a
        time and then right-shift them to get the channel value.
        """
        return (
            ((word & 0xff000000) >> 24),
            ((word & 0x00ff0000) >> 16),
            ((word & 0x0000ff00) >> 8),
            ((word & 0x000000ff) >> 0)
        )

    @staticmethod
    def _flip_image_rows(image_data, width, height):
        """
        Flip the rows so that the last row becomes the first row, second row becomes the second-to-last, and so on.

        This is done because bitmaps are read from bottom-row to top-row. See
        https://medium.com/sysf/bits-to-bitmaps-a-simple-walkthrough-of-bmp-image-format-765dc6857393 for more
        information.
        """
        for i in range(height // 2):
            lower_start = width * i
            lower_stop = width * (i + 1)
            upper_start = width * (height - i - 1)
            upper_stop = width * (height - i)

            row_lower = image_data[lower_start:lower_stop]
            row_upper = image_data[upper_start:upper_stop]

            image_data[lower_start:lower_stop] = row_upper
            image_data[upper_start:upper_stop] = row_lower

        return image_data
