from tonguetwister.disassembler.chunks.cast_member import CastMember
from tonguetwister.data.palettes import *


class PaletteCastMember(CastMember):
    PREDEFINED_PALETTES = {
        (1, None): ('Binary', PALETTE_1_BIT_BINARY),
        (2, 0): ('System - Mac', PALETTE_2_BIT_MAC),
        (4, 0): ('System - Mac', PALETTE_4_BIT_MAC),
        (8, 0): ('System - Mac', PALETTE_8_BIT_MAC),
        (4, -1): ('Rainbow', PALETTE_4_BIT_RAINBOW),
        (8, -1): ('Rainbow', PALETTE_8_BIT_RAINBOW),
        (4, -2): ('Grayscale', PALETTE_4_BIT_GRAYSCALE),
        (8, -2): ('Grayscale', PALETTE_8_BIT_GRAYSCALE),
        (4, -3): ('Pastels', PALETTE_4_BIT_PASTELS),
        (8, -3): ('Pastels', PALETTE_8_BIT_PASTELS),
        (4, -4): ('Vivid', PALETTE_4_BIT_VIVID),
        (8, -4): ('Vivid', PALETTE_8_BIT_VIVID),
        (4, -5): ('NTSC', PALETTE_4_BIT_NTSC),
        (8, -5): ('NTSC', PALETTE_8_BIT_NTSC),
        (8, -6): ('Metallic', PALETTE_8_BIT_METALLIC),  # Only for 8-bit color depth
        (4, -7): ('VGA', PALETTE_4_BIT_VGA),  # Only for 4-bit color depth
        (4, -100): ('System - Win (Dir 4)', PALETTE_4_BIT_WIN_DIR4),
        (8, -100): ('System - Win (Dir 4)', PALETTE_8_BIT_WIN_DIR4),
        (2, -101): ('System - Win', PALETTE_2_BIT_WIN),
        (4, -101): ('System - Win', PALETTE_4_BIT_WIN),
        (8, -101): ('System - Win', PALETTE_8_BIT_WIN)
    }

    @staticmethod
    def get_predefined_palette(bit_depth, palette_id):
        if (bit_depth, palette_id) in PaletteCastMember.PREDEFINED_PALETTES:
            return PaletteCastMember.PREDEFINED_PALETTES[(bit_depth, palette_id)][1]
        else:
            print(f'WARNING: No predefined palette for (bit depth: {bit_depth}, palette id: {palette_id})')
            return PALETTE_8_BIT_WIN

    @staticmethod
    def get_predefined_palette_name(bit_depth, palette_id):
        if (bit_depth, palette_id) in PaletteCastMember.PREDEFINED_PALETTES:
            return PaletteCastMember.PREDEFINED_PALETTES[(bit_depth, palette_id)][0]
        else:
            print(f'WARNING: No predefined palette for (bit depth: {bit_depth}, palette id: {palette_id})')
            return f'Invalid palette (bit depth: {bit_depth}, palette id: {palette_id})'
