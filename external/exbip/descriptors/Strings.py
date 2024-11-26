class BytestringDescriptor:
    FUNCTION_NAME = "rw_bytestring"

    def deserialize(binary_parser, value, length):
        return binary_parser._bytestream.read(length)

    def serialize(binary_parser, value, length):
        binary_parser._bytestream.write(value)
        return value
    
    def count(binary_parser, value, length):
        binary_parser.advance_offset(length)
        return value
    
class BytestringsDescriptor:
    FUNCTION_NAME = "rw_bytestrings"

    def deserialize(binary_parser, value, lengths):
        return [binary_parser._bytestream.read(length) for length in lengths]

    def serialize(binary_parser, value, lengths):
        for v in value:
            binary_parser._bytestream.write(v)
        return value
    
    def count(binary_parser, value, length):
        for v in value:
            binary_parser.advance_offset(len(v))
        return value

class CBytestringDescriptor:
    FUNCTION_NAME = "rw_cbytestring"
    
    def deserialize(binary_parser, value, chunksize=0x40, terminator=b'\x00'):
        # Read the bytestring in 'chunksize' chunks and scan each chunk
        # for the terminator byte. 
        # This is faster than reading individual bytes, c.f. 'strings.py' in
        # the 'benchmarks' directory. Larger chunksizes are more efficient for
        # larger strings, and more benignly hurt performance for short strings.
        # The terminator is also identified first and then the bytestring is
        # re-read. This is again faster than repeatedly resizing a bytestring.
        origin = binary_parser.tell()
        
        sz = 0
        fr = binary_parser._bytestream.read
        buf = fr(chunksize)
        idx = buf.find(terminator)
        while idx == -1:
            sz += chunksize
            buf = fr(chunksize)
            idx = buf.find(terminator)
            if not len(buf):
                binary_parser.seek(origin)
                return fr(sz+chunksize)
        origin  = sz + chunksize
        sz     += idx
        
        binary_parser.seek(origin)
        return fr(sz+1)[:-1]

    def serialize(binary_parser, value, chunksize=0x40, terminator=b'\x00'):
        binary_parser._bytestream.write(value + terminator)
        return value
    
    def count(binary_parser, value, chunksize=0x40, terminator=b'\x00'):
        binary_parser.advance_offset(len(value)+len(terminator))
        return value

class CBytestringsDescriptor:
    FUNCTION_NAME = "rw_cbytestrings"
    
    def deserialize(binary_parser, value, count, chunksize=0x40, terminator=b'\x00'):
        return [CBytestringDescriptor.deserialize(binary_parser, value, chunksize, terminator) for _ in range(count)]

    def serialize(binary_parser, value, chunksize=0x40, terminator=b'\x00'):
        total = b''.join((v+terminator) for v in value)
        binary_parser._bytestream.write(total)
        return value
    
    def count(binary_parser, value, chunksize=0x40, terminator=b'\x00'):
        binary_parser.advance_offset(sum(len(v) for v in value) + len(value)*len(terminator))
        return value
