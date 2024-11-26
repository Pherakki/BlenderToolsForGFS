class UnexpectedOffsetError(Exception):
    def __init__(self, prefix, expected, received, formatter):
        msg = f"{prefix}Excepted stream to be at {formatter(expected)}, but it is at {formatter(received)}"
        super().__init__(msg)
            
class UnexpectedGlobalOffsetError(UnexpectedOffsetError):
    def __init__(self, prefix, expected, received, transformer, formatter):
        msg = f"{prefix}Excepted stream to be at {formatter(expected)} [Global: {formatter(transformer(expected))}], but it is at {formatter(received)} [Global: {formatter(transformer(received))}]"
        super().__init__(msg)
            

class EnforceOffsetDescriptor:
    FUNCTION_NAME = "enforce_stream_offset"

    def deserialize(binary_parser, offset, message, formatter=lambda x: x):
        binary_parser.seek(offset)

    def serialize(binary_parser, offset, message, formatter=lambda x: x):
        if binary_parser.tell() != offset:
            prefix = message + ': ' if message is not None else ''
            if binary_parser.tell() != binary_parser.global_tell():
                raise UnexpectedGlobalOffsetError(prefix, offset, binary_parser.tell(), binary_parser.localToGlobalOffset, formatter)
            else:
                raise UnexpectedOffsetError(prefix, offset, binary_parser.tell())

    def count(binary_parser, offset, message, formatter=lambda x: x):
        binary_parser.offset = offset
