class TextureBinary:
    def __init__(self):
        super().__init__()
        
        self.name = None
        self.filetype = 1 # DDS = 1, TGA = 2, TMX = 3, GXT = 6, GNF = 9, EPT = 12
        self.data_size = None
        self.data = None
        self.unknown_1 = 1
        self.unknown_2 = 1
        self.unknown_3 = 0
        self.unknown_4 = 0
        
    def __repr__(self):
        return f"[GFD::TextureBinary] {self.name} {self.filetype} {self.data_size}"

    def exbip_rw(self, rw, version):
        self.name      = rw.rw_uint16_sized_bstr(self.name)  # Shift-JIS encoded
        self.filetype  = rw.rw_uint16(self.filetype)
        self.data_size = rw.rw_uint32(self.data_size)
        
        self.data      = rw.rw_bytestring(self.data, self.data_size)
        self.unknown_1 = rw.rw_uint8(self.unknown_1)
        self.unknown_2 = rw.rw_uint8(self.unknown_2)
        self.unknown_3 = rw.rw_uint8(self.unknown_3)
        self.unknown_4 = rw.rw_uint8(self.unknown_4)
