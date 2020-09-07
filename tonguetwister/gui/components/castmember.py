from kivy.uix.textinput import TextInput

from tonguetwister.chunks.cast_member import CastMember, ScriptMember, FieldMember, ShapeMember
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
        if isinstance(member, ScriptMember):
            return self._set_script_member_text(member)
        elif isinstance(member, FieldMember):
            return self._set_field_member_text(member)
        elif isinstance(member, ShapeMember):
            return self._set_shape_member_text(member)
        else:
            return ''

    def _set_script_member_text(self, member):
        return (
            f'Data:\n\n    '
            + (splat_ordered_dict(member._data, '\n    ', 14) if len(member._data) > 0 else 'None')
            + f'\n\nFooter:\n\n    '
            + (splat_ordered_dict(member._footer, '\n    ', 14) if len(member._footer) > 0 else 'None')
        )

    def _set_field_member_text(self, member):
        return self._set_script_member_text(member)

    def _set_shape_member_text(self, member):
        return self._set_script_member_text(member)
