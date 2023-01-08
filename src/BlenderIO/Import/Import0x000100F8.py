def import_0x000100F8(gfs, bpy_obj):
    if gfs.data_0x000100F8 is not None:
        string_data = '0x' + ''.join(f"{elem:0>2X}" for elem in gfs.data_0x000100F8.data)
        bpy_obj["0x000100F8"] = string_data
