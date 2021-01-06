
class InvalidDirectorFile(RuntimeError):
    pass


class UnexpectedChunkClass(RuntimeError):
    def __init__(self, instance, expected_class):
        super().__init__(f'Unexpected chunk class: {instance.__class__.__name__} (expected {expected_class.__name__})')


class BadResourceCollection(RuntimeError):
    pass


class BadRelationCollection(RuntimeError):
    pass


class ChunkNotFound(RuntimeError):
    def __init__(self, chunk_class):
        super().__init__(f'Could not find chunk: {chunk_class.__name__}')
