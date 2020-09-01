from collections import OrderedDict

from tonguetwister.lib.helper import splat_ordered_dict


class IdealizedMap:
    def __init__(self, stream):
        self._imap = OrderedDict()
        self._imap['u1'] = stream.uint32()
        self._imap['mmap_address'] = stream.uint32()
        self._imap['u2'] = stream.uint32()
        self._imap['u3'] = stream.uint32()
        self._imap['u4'] = stream.uint32()
        self._imap['u5'] = stream.uint32()

    @property
    def mapping(self):
        return self._imap

    def __repr__(self):
        return splat_ordered_dict(self.mapping)
