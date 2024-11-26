# try:
#     import numpy as np
#     _LOADED_NUMPY = True
# except ImportError:
_LOADED_NUMPY = False

import array
import struct
from ..utils import reshaping
from ..framework.descriptors import EndianPair

total_length         = reshaping.total_length
standardize_shape    = reshaping.standardize_shape
flatten_list         = reshaping.flatten_list
reshape_list         = reshaping.reshape_list
EndianPairDescriptor = EndianPair.EndianPairDescriptor

pack   = struct.pack
unpack = struct.unpack

if _LOADED_NUMPY:
    _typecode_lookup = {
      'b': 'i1',
      'h': 'i2',
      'i': 'i4',
      'q': 'i8',
      'B': 'u1',
      'H': 'u2',
      'I': 'u4',
      'Q': 'u8',
      'e': 'f2',
      'f': 'f4',
      'd': 'f8'
    }
    
    def define_dynamic_endian_primitive_array(name, typecode):
        elem_size  = struct.calcsize(typecode)
        dtype = _typecode_lookup[typecode]
        
        class PrimitiveArrayDescriptor:
            FUNCTION_NAME = f"rw_{name}"
            
            def deserialize(binary_parser, value, shape, endianness):
                shape = standardize_shape(shape)
                count = total_length(shape)
                v = np.frombuffer(binary_parser._bytestream.read(count*elem_size), dtype=np.dtype(endianness+dtype))
                return v.reshape(shape)
            
            def serialize(binary_parser, value, shape, endianness):
                if isinstance(value, np.ndarray):
                    binary_parser._bytestream.write(value.view(dtype=np.dtype(endianness+dtype)).tobytes())
                else:
                    shape = standardize_shape(shape)
                    deserialized_value = flatten_list(value, shape)
                    element_count = len(deserialized_value)
            
                    serialized_value = pack(endianness + typecode*element_count, *deserialized_value)
                    binary_parser._bytestream.write(serialized_value, elem_size*element_count)
                return value
            
            def count(binary_parser, value, shape, endianness):
                shape = standardize_shape(shape)
                count = total_length(shape)
                binary_parser.advance_offset(count*elem_size)
                return value
        
        PrimitiveArrayDescriptor.__name__     = name
        PrimitiveArrayDescriptor.__qualname__ = name
        return PrimitiveArrayDescriptor
    
    def define_endian_primitive_array(name, typecode, endianness):
        elem_size  = struct.calcsize(typecode)
        dtype = np.dtype(endianness + _typecode_lookup[typecode])
        
        class PrimitiveArrayDescriptor:
            FUNCTION_NAME = f"rw_{name}"
            
            def deserialize(binary_parser, value, shape):
                shape = standardize_shape(shape)
                count = total_length(shape)
                v = np.frombuffer(binary_parser._bytestream.read(count*elem_size), dtype=dtype)
                return v.reshape(shape)
            
            if endianness == ">":
                def serialize(binary_parser, value, shape):
                    if isinstance(value, np.ndarray):
                        binary_parser._bytestream.write(value.view(dtype=dtype).tobytes())
                    else:
                        shape = standardize_shape(shape)
                        deserialized_value = flatten_list(value, shape)
                        element_count = len(deserialized_value)
                
                        serialized_value = pack(">" + typecode*element_count, *deserialized_value)
                        binary_parser._bytestream.write(serialized_value, elem_size*element_count)
                    return value
            else:
                def serialize(binary_parser, value, shape):
                    if isinstance(value, np.ndarray):
                        binary_parser._bytestream.write(value.view(dtype=dtype).tobytes())
                    else:
                        shape = standardize_shape(shape)
                        deserialized_value = flatten_list(value, shape)
                        element_count = len(deserialized_value)
                
                        serialized_value = pack("<" + typecode*element_count, *deserialized_value)
                        binary_parser._bytestream.write(serialized_value, elem_size*element_count)
                    return value
            
            def count(binary_parser, value, shape):
                shape = standardize_shape(shape)
                count = total_length(shape)
                binary_parser.advance_offset(count*elem_size)
                return value
        
        PrimitiveArrayDescriptor.__name__     = name
        PrimitiveArrayDescriptor.__qualname__ = name
        return PrimitiveArrayDescriptor
