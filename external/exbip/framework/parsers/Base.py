import os
import types

class Scope:
    __slots__ = ("origin",)
    
    def __init__(self, origin):
        self.origin = origin


class OffsetManager:
    def __init__(self, rw):
        self._rw = rw

    def __enter__(self):
        self._rw.push_origin()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._rw.pop_origin()


class EndiannessManager:
    def __init__(self, rw, new_endianness):
        self._rw = rw
        self._prev_endianness = rw.endianness
        self.new_endianness = new_endianness

    def __enter__(self):
        self._rw.set_endianness(self.new_endianness)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._rw.set_endianness(self._prev_endianness)


class IBinaryParser:
    __slots__ = ("_reference_offset_stack", "_endianness")
    
    _LE_SETTERS = []
    _BE_SETTERS = []
    
    def __init__(self, endianness="<"):
        self._reference_offset_stack = [0]
        self.set_endianness(endianness)
    
    #########################
    # CLASS EXTENSION FUNCS #
    #########################
    @classmethod
    def extended_with(cls, descriptors=None, endian_inlined=None):
        if descriptors    is None: descriptors    = []
        if endian_inlined is None: endian_inlined = []
        
        # Construct slots
        slots = []
        for inliner in endian_inlined:
            slots.append(inliner.FUNCTION_NAME)
        
        # Create base class for extension
        class DerivedClass(cls):
            __slots__ = tuple(slots)
            
            _LE_SETTERS = [_ for _ in cls._LE_SETTERS]
            _BE_SETTERS = [_ for _ in cls._BE_SETTERS]
        
        # Install descriptors
        for desc in descriptors:
            setattr(DerivedClass, desc.FUNCTION_NAME, DerivedClass._get_rw_method(desc))
        
        # Install endian-aware extensions
        def mk_getattr(fn_name):
            def fn(self):
                return getattr(self, fn_name)
            return fn
        for inliner in endian_inlined:
            nm = inliner.FUNCTION_NAME
            DerivedClass._LE_SETTERS.append((nm, getattr(DerivedClass, inliner.little_endian)))
            DerivedClass._BE_SETTERS.append((nm, getattr(DerivedClass, inliner.big_endian)))
        
        return DerivedClass
    
    ############################
    # RUNTIME DESCRIPTOR USAGE #
    ############################
    def execute_descriptor(self, descriptor, *args, **kwargs):
        fn = self._get_rw_method(descriptor)
        return fn(self, *args, **kwargs)
    
    __call__ = execute_descriptor
    
    ######################
    # ABSTRACT INTERFACE #
    ######################
    # Read/Write interface
    @staticmethod
    def _get_rw_method(descriptor):
        """Retrieves the appropriate read/write method from a descriptor."""
        raise NotImplementedError

    #############################
    # ABSTRACT STREAM INTERFACE #
    #############################
    # Seeks - separate to a 'Seekable' interface?
    def global_seek(self, offset, whence=os.SEEK_SET):
        raise NotImplementedError
        
    # Tells - separate to a 'Tellable' interface?
    def global_tell(self):
        raise NotImplementedError
        
    ####################
    # STREAM INTERFACE #
    ####################
    @staticmethod
    def bytes_to_alignment(position, alignment):
        return (alignment - (position % alignment)) % alignment
    
    def is_unaligned(self, alignment):
        return self.bytes_to_alignment(self.tell(), alignment) != 0
    
    # SEEKS
    def relative_global_seek(self, offset, base_position, whence=os.SEEK_SET):
        if whence==os.SEEK_SET:
            return self.global_seek(offset + base_position, whence)
        else:
            return self.global_seek(offset, whence)
    
    def seek(self, offset, whence=os.SEEK_SET):
        return self.relative_global_seek(offset, self.current_origin(), whence)
    
    def relative_seek(self, offset, base_position, whence=os.SEEK_SET):
        return self.seek(offset, base_position, whence)
    
    # TELLS
    def relative_global_tell(self, base_position):
        return self.global_tell() - base_position

    def tell(self):
        return self.relative_global_tell(self.current_origin())

    def relative_tell(self, base_position):
        return self.tell() - base_position
    
    # TRANSFORMS
    def localToGlobalOffset(self, offset):
        return offset + self.current_origin()
    
    def globalToLocalOffset(self, offset):
        return offset - self.current_origin()
    
    # STREAM ORIGIN
    def current_origin(self):
        return self._reference_offset_stack[-1]

    def push_origin(self):
        self._reference_offset_stack.append(self.global_tell())
        
    def pop_origin(self):
        self._reference_offset_stack.pop()

    def new_origin(self):
        return OffsetManager(self)
    
    # STREAM ENDIANNESS
    @property
    def endianness(self):
        return self._endianness
    
    def set_endianness(self, value):
        # Doing setattr on type(self) rather than self seems to incur less
        # overhead when calling the function, but that's not particularly safe.
        if value == '<':
            for nm, le in self._LE_SETTERS:
                setattr(self, nm, types.MethodType(le, self))
                
        elif value == '>':
            for nm, be in self._BE_SETTERS:
                setattr(self, nm, types.MethodType(be, self))
        else:
            raise ValueError("Invalid endianness: {value} (use '<' or '>')")
        
        self._endianness = value
    
    def as_littleendian(self):
        return EndiannessManager(self, "<")
    
    def as_bigendian(self):
        return EndiannessManager(self, ">")
    
    def as_endian(self, endianness):
        if endianness.lower() == 'little':
            endianness = "<"
        elif endianness.lower() == 'big':
            endianness = '>'
        
        return EndiannessManager(self, endianness)
    
    ########################
    # VALIDATION UTILITIES #
    ########################
    def assert_equal(self, input_value, reference_value, value_name=None, formatter=None):
        if input_value != reference_value:
            if formatter is not None:
                input_value = formatter(input_value)
                reference_value = formatter(reference_value)

            if value_name is None:
                msg = f"Expected input to be '{reference_value}', but it was '{input_value}'"
            else:
                msg = f"Expected input '{value_name}' to be '{reference_value}', but it was '{input_value}'"
            raise ValueError(msg)
