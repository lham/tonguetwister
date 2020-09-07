from kivy.uix.textinput import TextInput

from tonguetwister.chunks.cast_member import CastMember
from tonguetwister.chunks.castmembers.field import FieldCastMember
from tonguetwister.chunks.castmembers.script import ScriptCastMember
from tonguetwister.chunks.castmembers.shape import ShapeCastMember
from tonguetwister.lib.helper import splat_ordered_dict


# noinspection PyMethodMayBeStatic,PyProtectedMember
class CastMemberView(TextInput):
    def __init__(self, parser_results, **kwargs):
        super().__init__(**kwargs)
        self.parser_results = parser_results

    def load(self, cast_member):
        self.text = (
            f'Media type: {CastMember.MEDIA_TYPES[cast_member.media_type]}\n\n'
            + self._set_member_text(cast_member.member)
        )

    def _set_member_text(self, member):
        if isinstance(member, ScriptCastMember):
            return self._set_script_member_text(member)
        elif isinstance(member, FieldCastMember):
            return self._set_field_member_text(member)
        elif isinstance(member, ShapeCastMember):
            return self._set_shape_member_text(member)
        else:
            return ''

    def _set_script_member_text(self, member):
        return (
            f'Data:\n\n    '
            + (splat_ordered_dict(member.body, '\n    ', 14) if len(member.body) > 0 else 'None')
            + f'\n\nFooter:\n\n    '
            + (splat_ordered_dict(member.footer, '\n    ', 14) if len(member.footer) > 0 else 'None')
        )

    def _set_field_member_text(self, member):
        return self._set_script_member_text(member)

    def _set_shape_member_text(self, member):
        return self._set_script_member_text(member)
