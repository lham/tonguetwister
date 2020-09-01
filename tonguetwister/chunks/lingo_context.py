from collections import OrderedDict, Sequence

from tonguetwister.lib.helper import splat_ordered_dict


class LingoContext(Sequence):

    def __init__(self, stream):
        stream.set_big_endian()
        self._parse_chunk_header(stream)
        self._parse_records(stream)

    def _parse_chunk_header(self, stream):
        self._context = OrderedDict()
        self._context['u1'] = stream.uint32()
        self._context['u2'] = stream.uint32()
        self._context['n_scripts'] = stream.uint32()
        self._context['n_scripts_2'] = stream.uint32()
        self._context['records_offset'] = stream.uint16()
        self._context['record_length'] = stream.uint16()
        self._context['u4'] = stream.uint16()
        self._context['u5'] = stream.uint16()
        self._context['lnam_id'] = stream.uint32()
        self._context['n_used?'] = stream.uint16()
        self._context['u6'] = stream.uint16()
        self._context['first_empty_slot_idx'] = stream.uint16()
        self._context['u7'] = stream.uint16()
        self._context['u8'] = stream.uint16()
        self._context['u9'] = stream.uint16()
        stream.read_bytes(56)

    def _parse_records(self, stream):
        stream.seek(self.header['records_offset'])
        self._records = []
        for i in range(self.header['n_scripts']):
            self._records.append(OrderedDict())
            self._records[i]['script_number'] = (stream.uint8(), stream.uint8(), stream.uint8(), stream.uint8())
            self._records[i]['mmap_idx'] = stream.uint32()
            self._records[i]['u2'] = stream.uint16()
            self._records[i]['u3'] = stream.uint16()

    @property
    def header(self):
        return self._context

    def __getitem__(self, i):
        return self._records[i]

    def __len__(self):
        return len(self._records)

    def __repr__(self):
        msg = f'    Header:{splat_ordered_dict(self.header)}\n'
        for i, record in enumerate(self._records):
            msg += f'    {i:2d}: {splat_ordered_dict(record)}\n'
        return msg
