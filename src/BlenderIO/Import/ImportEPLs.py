import io

from ...serialization.BinaryTargets import Writer


def import_epls(gfs, armature, gfs_to_bpy_bone_map):
    for epl in gfs.epls:
        if epl.node == 0:
            props = armature.data.GFSTOOLS_NodeProperties
        else:
            # Get bone
            bpy_bone_idx = gfs_to_bpy_bone_map[epl.node]
            bpy_bone     = armature.data.bones[bpy_bone_idx]
            props        = bpy_bone.GFSTOOLS_NodeProperties
        
        # Write the EPL to a blob
        stream = io.BytesIO()
        wtr = Writer(None)
        wtr.bytestream = stream
        wtr.rw_obj(epl.binary, 0x01105100)
        stream.seek(0)
        
        # Add blob
        item = props.epls.add()
        item.blob = ''.join(f"{elem:0>2X}" for elem in stream.read())
