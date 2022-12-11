import array
import copy
import struct

from .utils import chunk_list, flatten_list


class Context:
    __slots__ = ("endianness")

    def __init__(self):
        self.endianness = "<"


class BinaryTargetBase:
    __slots__ = ("filename", "endianness", "bytestream", "anchor_pos", "context")

    open_flags = None

    type_sizes = {
        'x': 1,  # pad byte
        'c': 1,  # char
        'b': 1,  # int8
        'B': 1,  # uint8
        '?': 1,  # bool
        'h': 2,  # int16
        'H': 2,  # uint16
        'i': 4,  # int32
        'I': 4,  # uint32
        'l': 4,  # int32
        'L': 4,  # uint32
        'q': 8,  # int64
        'Q': 8,  # uint64
        'e': 2,  # half-float
        'f': 4,  # float
        'd': 8  # double
    }

    ############################
    # Main Behaviour Functions #
    ############################

    def __init__(self, filename):
        self.filename = filename
        self.bytestream = None
        self.anchor_pos = 0
        self.context = Context()

    # Context managers are a decent approximation of RAII behaviour
    def __enter__(self):
        self.bytestream = open(self.filename, self.open_flags)
        return self

    def __exit__(self, exc_type, exc_val, traceback):
        self.bytestream.close()
        self.bytestream = None

    #######################
    # Interface Functions #
    #######################

    def rw_single(self, typecode, value, endianness=None):
        return self._rw_single(typecode, self.type_sizes[typecode], value, endianness)

    def rw_multiple(self, typecode, value, shape, endianness=None):
        return self._rw_multiple(typecode, self.type_sizes[typecode], value, shape, endianness)

    def rw_obj(self, obj, *args, **kwargs):
        previous_context = self.context
        self.context = obj.context
        obj.read_write(self, *args, **kwargs)
        self.context = previous_context
        return obj

    def rw_obj_method(self, obj, method, *args, **kwargs):
        previous_context = self.context
        self.context = obj.context
        method(self, *args, **kwargs)
        self.context = previous_context

    def align_with(self, offset, alignment, typecode, value, endianness=None):
        if endianness is None:
            endianness = self.context.endianness
        padval = struct.pack(endianness + typecode, value)
        self.align(offset, alignment, padval)

    def align_to(self, offset, width, typecode, value, endianness=None):
        alignment = width * self.type_sizes[typecode]
        self.align_with(offset, alignment, typecode, value, endianness)

    # RW functions (should be defined in a loop...)
    def rw_pad8   (self):                         return self._handle_pads(1)
    def rw_pad16  (self):                         return self._handle_pads(2)
    def rw_pad32  (self):                         return self._handle_pads(4)
    def rw_pad64  (self):                         return self._handle_pads(8)
    def rw_int8   (self, value, endianness=None): return self._rw_single('b', 1, value, endianness)
    def rw_uint8  (self, value, endianness=None): return self._rw_single('B', 1, value, endianness)
    def rw_int16  (self, value, endianness=None): return self._rw_single('h', 2, value, endianness)
    def rw_uint16 (self, value, endianness=None): return self._rw_single('H', 2, value, endianness)
    def rw_int32  (self, value, endianness=None): return self._rw_single('i', 4, value, endianness)
    def rw_uint32 (self, value, endianness=None): return self._rw_single('I', 4, value, endianness)
    def rw_int64  (self, value, endianness=None): return self._rw_single('q', 8, value, endianness)
    def rw_uint64 (self, value, endianness=None): return self._rw_single('Q', 8, value, endianness)
    def rw_float16(self, value, endianness=None): return self._rw_single('e', 2, value, endianness)
    def rw_float32(self, value, endianness=None): return self._rw_single('f', 4, value, endianness)
    def rw_float64(self, value, endianness=None): return self._rw_single('d', 8, value, endianness)

    def rw_pad8s   (self, shape):                         return self._handle_pads(shape)
    def rw_pad16s  (self, shape):                         return self._handle_pads(2*shape)
    def rw_pad32s  (self, shape):                         return self._handle_pads(4*shape)
    def rw_pad64s  (self, shape):                         return self._handle_pads(8*shape)
    def rw_int8s   (self, value, shape, endianness=None): return self._rw_multiple('b', 1, value, shape, endianness)
    def rw_uint8s  (self, value, shape, endianness=None): return self._rw_multiple('B', 1, value, shape, endianness)
    def rw_int16s  (self, value, shape, endianness=None): return self._rw_multiple('h', 2, value, shape, endianness)
    def rw_uint16s (self, value, shape, endianness=None): return self._rw_multiple('H', 2, value, shape, endianness)
    def rw_int32s  (self, value, shape, endianness=None): return self._rw_multiple('i', 4, value, shape, endianness)
    def rw_uint32s (self, value, shape, endianness=None): return self._rw_multiple('I', 4, value, shape, endianness)
    def rw_int64s  (self, value, shape, endianness=None): return self._rw_multiple('q', 8, value, shape, endianness)
    def rw_uint64s (self, value, shape, endianness=None): return self._rw_multiple('Q', 8, value, shape, endianness)
    def rw_float16s(self, value, shape, endianness=None): return self._rw_multiple('e', 2, value, shape, endianness)
    def rw_float32s(self, value, shape, endianness=None): return self._rw_multiple('f', 4, value, shape, endianness)
    def rw_float64s(self, value, shape, endianness=None): return self._rw_multiple('d', 8, value, shape, endianness)

    ####################################
    # Bytestream Interaction Functions #
    ####################################

    def tell(self):
        return self.bytestream.tell()

    def seek(self, offset, whence=0):
        self.bytestream.seek(offset, whence)

    def global_tell(self):
        return self.tell()

    def global_seek(self, offset, whence=0):
        self.seek(offset, whence)

    def local_tell(self):
        return self.convert_to_local_position(self.global_tell())

    def local_seek(self, pos, whence=0):
        return self.seek(self.convert_to_global_position(pos), whence)

    def convert_to_local_position(self, position):
        return position - self.anchor_pos

    def convert_to_global_position(self, position):
        return position + self.anchor_pos

    def assert_file_pointer_now_at(self, msg, location, file_pointer_location=None, use_hex=True):
        if file_pointer_location is None:
            file_pointer_location = self.global_tell()
        if file_pointer_location != location:
            if use_hex:
                size = lambda x: len(f'{x:0x}')
                formatter = lambda x: f"0x{x:0{size(x) + (((size(x) + 1) // 2) - (size(x) // 2))}x}"
            else:
                formatter = lambda x: x
            raise Exception(f"File pointer at {formatter(file_pointer_location)}, expected find {msg} with the pointer at {formatter(location)}.")

    def assert_global_file_pointer_now_at(self, msg, location, file_pointer_location=None, use_hex=True):
        self.assert_file_pointer_now_at(msg, location, file_pointer_location, use_hex)

    def assert_local_file_pointer_now_at(self, msg, location, file_pointer_location=None, use_hex=True):
        if file_pointer_location is None:
            file_pointer_location = self.local_tell()
        if file_pointer_location != location:
            if use_hex:
                size = lambda x: len(f'{x:0x}')
                formatter = lambda x: f"0x{x:0{size(x) + (((size(x) + 1) // 2) - (size(x) // 2))}x}"
            else:
                formatter = lambda x: x
            raise Exception(
                f"File pointer at {formatter(file_pointer_location)}, expected find {msg} with the pointer at {formatter(location)}.")

    def tie_to_offset(self, value):
        return value

    def tie_to_local_offset(self, value):
        return value

    ############################
    # Arg Validation Functions #
    ############################

    @staticmethod
    def assert_equal(data, check_value, formatter=lambda x: x):
        if (data != check_value):
            raise ValueError(f"Expected variable to be {formatter(check_value)}, but it was {formatter(data)}.")

    @classmethod
    def assert_is_zero(cls, data):
        cls.assert_equal(data, 0)

    ##########################
    # Pure Virtual Functions #
    ##########################

    def _handle_pads(self, count):
        raise NotImplementedError

    def rw_offset_uint32(self, value, offset, endianness=None):
        raise NotImplementedError

    def _rw_single(self, typecode, size, value, endianness=None):
        raise NotImplementedError

    def _rw_multiple(self, typecode, size, value, shape, endianness=None):
        raise NotImplementedError

    def rw_str(self, value, length, encoding='ascii'):
        raise NotImplementedError

    def rw_cstr(self, value, encoding='ascii'):
        raise NotImplementedError
        
    def rw_uint16_sized_str(self, value, encoding="ascii"):
        raise NotImplementedError

    def rw_bytestring(self, value, count):
        raise NotImplementedError

    def rw_bytestrings(self, value, count, shape):
        raise NotImplementedError

    def rw_unbounded_bytestring(self, value):
        raise NotImplementedError

    def rw_s3Quat(self, value, endianness=None):
        raise NotImplementedError

    def rw_s3Quats(self, value, shape, endianness=None):
        raise NotImplementedError
    
    def rw_uv(self, value, endianness=None):
        raise NotImplementedError

    def rw_obj_array(self, value, obj_constructor, shape, *args, validator=None, **kwargs):
        raise NotImplementedError
        
    def rw_new_obj(self, value, obj_constructor, ctor_args=None, ctor_kwargs=None, rw_args=None, rw_kwargs=None):
        raise NotImplementedError

    def align(self, offset, alignment, padval=b'\x00'):
        raise NotImplementedError

    def assert_at_eof(self):
        raise NotImplementedError

    def mode(self):
        raise NotImplementedError


