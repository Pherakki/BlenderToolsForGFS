class Blob:
    def __init__(self):
        self.data = b''
        
    def __repr__(self):
        return f"[GFS::Blob] {len(self.data)}"
    
    def exbip_rw(self, rw, version, size):
        self.data = rw.rw_bytestring(self.data, size)
