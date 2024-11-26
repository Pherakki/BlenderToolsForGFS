from ...serialization.serializable import GFSSerializable


class MetaphorTextureBinElement(GFSSerializable):
    def __init__(self):
        self.name = b''
        self.size = 0
        self.payload = b''

    def exbip_rw(self, rw):
        self.name = rw.rw_bytestring(self.name, 0x100)
        self.size = rw.rw_uint32(self.size)
        self.payload = rw.rw_bytestring(self.payload, self.size)


class MetaphorTextureBin(GFSSerializable):
    def __init__(self):
        self.texture_count = 0
        self.textures      = []
    
    def exbip_rw(self, rw):
        with rw.as_endian(">"):
            self.texture_count = rw.rw_uint32(self.texture_count)
            self.textures      = rw.rw_dynamic_objs(self.textures, MetaphorTextureBinElement, self.texture_count)

    def add_texture(self, name, payload):
        elem = MetaphorTextureBinElement()
        if isinstance(name, bytes):
            pass
        elif isinstance(name, str):
            name = name.encode("shift-jis")
        else:
            raise ValueError("Name is not 'bytes' or 'str'")
        
        elem.name = name + (0x100-len(name))*b'\x00'
        elem.size = len(payload)
        elem.payload = payload
        
        self.textures.append(elem)
        self.texture_count += 1
