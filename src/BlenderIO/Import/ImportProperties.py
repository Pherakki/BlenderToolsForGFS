from ..Utils.String import get_name_string


def import_properties(gfs_properties, bpy_properties, errorlog):
    for prop in gfs_properties:
        item = bpy_properties.add()
        item.dname = get_name_string("GFS Property", prop.name_bytes, "utf8", errorlog)
        if prop.type == 1:
            item.dtype = "INT32"
            item.int32_data = prop.data
        elif prop.type == 2:
            item.dtype = "FLOAT32"
            item.float32_data = prop.data
        elif prop.type == 3:
            item.dtype = "UINT8"
            item.uint8_data = prop.data
        elif prop.type == 4:
            item.dtype = "STRING"
            item.string_data = get_name_string(f"String GFS Property '{item.dname}' data", prop.data, "utf8", errorlog)
        elif prop.type == 5:
            item.dtype = "UINT8VEC3"
            item.uint8vec3_data = prop.data  
        elif prop.type == 6:
            item.dtype = "UINT8VEC4"
            item.uint8vec4_data = prop.data
        elif prop.type == 7:
            item.dtype = "FLOAT32VEC3"
            item.float32vec3_data = prop.data
        elif prop.type == 8:
            item.dtype = "FLOAT32VEC4"
            item.float32vec4_data = prop.data
        elif prop.type == 9:
            item.dtype = "BYTES"
            item.bytes_data = '0x' + ''.join(rf"{e:0>2X}" for e in prop.data)