else:
    def define_dynamic_endian_primitive_array(name, typecode):
        elem_size  = struct.calcsize(typecode)
        
        class PrimitiveArrayDescriptor:
            FUNCTION_NAME = f"rw_{name}"
            
            def deserialize(binary_parser, value, shape, endianness):
                shape = standardize_shape(shape)
                count = total_length(shape)
                v = array.array(typecode, binary_parser._bytestream.read(count*elem_size))
                if endianness == ">":
                    v.byteswap()
                return reshape_list(v, shape)
            
            def serialize(binary_parser, value, shape, endianness):
                shape = standardize_shape(shape)
                deserialized_value = flatten_list(value, shape)
                element_count = len(deserialized_value)
        
                serialized_value = pack(endianness + typecode*element_count, *deserialized_value)
                binary_parser._bytestream.write(serialized_value, elem_size*element_count)
                return value
            
            def count(binary_parser, value, shape, endianness):
                shape = standardize_shape(shape)
                count = total_length(shape)
                binary_parser.advance_offset(count*elem_size)
                return value
            
        PrimitiveArrayDescriptor.__name__     = name
        PrimitiveArrayDescriptor.__qualname__ = name
        return PrimitiveArrayDescriptor
    
    def define_endian_primitive_array(name, typecode, endianness):
        elem_size  = struct.calcsize(typecode)

        class PrimitiveArrayDescriptor:
            FUNCTION_NAME = f"rw_{name}"
            
            
            if typecode == 'e':
                # Slower by array doesn't understand 'e'
                if endianness == ">":
                    def deserialize(binary_parser, value, shape):
                        shape = standardize_shape(shape)
                        count = total_length(shape)
                        v = unpack('>' + 'e'*count, binary_parser._bytestream.read(count*elem_size))
                        return reshape_list(v, shape)
                else:
                    def deserialize(binary_parser, value, shape):
                        shape = standardize_shape(shape)
                        count = total_length(shape)
                        v = unpack('<' + 'e'*count, binary_parser._bytestream.read(count*elem_size))
                        return reshape_list(v, shape)
            else:
                if endianness == ">":
                    def deserialize(binary_parser, value, shape):
                        shape = standardize_shape(shape)
                        count = total_length(shape)
                        v = array.array(typecode, binary_parser._bytestream.read(count*elem_size))
                        v.byteswap()
                        return reshape_list(v, shape)
                else:
                    def deserialize(binary_parser, value, shape):
                        shape = standardize_shape(shape)
                        count = total_length(shape)
                        v = array.array(typecode, binary_parser._bytestream.read(count*elem_size))
                        return reshape_list(v, shape)
            
            if endianness == ">":
                def serialize(binary_parser, value, shape):
                    shape = standardize_shape(shape)
                    deserialized_value = flatten_list(value, shape)
                    element_count = len(deserialized_value)
            
                    serialized_value = pack(">" + typecode*element_count, *deserialized_value)
                    binary_parser._bytestream.write(serialized_value)
                    return value
            else:
                def serialize(binary_parser, value, shape):
                    shape = standardize_shape(shape)
                    deserialized_value = flatten_list(value, shape)
                    element_count = len(deserialized_value)
            
                    serialized_value = pack("<" + typecode*element_count, *deserialized_value)
                    binary_parser._bytestream.write(serialized_value)
                    return value
                
            def count(binary_parser, value, shape):
                shape = standardize_shape(shape)
                count = total_length(shape)
                binary_parser.advance_offset(count*elem_size)
                return value

        PrimitiveArrayDescriptor.__name__     = name
        PrimitiveArrayDescriptor.__qualname__ = name
        return PrimitiveArrayDescriptor

int8s_e     = define_dynamic_endian_primitive_array("int8s_e",    "b")
int16s_e    = define_dynamic_endian_primitive_array("int16s_e",   "h")
int32s_e    = define_dynamic_endian_primitive_array("int32s_e",   "i")
int64s_e    = define_dynamic_endian_primitive_array("int64s_e",   "q")
uint8s_e    = define_dynamic_endian_primitive_array("uint8s_e",   "B")
uint16s_e   = define_dynamic_endian_primitive_array("uint16s_e",  "H")
uint32s_e   = define_dynamic_endian_primitive_array("uint32s_e",  "I")
uint64s_e   = define_dynamic_endian_primitive_array("uint64s_e",  "Q")
float16s_e  = define_dynamic_endian_primitive_array("float16s_e", "e")
float32s_e  = define_dynamic_endian_primitive_array("float32s_e", "f")
float64s_e  = define_dynamic_endian_primitive_array("float64s_e", "d")

