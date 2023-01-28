import io

from ...serialization.BinaryTargets import Reader
from ...FileFormats.GFS.SubComponents.Physics.Binary.ContainerPayload import PhysicsPayload


def export_physics(gfs, bpy_obj):
    physics = PhysicsPayload()
    physics_blob = bpy_obj.data.GFSTOOLS_ModelProperties.physics_blob
    if len(physics_blob):
        stream = io.BytesIO()
        stream.write(bytes.fromhex(physics_blob))
        stream.seek(0)
        
        rdr = Reader(None)
        rdr.bytestream = stream
        rdr.rw_obj(physics, 0x01105100)
        
    # If there's any physics to export, put it on the container
    if physics.physics_bone_count or physics.collider_count or physics.physics_bone_link_count:
        gfs.physics_data = physics
