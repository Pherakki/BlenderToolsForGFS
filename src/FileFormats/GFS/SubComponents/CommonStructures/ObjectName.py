from .....serialization.Serializable import Serializable
from .....serialization.utils import safe_format, hex32_format
from ...Utils.StringHashing import gfs_string_hash

all_strings = set()
all_strings_and_hashes = set()

class ObjectName(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.string_size = None
        self.string      = None
        self.string_hash = None
    
    @classmethod
    def from_name(cls, name, encoding="utf8"):
        instance = cls()
        
        instance.string = name
        
        name_bytestring = instance.string_encode(encoding)
        instance.string_size = len(name_bytestring)
        instance.string_hash = gfs_string_hash(name_bytestring)
        
        return instance
    
    def __repr__(self):
        return f"[GFS::ObjName] {safe_format(self.string_hash, hex32_format)} {self.string}"
    
    def read_write(self, rw, version, encoding="utf8"):
        # TODO: Replace if statement with something more self-documenting
        self.string_size = rw.rw_uint16(self.string_size)
        if rw.mode() == "read":
            self.string = self._read_string(rw, self.string, encoding)
        else:
            self.string = self._write_string(rw, self.string, encoding)
        
        if version > 0x01080010:
            self.rw_hash(rw, encoding)

    def rw_hash(self, rw, encoding):
        if self.string_size > 0:
            self.string_hash = rw.rw_uint32(self.string_hash)
            return
            all_strings.add(self.string)
            all_strings_and_hashes.add((self.string, self.string_hash))
            
            string_hash = gfs_string_hash(self.string_encode(encoding))
            if string_hash != self.string_hash:
                raise ValueError(f"The hash of '{self.string}' does not match the generated hash:\n"\
                                 f"READ: {self.string_hash}\n"\
                                 f"GEN : {string_hash}")


    # Need to handle some known incorrectly-encoded strings, so we dispatch
    # encoding/decoding out to some funcs that are aware of these special exceptions
    def _read_string(self, rw, string, encoding):
        tmp = rw.rw_bytestring(string, self.string_size)
        try:
            out = tmp.decode(encoding)
        except UnicodeDecodeError as e:
            if tmp[-28:] == b'DirectX \xe3\x83\x9e\xe3\x83\x8d\xe3\x83\xbc\xe3\x82\xb8\xe3\x83\xa3.\x97L\x8c\xf8':
                out = tmp[:-4].decode("utf-8") + tmp[-4:].decode("shift-jis")
            else:
                raise Exception(f"Unable to decode '{tmp}' with encoding '{encoding}': {e}")
        return out
    
    def string_encode(self, encoding):
        if self.string[-16:] == "DirectX マネージャ.有効":
            out = self.string[:-2].encode("utf-8") + self.string[-2:].encode('shift-jis')
        else:
            out = self.string.encode(encoding)
        return out
    
    def _write_string(self, rw, string, encoding):
        rw.rw_bytestring(self.string_encode(encoding), self.string_size)        
        return string
