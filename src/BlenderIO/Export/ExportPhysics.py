import io

from ...serialization.BinaryTargets import Reader
from ...FileFormats.GFS.SubComponents.Physics.Binary.ContainerPayload import PhysicsPayload


def export_physics(gfs, bpy_obj):
    bone_names = set([node.name for node in gfs.bones])
    physics = PhysicsPayload()
    physics_blob = bpy_obj.data.GFSTOOLS_ModelProperties.physics_blob
    if len(physics_blob):
        stream = io.BytesIO()
        stream.write(bytes.fromhex(physics_blob))
        stream.seek(0)
        
        rdr = Reader(None)
        rdr.bytestream = stream
        rdr.rw_obj(physics, 0x01105100)

    # Remove physics bones for which the bone no longer exists
    for i, pbone in reversed(list(enumerate(physics.physics_bones))):
        if pbone.has_name:
            if pbone.name.string not in bone_names:
                # OK to delete at index because we're traversing the list backwards
                del physics.physics_bones[i]
                physics.physics_bone_count -= 1
                for j, blink in reversed(list(enumerate(physics.physics_bone_links))):
                    if blink.parent_physics_bone == i or blink.child_physics_bone == i:
                        del physics.physics_bone_links[j]
                        physics.physics_bone_link_count -= 1
                        
                    if blink.parent_physics_bone >= i:
                        blink.parent_physics_bone -= 1
                    if blink.child_physics_bone >= i:
                        blink.child_physics_bone -= 1

    # Remove colliders for which the bone no longer exists
    for i, collider in reversed(list(enumerate(physics.colliders))):
        if collider.has_name:
            if collider.name.string not in bone_names:
                # OK to delete at index because we're traversing the list backwards
                del physics.colliders[i]
                physics.collider_count -= 1
                
    # If there's any physics to export, put it on the container
    if physics.physics_bone_count or physics.collider_count or physics.physics_bone_link_count:
        gfs.physics_data = physics
