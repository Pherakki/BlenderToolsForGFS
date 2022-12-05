from ....serialization.Serializable import Serializable
from ....serialization.utils import safe_format, hex32_format


class TextureBinary(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.name = None
        self.pixel_format = 1 # Always 1 regardless of DXT encoding?!
        self.data_size = None
        self.data = None
        self.footer = 0x1010000
        
    def __repr__(self):
        return f"[GFD::TexturesContainer::Texture] {self.name} {safe_format(self.pixel_format, hex32_format)} {self.data_size}"

    def read_write(self, rw):
        self.name         = rw.rw_uint16_sized_str(self.name)
        self.pixel_format = rw.rw_uint16(self.pixel_format)
        self.data_size = rw.rw_uint32(self.data_size)
        
        self.data = rw.rw_bytestring(self.data, self.data_size)
        self.footer = rw.rw_uint32(self.footer)
        rw.assert_equal(self.footer, 0x1010000)
