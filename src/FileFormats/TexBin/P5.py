from ...serialization.serializable import GFSSerializable


def align(size, alignment):
    return (alignment - (size % alignment)) % alignment


class ConfigurationDescriptor:
    def deserialize(rw, bin_count, tex_counts):
        config = rw.rw_bytestring(None, 0x40).rstrip(b'\x00')
        bin_count, tex_counts, _ = config.split(b',\r\n')
        return int(bin_count),  [int(t) for t in tex_counts.split(b',')]
    
    def serialize(rw, bin_count, tex_counts):
        config = str(bin_count).encode('ascii') + b",\r\n"
        config += ','.join([str(t) for t in tex_counts]).encode('ascii') + b",\r\n"
        config += (0x40-len(config))*b'\x00'
        rw.rw_bytestring(config, 0x40)
        
        return bin_count, tex_counts
    
    def count(rw, bin_count, tex_counts):
        rw.advance_offset(0x40)
        return bin_count, tex_counts


class ListElementDescriptor:
    def deserialize(rw, textures, start_idx, tex_count):
        for i in range(tex_count):
            tx = P5TextureBinElement()
            idx = start_idx + i
            if idx == len(textures):
                textures.append(tx)
            elif idx < len(textures):
                textures[idx] = tx
            else:
                raise ValueError("Discontinuous array read")
            rw.rw_obj(tx)
        rw.rw_bytestring(None, 0x100)
        return start_idx + tex_count
    
    def serialize(rw, textures, start_idx, tex_count):
        for i in range(tex_count):
            rw.rw_obj(textures[start_idx+i])
        rw.rw_bytestring(b'\x00'*0x100, 0x100)
        return start_idx + tex_count
    
    def count(rw, textures, start_idx, tex_count):
        for i in range(tex_count):
            rw.rw_obj(textures[start_idx+i])
        rw.rw_bytestring(b'\x00'*0x100, 0x100)
        return start_idx + tex_count


class P5TextureBinElement(GFSSerializable):
    def __init__(self):
        self.name = b""
        self.size = 0
        self.payload = b""
    
    def exbip_rw(self, rw):
        self.name = rw.rw_bytestring(self.name, 0xFC)
        self.size = rw.rw_uint32_le(self.size)
        self.payload = rw.rw_bytestring(self.payload, self.size + align(self.size, 0x40))


class P5TextureBin(GFSSerializable):
    def __init__(self):
        self.name = b''
        self.unknown_1 = 9
        self.bin_count = 0
        self.tex_counts = [0]
        self.textures   = []
    
    def exbip_rw(self, rw, ft):
        with rw.as_endian(">"):
            self.name = rw.rw_bytestring(self.name, 0xFC)
            self.unknown_1 = rw.rw_uint32(self.unknown_1)
            self.bin_count, self.tex_counts = rw.rw_descriptor(ConfigurationDescriptor, self.bin_count, self.tex_counts)
            
            running_count = 0
            running_count = self.rw_textures(rw, running_count, self.tex_counts[0])
            
            for i, c in enumerate(self.tex_counts[1:]):
                fp = ft.format(f"{i+1:0>2}")
                with type(rw)().FileIO(fp) as rw2:
                    running_count = self.rw_textures(rw2, running_count, c)
    
    def rw_textures(self, rw, running_count, tex_count):
        return rw.rw_descriptor(ListElementDescriptor, self.textures, running_count, tex_count)
    
    def add_texture(self, name, payload):
        elem = P5TextureBinElement()
        if isinstance(name, bytes):
            pass
        elif isinstance(name, str):
            name = name.encode("shift-jis")
        else:
            raise ValueError("Name is not 'bytes' or 'str'")
        
        if len(name) > 0xFC:
            raise ValueError("Name is {len(name)} bytes long; maximum is {252}")
        elem.name = name + (0xFC-len(name))*b'\x00'
        elem.size = len(payload)
        elem.payload = payload
        
        self.textures.append(elem)
        self.tex_counts[-1] += 1
