from collections import OrderedDict, Sequence

from tonguetwister.lib.helper import splat_ordered_dict


class CastAssociationMap(Sequence):
    def __init__(self, stream):
        stream.set_big_endian()
        self._parse_records(stream)

    def _parse_records(self, stream):
        self._records = []
        while stream.tell() < stream.size():
            self._records.append(OrderedDict())
            self._records[-1]['mmap_idx'] = stream.uint32()

    def __getitem__(self, i):
        return self._records[i]

    def __len__(self):
        return len(self._records)

    def __repr__(self):
        msg = 'Associations\n'
        for i, record in enumerate(self._records):
            msg += f'    {i:4d}: {splat_ordered_dict(record)}\n'

        return msg