int8s_le    = define_endian_primitive_array("int8s_le",    "b", "<")
int16s_le   = define_endian_primitive_array("int16s_le",   "h", "<")
int32s_le   = define_endian_primitive_array("int32s_le",   "i", "<")
int64s_le   = define_endian_primitive_array("int64s_le",   "q", "<")
uint8s_le   = define_endian_primitive_array("uint8s_le",   "B", "<")
uint16s_le  = define_endian_primitive_array("uint16s_le",  "H", "<")
uint32s_le  = define_endian_primitive_array("uint32s_le",  "I", "<")
uint64s_le  = define_endian_primitive_array("uint64s_le",  "Q", "<")
float16s_le = define_endian_primitive_array("float16s_le", "e", "<")
float32s_le = define_endian_primitive_array("float32s_le", "f", "<")
float64s_le = define_endian_primitive_array("float64s_le", "d", "<")

int8s_be    = define_endian_primitive_array("int8s_be",    "b", ">")
int16s_be   = define_endian_primitive_array("int16s_be",   "h", ">")
int32s_be   = define_endian_primitive_array("int32s_be",   "i", ">")
int64s_be   = define_endian_primitive_array("int64s_be",   "q", ">")
uint8s_be   = define_endian_primitive_array("uint8s_be",   "B", ">")
uint16s_be  = define_endian_primitive_array("uint16s_be",  "H", ">")
uint32s_be  = define_endian_primitive_array("uint32s_be",  "I", ">")
uint64s_be  = define_endian_primitive_array("uint64s_be",  "Q", ">")
float16s_be = define_endian_primitive_array("float16s_be", "e", ">")
float32s_be = define_endian_primitive_array("float32s_be", "f", ">")
float64s_be = define_endian_primitive_array("float64s_be", "d", ">")

int8s       = EndianPairDescriptor("rw_int8s",    "rw_int8s_le",    "rw_int8s_be")
int16s      = EndianPairDescriptor("rw_int16s",   "rw_int16s_le",   "rw_int16s_be")
int32s      = EndianPairDescriptor("rw_int32s",   "rw_int32s_le",   "rw_int32s_be")
int64s      = EndianPairDescriptor("rw_int64s",   "rw_int64s_le",   "rw_int64s_be")
uint8s      = EndianPairDescriptor("rw_uint8s",   "rw_uint8s_le",   "rw_uint8s_be")
uint16s     = EndianPairDescriptor("rw_uint16s",  "rw_uint16s_le",  "rw_uint16s_be")
uint32s     = EndianPairDescriptor("rw_uint32s",  "rw_uint32s_le",  "rw_uint32s_be")
uint64s     = EndianPairDescriptor("rw_uint64s",  "rw_uint64s_le",  "rw_uint64s_be")
float16s    = EndianPairDescriptor("rw_float16s", "rw_float16s_le", "rw_float16s_be")
float32s    = EndianPairDescriptor("rw_float32s", "rw_float32s_le", "rw_float32s_be")
float64s    = EndianPairDescriptor("rw_float64s", "rw_float64s_le", "rw_float64s_be")


PRIMITIVE_ARRAY_DESCRIPTORS = [int8s_e,     int16s_e,    int32s_e,    int64s_e,
                               uint8s_e,    uint16s_e,   uint32s_e,   uint64s_e,
                               float16s_e,  float32s_e,  float64s_e,
                               int8s_le,    int16s_le,   int32s_le,   int64s_le,
                              uint8s_le,   uint16s_le,  uint32s_le,  uint64s_le,
                               float16s_le, float32s_le, float64s_le,
                               int8s_be,    int16s_be,   int32s_be,   int64s_be,
                               uint8s_be,   uint16s_be,  uint32s_be,  uint64s_be,
                               float16s_be, float32s_be, float64s_be]

PRIMITIVE_ENDIAN_ARRAY_DESCRIPTORS = [int8s,    int16s,   int32s,  int64s,
                                      uint8s,   uint16s,  uint32s, uint64s,
                                      float16s, float32s, float64s]
