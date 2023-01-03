from ......serialization.Serializable import Serializable


class TextureBinary(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.name = None
        self.filetype = 1 # DDS = 1, TGA = 2, TMX = 3, GXT = 6, GNF = 9, EPT = 12
        self.data_size = None
        self.data = None
        self.footer = 0x1010000
        
    def __repr__(self):
        return f"[GFD::TextureBinary] {self.name} {self.filetype} {self.data_size}"

    def read_write(self, rw, version):
        self.name      = rw.rw_uint16_sized_str(self.name)
        self.filetype  = rw.rw_uint16(self.filetype)
        self.data_size = rw.rw_uint32(self.data_size)
        
        self.data      = rw.rw_bytestring(self.data, self.data_size)
        self.footer    = rw.rw_uint32(self.footer)
        rw.assert_equal(self.footer, 0x1010000)
