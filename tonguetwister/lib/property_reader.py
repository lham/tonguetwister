from functools import wraps

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
    print('here1')
    def wrap(func):
        print('here2', func)
        func._register = index

        @wraps(func)
        def decorated_function(*args, **kwargs):
            return func(*args, **kwargs)

        return decorated_function

    return wrap


class PropertyReader(metaclass=PropertyReaderRegistry):
    unknown_prop_prefix = 'unknown_property_'

    def read(self, prop_id: int, stream: ByteBlockIO, length: int) -> dict:
        addr_start = stream.tell()

        # noinspection PyUnresolvedReferences
        key_map = self._get_key_map()

        if prop_id in key_map:
            method_name = key_map[prop_id]
            method = getattr(self, method_name)
        elif 'default' in key_map:
            method_name = f'{self.unknown_prop_prefix}{prop_id}'
            method = getattr(self, key_map['default'])
        else:
            method_name = f'{self.unknown_prop_prefix}{prop_id}'
            method = lambda s, l: s.read_bytes(l)

        if length > 0:
            return_value = method(stream, length)

            if isinstance(return_value, tuple):
                result = return_value[0]
                split = return_value[1]
            else:
                result = return_value
                split = True
        else:
            result = bytes()
            split = False

        if stream.tell() - addr_start != length:
            raise RuntimeError(f'Property reader did not read correct number of bytes for property id {prop_id}')

        if isinstance(result, dict) and split:
            return result
        else:
            return {method_name: result}

    def register(self, index, method_name):
        # noinspection PyUnresolvedReferences
        key_map = self._get_key_map()
        key_map[index] = method_name
