from .....serialization.Serializable import Serializable


class Blob(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.data = b''
        
    def __repr__(self):
        return f"[GFS::Blob] {len(self.data)}"
    
    def read_write(self, rw, version, size):
        self.data = rw.rw_bytestring(self.data, size)