class Reader(BinaryTargetBase):
    open_flags = "rb"

    def _handle_pads(self, count):
        value = self.bytestream.read(count)
        if value != b'\x00'*count:
            raise ValueError(f"Excepted padding bytes, but found {value}")

    def rw_offset_uint32(self, value, offset, endianness=None):
        return self.rw_uint32(value, endianness) + offset
    
    def _rw_single(self, typecode, size, value, endianness=None):
        if endianness is None:
            endianness = self.context.endianness
        return struct.unpack(endianness + typecode, self.bytestream.read(size))[0]

    def _rw_multiple(self, typecode, size, value, shape, endianness=None):
        if endianness is None:
            endianness = self.context.endianness

        if not hasattr(shape, "__getitem__"):
            shape = (shape,)
        n_to_read = 1
        for elem in shape:
            n_to_read *= elem

        if typecode == "e":
            arr_typecode = "f"
        else:
            arr_typecode = typecode
        data = array.array(arr_typecode,
                           struct.unpack(endianness + typecode * n_to_read, self.bytestream.read(size * n_to_read)))
        # Group the lists up
        # Skip the outer index because we don't need it (we'll automatically
        # get an end result of that length) and create groups by iterating
        # over the shape in reverse
        for subshape in shape[1::][::-1]:
            data = chunk_list(data, subshape)
        return data

    def rw_str(self, value, length, encoding='ascii'):
        data = self.bytestream.read(length)
        try:
            return data.decode(encoding)
        except Exception as e:
            print(data)
            raise e

    def rw_cstr(self, value, encoding='ascii', end_char=b"\x00"):
        out = b""
        val = self.bytestream.read(1)
        while (val != end_char and val != b''):
            out += val
            val = self.bytestream.read(1)
        return out.decode(encoding)
        
    def rw_uint16_sized_str(self, value, encoding="ascii"):
        size = self.rw_uint16(None)
        return self.rw_str(None, size, encoding)
        
    def rw_bytestring(self, value, count):
        return self.bytestream.read(count)

    def rw_bytestrings(self, value, count, shape):
        out = [None]*shape
        for i in range(shape):
            out[i] = self.rw_bytestring(value, count)
        return out

    def rw_unbounded_bytestring(self, value):
        return self.bytestream.read()

    def rw_s3Quat(self, value, endianness=None):
        input_data = self.rw_uint8s(None, 6)
        if (input_data[0] & 0x80) >> 7 == 1:
            print("WARNING: Quaternion with a leading bit of 1 found.")
        c1 = (input_data[0] & 0x7F) << 8 | input_data[1]
        c2 = (input_data[2] & 0xFF) << 7 | (input_data[3] & 0xFE) >> 1
        c3 = (input_data[3] & 0x01) << 14 | (input_data[4] & 0xFF) << 6 | (input_data[5] & 0xFC) >> 2
        largest_index = input_data[5] & 0x03

        components = [c1, c2, c3]
        components = [c - 16383 for c in components]
        components = [c / 16384 for c in components]
        components = [c / (2**.5) for c in components]

        square_vector_length = sum([c ** 2 for c in components])
        largest_component = (1 - square_vector_length)**.5
        if square_vector_length <= 1: # Should be smaller than 0.5...
            largest_component = (1 - square_vector_length)**.5
        else:
            print("WARNING: Quaternion with an invalid largest component found.")
            largest_component = 0

        components.insert(largest_index, largest_component)

        return components

    def rw_s3Quats(self, value, shape, endianness=None):
        if not hasattr(shape, "__getitem__"):
            shape = (shape,)
        n_to_read = 1
        for elem in shape:
            n_to_read *= elem

        data = [self.rw_s3Quat(None, endianness) for _ in range(n_to_read)]

        for subshape in shape[1::][::-1]:
            data = chunk_list(data, subshape)
        return data

    def rw_uv(self, value, endianness=None):
        u, v = self.rw_float32s(None, 2, endianness)
        return [u, (v*-1) + 1]
        
    def peek_bytestring(self, count):
        val = self.bytestream.read(count)
        self.bytestream.seek(-len(val), 1)
        return val

    def rw_obj_array(self, value, obj_constructor, shape, *args, validator=None, **kwargs):
        if not hasattr(shape, "__getitem__"):
            shape = (shape,)
        n_to_read = 1
        for elem in shape:
            n_to_read *= elem

        data = []
        for _ in range(n_to_read):
            d = obj_constructor()
            data.append(d)
            if validator is not None:
                validator(d)
            self.rw_obj(d, *args, **kwargs)
    
        for subshape in shape[1::][::-1]:
            data = chunk_list(data, subshape)
        return data
    
    def rw_new_obj(self, value, obj_constructor, ctor_args=None, ctor_kwargs=None, rw_args=None, rw_kwargs=None):
        if ctor_args is None: ctor_args = []
        if ctor_kwargs is None: ctor_kwargs = {}
        if rw_args is None: rw_args = []
        if rw_kwargs is None: rw_kwargs = {}
        obj = obj_constructor(*ctor_args, **ctor_kwargs)
        return self.rw_obj(obj, *rw_args, **rw_kwargs)
    
    def align(self, offset, alignment, padval=b'\x00'):
        n_to_read = (alignment - (offset % alignment)) % alignment
        data = self.bytestream.read(n_to_read)
        expected = padval * (len(data) // len(padval))
        assert data == expected, f"Unexpected padding: Expected {expected}, read {data}."

    def assert_at_eof(self):
        if (self.peek_bytestring(1) != b''):
            raise Exception("Not at end of file!")

    def mode(self):
        return "read"


class Writer(BinaryTargetBase):
    open_flags = "wb"

    def _handle_pads(self, count):
        self.bytestream.write(b'\x00'*count)

    def rw_offset_uint32(self, value, offset, endianness=None):
        self.rw_uint32(value - offset, endianness)
        return value

    def _rw_single(self, typecode, size, value, endianness=None):
        if endianness is None:
            endianness = self.context.endianness
        self.bytestream.write(struct.pack(endianness + typecode, value))
        return value

    def _rw_multiple(self, typecode, size, value, shape, endianness=None):
        if endianness is None:
            endianness = self.context.endianness

        if not hasattr(shape, "__getitem__"):
            shape = (shape,)
        n_to_read = 1
        for elem in shape:
            n_to_read *= elem

        data = value  # Shouldn't need to deepcopy since flatten_list will copy
        for _ in range(len(shape) - 1):
            data = flatten_list(data)
        self.bytestream.write(struct.pack(endianness + typecode * n_to_read, *data))
        return value

    def rw_str(self, value, length, encoding='ascii'):
        self.bytestream.write(value.encode(encoding))
        return value

    def rw_cstr(self, value, encoding='ascii', end_char=b'\x00'):
        out = value.encode(encoding) + end_char
        self.bytestream.write(out)
        return value
        
    def rw_uint16_sized_str(self, value, encoding="ascii"):
        bytestring = value.encode(encoding)
        size = self.rw_uint16(len(bytestring))
        self.rw_bytestring(bytestring, size)
        return value
    
    def rw_bytestring(self, value, count):
        if len(value) != count:
            raise ValueError(f"Expected to write a bytestring of length {count}, but it was length {len(value)}.")
        self.bytestream.write(value)
        return value

    def rw_bytestrings(self, value, count, shape):
        for v in value:
            self.rw_bytestring(v, count)
        return value

    def rw_unbounded_bytestring(self, value):
        return self.rw_bytestring(value, len(value))

    def rw_s3Quat(self, value, endianness=None):
        components = copy.deepcopy(value)
        abs_components = [abs(c) for c in components]
        abs_largest_component = max(abs_components)
        largest_index = abs_components.index(abs_largest_component)
        largest_component = components[largest_index]
        largest_component_sign = largest_component // (abs(largest_component))
        # Get rid of the largest component
        # No need to store the sign of the largest component, because
        # (X, Y, Z, W) = (-X, -Y, -Z, -W)
        # So just multiply through by the sign of the removed component to create an equivalent quaternion
        # In this way, the largest component is always +ve
        del components[largest_index]
        components = [largest_component_sign * c for c in components]

        # No other component can be larger than 1/sqrt(2) due to normalisation
        # So map the remaining components from the interval [-1/sqrt(2), 1/sqrt(2)] to [0, 32767] to gain ~1.4x precision
        components = [int(round(c * (2**.5) * 16384)) + 16383 for c in components]

        for i, elem in enumerate(components):
            if elem < 0:
                components[i] = 0
            elif elem > 32767:
                components[i] = 32767

        # Now convert to big-endian uint15s
        packed_rep = [0, 0, 0, 0, 0, 0]
        packed_rep[0] = (components[0] >> 8) & 0x7F
        packed_rep[1] = components[0] & 0xFF
        packed_rep[2] = (components[1] >> 7) & 0xFF
        packed_rep[3] = ((components[1] & 0xFF) << 1) | ((components[2] & 0xC0) >> 7)
        packed_rep[4] = (components[2] >> 6) & 0xFF
        packed_rep[5] = ((components[2] & 0x3F) << 2) | largest_index

        self.rw_uint8s(packed_rep, 6)

        return value

    def rw_s3Quats(self, value, shape, endianness=None):
        if not hasattr(shape, "__getitem__"):
            shape = (shape,)
        n_to_read = 1
        for elem in shape:
            n_to_read *= elem

        data = value  # Shouldn't need to deepcopy since flatten_list will copy
        for _ in range(len(shape) - 1):
            data = flatten_list(data)
        for d in data:
            self.rw_s3Quat(d)

        return value

    def rw_uv(self, value, endianness=None):
        self.rw_float32s([value[0], (value[1]*-1) + 1], 2, endianness)
        return value
    
    def rw_obj_array(self, value, obj_constructor, shape, *args, validator=None, **kwargs):
        if not hasattr(shape, "__getitem__"):
            shape = (shape,)
        n_to_read = 1
        for elem in shape:
            n_to_read *= elem

        data = value  # Shouldn't need to deepcopy since flatten_list will copy
        for _ in range(len(shape) - 1):
            data = flatten_list(data)
        for d in data:
            if validator is not None:
                validator(d)
            self.rw_obj(d, *args, **kwargs)

        return value
    
    def rw_new_obj(self, value, obj_constructor, ctor_args=None, ctor_kwargs=None, rw_args=None, rw_kwargs=None):
        if rw_args is None: rw_args = []
        if rw_kwargs is None: rw_kwargs = {}
        return self.rw_obj(value, *rw_args, **rw_kwargs)
    
    def align(self, offset, alignment, padval=b'\x00'):
        n_to_read = (alignment - (offset % alignment)) % alignment
        data = padval * (n_to_read // len(padval))
        self.bytestream.write(data)

    def assert_at_eof(self):
        pass

    def mode(self):
        return "write"


class OffsetTracker(BinaryTargetBase):
    open_flags = None

    __slots__ = ("virtual_offset", "pointers")

    def __init__(self):
        super().__init__(None)
        self.virtual_offset = 0
        self.pointers = []

    # Context managers are a decent approximation of RAII behaviour
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, traceback):
        pass

    def log_offset(self):
        self.pointers.append(self.virtual_offset)

    def adv_offset(self, adv):
        self.virtual_offset += adv

    def _handle_pads(self, count):
        self.adv_offset(count)

    def rw_offset_uint32(self, value, offset, endianness=None):
        return self.rw_uint32(value, endianness)

    def _rw_single(self, typecode, size, value, endianness=None):
        self.adv_offset(size)
        return value

    def _rw_multiple(self, typecode, size, value, shape, endianness=None):
        if not hasattr(shape, "__getitem__"):
            shape = (shape,)
        n_to_read = 1
        for elem in shape:
            n_to_read *= elem

        for i in range(n_to_read):
            self.adv_offset(size)

        return value

    def rw_str(self, value, length, encoding='ascii'):
        length = len(value.encode(encoding))
        self.adv_offset(length)
        return value

    def rw_cstr(self, value, encoding='ascii', end_char=b'\x00'):
        out = value.encode(encoding) + end_char
        length = len(out)
        self.adv_offset(length)
        return value
    
    def rw_uint16_sized_str(self, value, encoding="ascii"):
        bytestring = value.encode(encoding)
        size = self.rw_uint16(len(bytestring))
        self.rw_bytestring(bytestring, size)
        return value
    
    def rw_bytestring(self, value, count):
        self.virtual_offset += count
        return value

    def rw_bytestrings(self, value, count, shape):
        for v in value:
            self.rw_bytestring(v, count)
        return value

    def rw_unbounded_bytestring(self, value):
        return self.rw_bytestring(value, len(value))
    
    def align(self, offset, alignment, padval=b'\x00'):
        n_to_read = (alignment - (offset % alignment)) % alignment
        data = padval * (n_to_read // len(padval))

        self.adv_offset(len(data))

    def assert_at_eof(self):
        pass

    def mode(self):
        return "VirtualParser"

    def tell(self):
        return self.virtual_offset

    def seek(self, offset, whence=0):
        if whence != 0:
            raise NotImplementedError
        self.virtual_offset = offset

    def assert_file_pointer_now_at(self, location, file_pointer_location=None, use_hex=False):
        pass

    def assert_local_file_pointer_now_at(self, msg, location, file_pointer_location=None, use_hex=False):
        pass

    @staticmethod
    def assert_equal(data, check_value, formatter=lambda x: x):
        pass

    @classmethod
    def assert_is_zero(cls, data):
        pass
    
    def rw_obj_array(self, value, obj_constructor, shape, *args, validator=None, **kwargs):
        if not hasattr(shape, "__getitem__"):
            shape = (shape,)
        n_to_read = 1
        for elem in shape:
            n_to_read *= elem

        data = value  # Shouldn't need to deepcopy since flatten_list will copy
        for _ in range(len(shape) - 1):
            data = flatten_list(data)
        for d in data:
            self.rw_obj(d, *args, **kwargs)

        return value
        
    def rw_s3Quat(self, value, endianness=None):
        self.adv_offset(6)
        return value

    def rw_s3Quats(self, value, shape, endianness=None):
        if not hasattr(shape, "__getitem__"):
            shape = (shape,)
        n_to_read = 1
        for elem in shape:
            n_to_read *= elem

        for _ in range(n_to_read):
            self.rw_s3Quat(None)

        return value
    
    def rw_new_obj(self, value, obj_constructor, ctor_args=None, ctor_kwargs=None, rw_args=None, rw_kwargs=None):
        if rw_args is None: rw_args = []
        if rw_kwargs is None: rw_kwargs = {}
        return self.rw_obj(value, *rw_args, **rw_kwargs)
    
    def rw_uv(self, value, endianness=None):
        self.rw_float32s(value, 2, endianness)
        return value

class PointerCalculator(OffsetTracker):
    open_flags = None

    def tie_to_offset(self, value):
        return self.tell()

    def tie_to_local_offset(self, value):
        return self.local_tell()

    def mode(self):
        return "PointerCalculator"
