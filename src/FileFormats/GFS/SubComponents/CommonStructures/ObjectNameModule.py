from .....serialization.formatters import HEX32_formatter
from ...Utils.StringHashing import gfs_string_hash


class ObjectName:
    ################
    # CONSTRUCTORS #
    ################
    def __init__(self):
        self.string      = None
        self.string_hash = None

    @classmethod
    def from_string(cls, name, encoding):
        instance = cls()
        instance.set_string(name, encoding)
        return instance
        
    @classmethod
    def from_bytestring(cls, name):
        instance = cls()
        instance.set_bytestring(name)
        return instance
    
    @classmethod
    def from_name(cls, name, encoding="utf8"):
        if isinstance(name, bytes) or isinstance(name, bytearray):
            return cls.from_bytestring(name)
        elif isinstance(name, str):
            return cls.from_string(name, encoding)
        else:
            raise ValueError("Provided value is not a 'str' or bytes-like")
    
    ##################
    # CLASS METADATA #
    ##################
    def __repr__(self):
        return f"[GFS::ObjName] {HEX32_formatter(self.string_hash)} {self.string}"
    
    ################
    # RW FUNCTIONS #
    ################
    def exbip_rw(self, rw, version, null_terminated=False):
        self.string = rw.rw_uint16_sized_bstr(self.string)
        if len(self.string) and version > 0x01080010:
            if (null_terminated and (version > 0x01105100)):
                rw.rw_uint8(0)
            self.string_hash = rw.rw_uint32(self.string_hash)

    # ###################
    # # INTERFACE FUNCS #
    # ###################
    def set_bytestring(self, value):
        self.string      = value
        self.string_hash = gfs_string_hash(value)

    def set_string(self, value, encoding="utf8"):
        self.set_bytestring(value.encode(encoding))
 