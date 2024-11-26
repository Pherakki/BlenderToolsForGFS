class NotAtEOFError(Exception):
    def __init__(self):
        super().__init__("Finished reading the stream before EOF was reached")
        

class AssertEOFDescriptor:
    FUNCTION_NAME = "assert_eof"

    def deserialize(binary_parser):
        if binary_parser.peek_bytestream(1) != b'':
            raise NotAtEOFError

    def serialize(binary_parser):
        pass

    def count(binary_parser):
        pass
