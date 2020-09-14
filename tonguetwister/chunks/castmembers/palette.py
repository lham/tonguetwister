from tonguetwister.chunks.castmembers.core import SpecificCastMember


class PaletteCastMember(SpecificCastMember):
    DEFAULT_PALETTES = {
        (8, -1): 'Macintosh system',
        (8, -2): 'Rainbow',
        (8, -3): 'Grayscale',
        (8, -4): 'Pastels',
        (8, -5): 'Vivid',
        (8, -6): 'NTSC',
        (8, -7): 'Metallic',
        (4, -8): 'VGA',  # Only for 4-bit color depth
        (8, -101): 'Windows system (<= Director 4)',
        (8, -102): 'Windows system (>= Director 5)',
        (8, -8): 'Web 216 (Director 7)'
    }

    @staticmethod
    def get_palette_name(bit_depth, palette_value):
        if palette_value >= 0:
            return f'Palette cast member #{palette_value}'

        if (bit_depth, palette_value) in PaletteCastMember.DEFAULT_PALETTES:
            return PaletteCastMember.DEFAULT_PALETTES[(bit_depth, palette_value)]

        return f'Unknown palette (bit depth: {bit_depth}, palette id: {palette_value})'

