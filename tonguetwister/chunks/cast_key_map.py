from collections import OrderedDict, Sequence

from tonguetwister.lib.helper import splat_ordered_dict


class CastKeyMap(Sequence):
    def __init__(self, stream):
        self._parse_chunk_header(stream)
        self._parse_records(stream)

    @property
    def header(self):
        return self._header

    def _parse_chunk_header(self, stream):
        self._header = OrderedDict()
        self._header['header_length'] = stream.uint16()
        self._header['record_length'] = stream.uint16()
        self._header['n_records'] = stream.uint32()
        self._header['n_used_record_slots'] = stream.uint32()

    def _parse_records(self, stream):
        self._records = []
        for i in range(self.header['n_records']):
            self._records.append(OrderedDict())
            self._records[i]['active'] = i < self.header['n_used_record_slots']
            self._records[i]['mmap_idx'] = stream.uint32()
            self._records[i]['cast_mmap_idx'] = stream.uint32()
            self._records[i]['four_cc'] = stream.string(4)

    def __getitem__(self, i):
        return self._records[i]

    def __len__(self):
        return len(self._records)

    def __repr__(self):
        msg = f'    Header: {splat_ordered_dict(self.header)}\n'
        for i, record in enumerate(self._records):
            msg += f'    {i:4d}: {splat_ordered_dict(record)}\n'

        return msg
