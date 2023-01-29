def import_0x000100F8(gfs, bpy_obj):
    if gfs.data_0x000100F8 is not None:
        if gfs.data_0x000100F8 != b'\x00\x00\x00\x01\x00\x00\x00\t\x00\x0eapp_uniq_emote\xfe\x8dSQ\x00\x00\x00\x03 \n\n':
            raise NotImplementedError("Found unexpected 0x000100F8 data. Please report this as an error, including the file that generated this error with your report")    
        bpy_obj.data.GFSTOOLS_ModelProperties.has_external_emt = True
