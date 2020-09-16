from tonguetwister.chunks.castmembers.core import SpecificCastMember
from tonguetwister.data.palettes import *


class PaletteCastMember(SpecificCastMember):
    PREDEFINED_PALETTES = {
        (8, 0): ('Macintosh system', PALETTE_MAC),
        (8, -1): ('Rainbow', PALETTE_RAINBOW),
        (8, -2): ('Grayscale', PALETTE_GRAYSCALE),
        (8, -3): ('Pastels', PALETTE_PASTEL),
        (8, -4): ('Vivid', PALETTE_VIVID),
        (8, -5): ('NTSC', PALETTE_NTSC),
        (8, -6): ('Metallic', PALETTE_METALLIC),
        (4, -7): ('VGA', None),  # Only for 4-bit color depth
        (8, -100): ('Windows system (<= Director 4)', PALETTE_WINDOWS_PRE_5),
        (8, -101): ('Windows system (>= Director 5)', PALETTE_WINDOWS_POST_4),
        (8, -8): ('Web 216 (Director 7)', None),
    }

    @staticmethod
    def get_predefined_palette(bit_depth, palette_id):
        if (bit_depth, palette_id) in PaletteCastMember.PREDEFINED_PALETTES:
            return PaletteCastMember.PREDEFINED_PALETTES[(bit_depth, palette_id)][1]
        else:
            print(f'WARNING: No predefined palette for (bit depth: {bit_depth}, palette id: {palette_id})')
            raise PALETTE_WINDOWS_POST_4

    @staticmethod
    def get_predefined_palette_name(bit_depth, palette_id):
        if (bit_depth, palette_id) in PaletteCastMember.PREDEFINED_PALETTES:
            return PaletteCastMember.PREDEFINED_PALETTES[(bit_depth, palette_id)][0]

        return f'Unknown palette (bit depth: {bit_depth}, palette id: {palette_id})'
