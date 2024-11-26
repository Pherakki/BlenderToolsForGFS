import struct
from ..framework.descriptors import EndianPair
EndianPairDescriptor = EndianPair.EndianPairDescriptor


def define_endian_primitive(name, typecode):
    elem_size  = struct.calcsize(typecode)
    struct_cls = struct.Struct(typecode)
    pack       = struct_cls.pack
    unpack     = struct_cls.unpack

    class PrimitiveDescriptor:
        FUNCTION_NAME = f"rw_{name}"

        def deserialize(binary_parser, value):
            return unpack(binary_parser._bytestream.read(elem_size))[0]

        def serialize(binary_parser, value):
            binary_parser._bytestream.write(pack(value))
            return value
        
        def count(binary_parser, value):
            binary_parser.advance_offset(elem_size)
            return value

    PrimitiveDescriptor.__name__     = name
    PrimitiveDescriptor.__qualname__ = name

    return PrimitiveDescriptor


pack   = struct.pack
unpack = struct.unpack
def define_dynamic_endian_primitive(name, typecode):
    elem_size  = struct.calcsize(typecode)
    
    class PrimitiveDescriptor:
        FUNCTION_NAME = f"rw_{name}"

        def deserialize(binary_parser, value, endianness):
            return unpack(endianness+typecode, binary_parser._bytestream.read(elem_size))[0]

        def serialize(binary_parser, value, endianness):
            binary_parser._bytestream.write(pack(endianness+typecode, value))
            return value
        
        def count(binary_parser, value, endianness):
            binary_parser.advance_offset(elem_size)
            return value

    PrimitiveDescriptor.__name__     = name
    PrimitiveDescriptor.__qualname__ = name

    return PrimitiveDescriptor


int8_e     = define_dynamic_endian_primitive("int8_e",    "b")
int16_e    = define_dynamic_endian_primitive("int16_e",   "h")
int32_e    = define_dynamic_endian_primitive("int32_e",   "i")
int64_e    = define_dynamic_endian_primitive("int64_e",   "q")
uint8_e    = define_dynamic_endian_primitive("uint8_e",   "B")
uint16_e   = define_dynamic_endian_primitive("uint16_e",  "H")
uint32_e   = define_dynamic_endian_primitive("uint32_e",  "I")
uint64_e   = define_dynamic_endian_primitive("uint64_e",  "Q")
float16_e  = define_dynamic_endian_primitive("float16_e", "e")
float32_e  = define_dynamic_endian_primitive("float32_e", "f")
float64_e  = define_dynamic_endian_primitive("float64_e", "d")

int8_le    = define_endian_primitive("int8_le",    "<b")
int16_le   = define_endian_primitive("int16_le",   "<h")
int32_le   = define_endian_primitive("int32_le",   "<i")
int64_le   = define_endian_primitive("int64_le",   "<q")
uint8_le   = define_endian_primitive("uint8_le",   "<B")
uint16_le  = define_endian_primitive("uint16_le",  "<H")
uint32_le  = define_endian_primitive("uint32_le",  "<I")
uint64_le  = define_endian_primitive("uint64_le",  "<Q")
float16_le = define_endian_primitive("float16_le", "<e")
float32_le = define_endian_primitive("float32_le", "<f")
float64_le = define_endian_primitive("float64_le", "<d")

int8_be    = define_endian_primitive("int8_be",    ">b")
int16_be   = define_endian_primitive("int16_be",   ">h")
int32_be   = define_endian_primitive("int32_be",   ">i")
int64_be   = define_endian_primitive("int64_be",   ">q")
uint8_be   = define_endian_primitive("uint8_be",   ">B")
uint16_be  = define_endian_primitive("uint16_be",  ">H")
uint32_be  = define_endian_primitive("uint32_be",  ">I")
uint64_be  = define_endian_primitive("uint64_be",  ">Q")
float16_be = define_endian_primitive("float16_be", ">e")
float32_be = define_endian_primitive("float32_be", ">f")
float64_be = define_endian_primitive("float64_be", ">d")

int8       = EndianPairDescriptor("rw_int8",    "rw_int8_le",    "rw_int8_be")
int16      = EndianPairDescriptor("rw_int16",   "rw_int16_le",   "rw_int16_be")
int32      = EndianPairDescriptor("rw_int32",   "rw_int32_le",   "rw_int32_be")
int64      = EndianPairDescriptor("rw_int64",   "rw_int64_le",   "rw_int64_be")
uint8      = EndianPairDescriptor("rw_uint8",   "rw_uint8_le",   "rw_uint8_be")
uint16     = EndianPairDescriptor("rw_uint16",  "rw_uint16_le",  "rw_uint16_be")
uint32     = EndianPairDescriptor("rw_uint32",  "rw_uint32_le",  "rw_uint32_be")
uint64     = EndianPairDescriptor("rw_uint64",  "rw_uint64_le",  "rw_uint64_be")
float16    = EndianPairDescriptor("rw_float16", "rw_float16_le", "rw_float16_be")
float32    = EndianPairDescriptor("rw_float32", "rw_float32_le", "rw_float32_be")
float64    = EndianPairDescriptor("rw_float64", "rw_float64_le", "rw_float64_be")

PRIMITIVE_DESCRIPTORS = [int8_e,     int16_e,    int32_e,    int64_e,
                         uint8_e,    uint16_e,   uint32_e,   uint64_e,
                         float16_e,  float32_e,  float64_e,
                         int8_le,    int16_le,   int32_le,   int64_le,
                         uint8_le,   uint16_le,  uint32_le,  uint64_le,
                         float16_le, float32_le, float64_le,
                         int8_be,    int16_be,   int32_be,   int64_be,
                         uint8_be,   uint16_be,  uint32_be,  uint64_be,
                         float16_be, float32_be, float64_be]

PRIMITIVE_ENDIAN_DESCRIPTORS = [int8, int16, int32, int64,
                                uint8, uint16, uint32, uint64,
                                float16, float32, float64]
