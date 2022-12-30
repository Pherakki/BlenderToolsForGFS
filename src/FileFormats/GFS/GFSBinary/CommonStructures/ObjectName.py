from .....serialization.Serializable import Serializable
from .....serialization.utils import safe_format, hex32_format
from ...Utils.StringHashing import gfs_string_hash

all_strings = set()
all_strings_and_hashes = set()

class ObjectName(Serializable):
    ENCODING = 'utf8'
    
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.string_size = None
        self.string      = None
        self.string_hash = None
    
    @classmethod
    def from_name(cls, name):
        instance = cls()
        
        name_bytestring = name.encode(cls.ENCODING)
        instance.string = name
        instance.string_size = len(name_bytestring)
        instance.string_hash = gfs_string_hash(name_bytestring)
        
        return instance
    
    def __repr__(self):
        return f"[GFS::ObjName] {safe_format(self.string_hash, hex32_format)} {self.string}"
    
    def read_write(self, rw, version):
        # TODO: Replace if statement with something more self-documenting
        self.string_size = rw.rw_uint16(self.string_size)
        self.string      = rw.rw_str(self.string, self.string_size, encoding=self.ENCODING)
        if version > 0x01080010:
            self.rw_hash(rw)

    def rw_hash(self, rw):
        if self.string_size > 0:
            self.string_hash = rw.rw_uint32(self.string_hash)
            all_strings.add(self.string)
            all_strings_and_hashes.add((self.string, self.string_hash))
            
            string_hash = gfs_string_hash(self.string.encode(self.ENCODING))
            if string_hash != self.string_hash:
                raise ValueError(f"The hash of '{self.string}' does not match the generated hash:\n"\
                                 f"READ: {self.string_hash}\n"\
                                 f"GEN : {string_hash}")
