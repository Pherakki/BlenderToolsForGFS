import io

from ...serialization.BinaryTargets import Writer


def import_physics(gfs, bpy_obj):
    if gfs.physics_data is not None:
        stream = io.BytesIO()
        wtr = Writer(None)
        wtr.bytestream = stream
        wtr.rw_obj(gfs.physics_data, 0x01105100)
        stream.seek(0)
        
        string_data = '0x' + ''.join(f"{elem:0>2X}" for elem in stream.read())
        bpy_obj["physics"] = string_data
