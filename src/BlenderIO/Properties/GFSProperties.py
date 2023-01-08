import bpy


class GFSToolsGenericProperty(bpy.types.PropertyGroup):
    dname:  bpy.props.StringProperty(name="", default="New Property")
    dtype: bpy.props.EnumProperty(items=(
            ("UINT32",      "UInt32",    "A single 32-bit unsigned integer"      ),
            ("FLOAT32",     "Float32",   "A single 32-bit floating-point number."),
            ("UINT8",       "UInt8",     "A single 8-bit unsigned integer"       ),
            ("STRING",      "String",    "A UTF8-encoded string"                 ),
            ("UINT8VEC3",   "UInt8*3",   "A 3-vector of 8-bit unsigned integers" ),
            ("UINT8VEC4",   "UInt8*4",   "A 4-vector of 8-bit unsigned integers" ),
            ("FLOAT32VEC3", "Float32*3", "A 3-vector of floating-point numbers"  ),
            ("FLOAT32VEC4", "Float32*4", "A 4-vector of floating-point numbers"  ),
            ("BYTES",       "Bytes",     "A blob of bytes."                      )
        ), name="", default="UINT32")

    uint32_data:      bpy.props.IntProperty(name="", min=0)
    float32_data:     bpy.props.FloatProperty(name="")
    uint8_data:       bpy.props.IntProperty(name="", min=0, max=255)
    string_data:      bpy.props.StringProperty(name="")
    uint8vec3_data:   bpy.props.IntVectorProperty(name="", size=3, min=0, max=255)
    uint8vec4_data:   bpy.props.IntVectorProperty(name="", size=4, min=0, max=255)
    float32vec3_data: bpy.props.FloatVectorProperty(name="", size=3)
    float32vec4_data: bpy.props.FloatVectorProperty(name="", size=4)
    bytes_data:       bpy.props.StringProperty(name="", default="0x00")
