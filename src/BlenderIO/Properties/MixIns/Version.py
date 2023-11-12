import struct
import bpy


def version_getter(self):
    v = struct.unpack('I', struct.pack('i', self.int_version))[0]
    return f"0x{v:0>8X}"

def version_setter(self, value):
    bad_string = ValueError("Version numbers must be a hexadecimal string starting with '0x' and followed by exactly 8 hexadecimal digits")
    
    print(value)
    if value[:2] != "0x" or len(value) != 10:
        raise bad_string
    
    try:
        self.int_version = struct.unpack('i', struct.pack('I', int(value, 16)))[0]
    except:
        raise bad_string


class GFSVersionedProperty():
    int_version:    bpy.props.IntProperty(name="Integer Version", default=0x01105100)
    version:         bpy.props.StringProperty(name="Version", get=version_getter, set=version_setter)
