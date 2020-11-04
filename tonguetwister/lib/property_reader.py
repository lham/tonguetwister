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


def property_reader(index):
    def wrap(func):
        func._register = index

        @wraps(func)
        def decorated_function(*args, **kwargs):
            return func(*args, **kwargs)

        return decorated_function

    return wrap


class PropertyReader(metaclass=PropertyReaderRegistry):
    unknown_prop_prefix = 'unknown_property_'

    def __init__(self):
        self._key_map = {}
        if self.__class__.__name__ in registry:
            # Clone so that dynamically added keys doesn't register on the class itself
            self._key_map = {k: v for k, v in registry[self.__class__.__name__].items()}

    def read(self, prop_id: int, stream: ByteBlockIO, length: int) -> dict:
        _bytes = stream.read_bytes(length)
        property_stream = ByteBlockIO(_bytes, endianess=stream.endianess)

        if prop_id in self._key_map:
            method_name = self._key_map[prop_id]
            method = getattr(self, method_name)
        elif 'default' in self._key_map:
            method_name = f'{self.unknown_prop_prefix}{prop_id}'
            method = getattr(self, self._key_map['default'])
        else:
            method_name = f'{self.unknown_prop_prefix}{prop_id}'
            method = lambda s: s.read_bytes()

        if length > 0:
            return_value = method(property_stream)

            if isinstance(return_value, tuple):
                result = return_value[0]
                split = return_value[1]
            else:
                result = return_value
                split = True
        else:
            result = bytes()
            split = False

        if not property_stream.is_depleted():
            print(property_stream.get_processed_bytes_string())
            print(property_stream.get_unprocessed_bytes_array())
            raise RuntimeError(f'Property reader did not read correct number of bytes for property id {prop_id}')

        if isinstance(result, dict) and split:
            return result
        else:
            return {method_name: result}

    def register(self, index, method_name, method):
        self._key_map[index] = method_name
        setattr(self, method_name, method)
