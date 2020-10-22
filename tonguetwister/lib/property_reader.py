from functools import wraps
from typing import Any

from tonguetwister.lib.byte_block_io import ByteBlockIO

registry = {}


class PropertyReaderRegistry(type):
    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)

        for key, val in attrs.items():
            prop_id = getattr(val, '_register', None)
            if prop_id is not None:
                if name not in registry:
                    registry[name] = {}
                registry[name][prop_id] = val.__name__

        setattr(cls, PropertyReaderRegistry._get_key_map.__name__, PropertyReaderRegistry._get_key_map)

    def _get_key_map(self):
        if self.__class__.__name__ in registry:
            return registry[self.__class__.__name__]
        else:
            return {}


def property_reader(index):
    def wrap(func):
        func._register = index

        @wraps(func)
        def decorated_function(*args, **kwargs):
            return func(*args, **kwargs)

        return decorated_function

    return wrap


class PropertyReader(metaclass=PropertyReaderRegistry):
    unknown_prop_prefix = 'unknown_prop_'

    def read(self, prop_id: int, stream: ByteBlockIO, length: int) -> dict:
        addr_start = stream.tell()

        # noinspection PyUnresolvedReferences
        key_map = self._get_key_map()

        if prop_id in key_map:
            method_name = key_map[prop_id]
            method = getattr(self, method_name)
        else:
            method_name = f'{self.unknown_prop_prefix}{prop_id}'
            method = lambda s: s.read_bytes(length)

        if length > 0:
            result = method(stream)
        else:
            result = bytes()

        if stream.tell() - addr_start != length:
            raise RuntimeError(f'Property reader did not read correct number of bytes for property id {prop_id}')

        if isinstance(result, dict):
            return result
        else:
            return {method_name: result}
