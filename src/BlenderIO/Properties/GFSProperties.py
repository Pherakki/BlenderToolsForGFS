import bpy
from ..Utils.String import set_name_string


class GFSToolsGenericProperty(bpy.types.PropertyGroup):
    dname:  bpy.props.StringProperty(name="", default="New Property")
    dtype: bpy.props.EnumProperty(items=(
            ("INT32",       "Int32",     "A single 32-bit signed integer"        ),
            ("FLOAT32",     "Float32",   "A single 32-bit floating-point number."),
            ("UINT8",       "UInt8",     "A single 8-bit unsigned integer"       ),
            ("STRING",      "String",    "A UTF8-encoded string"                 ),
            ("UINT8VEC3",   "UInt8*3",   "A 3-vector of 8-bit unsigned integers" ),
            ("UINT8VEC4",   "UInt8*4",   "A 4-vector of 8-bit unsigned integers" ),
            ("FLOAT32VEC3", "Float32*3", "A 3-vector of floating-point numbers"  ),
            ("FLOAT32VEC4", "Float32*4", "A 4-vector of floating-point numbers"  ),
            ("BYTES",       "Bytes",     "A blob of bytes."                      )
        ), name="", default="INT32")

    int32_data:       bpy.props.IntProperty(name="")
    float32_data:     bpy.props.FloatProperty(name="")
    uint8_data:       bpy.props.IntProperty(name="", min=0, max=255)
    string_data:      bpy.props.StringProperty(name="")
    uint8vec3_data:   bpy.props.IntVectorProperty(name="", size=3, min=0, max=255)
    uint8vec4_data:   bpy.props.IntVectorProperty(name="", size=4, min=0, max=255)
    float32vec3_data: bpy.props.FloatVectorProperty(name="", size=3)
    float32vec4_data: bpy.props.FloatVectorProperty(name="", size=4)
    bytes_data:       bpy.props.StringProperty(name="", default="0x00")
    
    @staticmethod
    def extract_data(prop, errorlog):
        if   prop.dtype == "INT32":
            dtype = 1; prop_data = prop.int32_data
        elif prop.dtype == "FLOAT32":
            dtype = 2; prop_data = prop.float32_data
        elif prop.dtype == "UINT8":
            dtype = 3; prop_data = prop.uint8_data
        elif prop.dtype == "STRING":
            dtype = 4; prop_data = set_name_string("Property String Data", prop.string_data, "utf8", errorlog)
        elif prop.dtype == "UINT8VEC3":
            dtype = 5; prop_data = prop.uint8vec3_data
        elif prop.dtype == "UINT8VEC4":
            dtype = 6; prop_data = prop.uint8vec4_data
        elif prop.dtype == "FLOAT32VEC3":
            dtype = 7; prop_data = prop.float32vec3_data
        elif prop.dtype == "FLOAT32VEC4":
            dtype = 8; prop_data = prop.float32vec4_data
        elif prop.dtype == "BYTES":
            bytes_data = prop.bytes_data
            if bytes_data.startswith('0x'):
                bytes_data = bytes_data[2:]
            
            # Catch an error here
            bytes_data = bytes.fromhex(bytes_data)
            
            dtype = 9
            prop_data = prop.bytes_data
        
        return prop.dname, dtype, prop_data
