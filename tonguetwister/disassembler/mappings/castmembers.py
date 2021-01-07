class CastMemberTypeMapping:
    @staticmethod
    def get():
        # Avoid circular import
        from tonguetwister.disassembler.chunks.castmembers.bitmap import BitmapCastMember
        from tonguetwister.disassembler.chunks.castmembers.field import FieldCastMember
        from tonguetwister.disassembler.chunks.castmembers.script import ScriptCastMember
        from tonguetwister.disassembler.chunks.castmembers.shape import ShapeCastMember

        return [
            None,
            BitmapCastMember,
            None,
            FieldCastMember,
            None,
            None,
            None,
            None,
            ShapeCastMember,
            None,
            None,
            ScriptCastMember,
            None,
            None,
            None,
            None,
            None,
            None,
            None
        ]
