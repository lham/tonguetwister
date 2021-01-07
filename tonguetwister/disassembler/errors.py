class InvalidDirectorFile(RuntimeError):
    pass


class UnexpectedChunkClass(RuntimeError):
    def __init__(self, instance, expected_class):
        super().__init__(f'Unexpected chunk class: {instance.__class__.__name__} (expected {expected_class.__name__})')


class ResourceAlreadyExists(RuntimeError):
    pass


class BadMemoryMapEntry(RuntimeError):
    pass


class ResourceNotLocated(RuntimeError):
    pass
