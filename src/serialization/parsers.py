from ...external.exbip.parsers.Reader        import Reader
from ...external.exbip.parsers.Writer        import Writer
from ...external.exbip.parsers.Validator     import Validator
from ...external.exbip.parsers.OffsetTracker import OffsetTracker


class UInt16SizedStrDescriptor:
    FUNCTION_NAME = "rw_uint16_sized_bstr"
    
    def deserialize(binary_parser, value):
        size = binary_parser.rw_uint16(None)
        return binary_parser.rw_bytestring(None, size)
    
    def serialize(binary_parser, value):
        binary_parser.rw_uint16(len(value))
        binary_parser.rw_bytestring(value, len(value))
        return value
    
    def count(binary_parser, value):
        binary_parser.advance_offset(len(value)+2)
        return value

class UVV1Descriptor:
    FUNCTION_NAME = "rw_uv_v1"
    
    def deserialize(binary_parser, value):
        uv = binary_parser.rw_float32s(None, 2)
        return [uv[0], 1-uv[1]]
    
    def serialize(binary_parser, value):
        binary_parser.rw_float32s([value[0], 1-value[1]], 2)
        return value
    
    def count(binary_parser, value):
        binary_parser.advance_offset(8)
        return value
    
class UVV2Descriptor:
    FUNCTION_NAME = "rw_uv_v2"
    
    def deserialize(binary_parser, value):
        uv = binary_parser.rw_float16s(None, 2)
        return [uv[0], 1-uv[1]]
    
    def serialize(binary_parser, value):
        binary_parser.rw_float16s([value[0], 1-value[1]], 2)
        return value
    
    def count(binary_parser, value):
        binary_parser.advance_offset(4)
        return value
   
class UInt8Vector32Descriptor:
    FUNCTION_NAME = "rw_uint8vector32"
    
    def deserialize(binary_parser, value):
        res = binary_parser.rw_uint32(None)
        return [res & 0x000000FF, (res & 0x0000FF00) >> 0x08, (res & 0x00FF0000) >> 0x10, (res & 0xFF000000) >> 0x18]
    
    def serialize(binary_parser, value):
        o = 0
        for i, v in enumerate(value):
            o |= (v << i*8)
        binary_parser.rw_uint32(o)
        return value
    
    def count(binary_parser, value):
        binary_parser.advance_offset(4)
        return value
 

class PaddedUInt8sDescriptor:
    FUNCTION_NAME = "rw_padded_uint8s"
    
    def deserialize(binary_parser, value, count):
        return binary_parser.rw_uint8s(None, count)
    
    def serialize(binary_parser, value, count):
        uints = [v for v in value]
        uints += [0 for _ in range(count-len(value))]
        binary_parser.rw_uint8s(uints, count)
        return value
    
    def count(binary_parser, value, count):
        binary_parser.advance_offset(count)
        return value

class PaddedUInt16sDescriptor:
    FUNCTION_NAME = "rw_padded_uint16s"
    
    def deserialize(binary_parser, value, count):
        return binary_parser.rw_uint16s(None, count)
    
    def serialize(binary_parser, value, count):
        uints = [v for v in value]
        uints += [0 for _ in range(count-len(value))]
        binary_parser.rw_uint16s(uints, count)
        return value
    
    def count(binary_parser, value, count):
        binary_parser.advance_offset(count*2)
        return value
    
class PaddedFloat32sDescriptor:
    FUNCTION_NAME = "rw_padded_float32s"
    
    def deserialize(binary_parser, value, count):
        return binary_parser.rw_float32s(None, count)
    
    def serialize(binary_parser, value, count):
        uints = [v for v in value]
        uints += [0. for _ in range(count-len(value))]
        binary_parser.rw_float32s(uints, count)
        return value
    
    def count(binary_parser, value, count):
        binary_parser.advance_offset(count*4)
        return value
    
    
class PaddedUnitary16sDescriptor:
    FUNCTION_NAME = "rw_padded_unit_intervals16"
    
    def deserialize(binary_parser, value, count):
        uints = binary_parser.rw_uint16s(None, count)
        return [u/0xFFFF for u in uints]
    
    def serialize(binary_parser, value, count):
        uints = [int(max(min(round(v*0xFFFF), 0xFFFF), 0)) for v in value]
        uints += [0 for _ in range(count-len(value))]
        binary_parser.rw_uint16s(uints, count)
        return value
    
    def count(binary_parser, value, count):
        binary_parser.advance_offset(count*2)
        return value
    
GFS_DESCRIPTORS = [
    UInt16SizedStrDescriptor,
    UVV1Descriptor,
    UVV2Descriptor,
    PaddedUInt8sDescriptor,
    PaddedUInt16sDescriptor,
    PaddedFloat32sDescriptor,
    PaddedUnitary16sDescriptor,
    UInt8Vector32Descriptor
]

class GFSReader(Reader.extended_with(GFS_DESCRIPTORS, [])):
    pass

class GFSWriter(Writer.extended_with(GFS_DESCRIPTORS, [])):
    pass

class GFSValidator(Validator.extended_with(GFS_DESCRIPTORS, [])):
    pass

class GFSOffsetTracker(OffsetTracker.extended_with(GFS_DESCRIPTORS, [])):
    pass

