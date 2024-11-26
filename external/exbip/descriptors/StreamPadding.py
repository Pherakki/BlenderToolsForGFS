class UnexpectedPaddingError(Exception):
    def __init__(self, expected, received):
        super().__init__(f"Expected padding with a value of '{expected}', received '{received}'")
            

class PaddingDescriptor:
    FUNCTION_NAME = "rw_padding"

    def deserialize(binary_parser, count, pad_value=b'\x00'):
        size = count*len(pad_value)
        align_data = binary_parser._bytestream.read(size)
        expected_pad = pad_value*count
        if align_data != expected_pad:
            raise UnexpectedPaddingError(expected_pad, align_data)

    def serialize(binary_parser, count, pad_value=b'\x00'):
        binary_parser._bytestream.write(pad_value * count)

    def count(binary_parser, count, pad_value=b'\x00'):
        binary_parser.advance_offset(len(pad_value) * count)
