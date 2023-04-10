import io

from ...serialization.BinaryTargets import Reader
from ...FileFormats.GFS.SubComponents.Physics.Binary.ContainerPayload import PhysicsPayload
from ...FileFormats.GFS.SubComponents.Physics.Binary.PhysicsBoneBinary import PhysicsBoneBinary
from ...FileFormats.GFS.SubComponents.Physics.Binary.ColliderBinary import ColliderBinary
from ...FileFormats.GFS.SubComponents.Physics.Binary.BoneLinkBinary import PhysicsBoneLinkBinary


def export_physics(gfs, bpy_obj, errorlog):
    props = bpy_obj.data.GFSTOOLS_ModelProperties.physics  
    if not props.has_physics:
        return

    bone_names = set([node.name for node in gfs.bones])
    physics = PhysicsPayload()

    # Export physics 
    physics.unknown_0x00 = props.unknown_0x00
    physics.unknown_0x04 = props.unknown_0x04
    physics.unknown_0x08 = props.unknown_0x08
    physics.unknown_0x0C = props.unknown_0x0C
    physics.unknown_0x10 = props.unknown_0x10
    
    for b_bone in props.bones:
        bone = PhysicsBoneBinary()
        bone.has_name = b_bone.has_name
        bone.name = bone.name.from_name(b_bone.name)
        bone.unknown_0x00 = b_bone.unknown_0x00
        bone.unknown_0x04 = b_bone.unknown_0x04
        bone.unknown_0x08 = b_bone.unknown_0x08
        bone.unknown_0x0C = b_bone.unknown_0x0C
        bone.unknown_0x14 = b_bone.nameless_data
        physics.physics_bones.append(bone)
    physics.physics_bone_count = len(physics.physics_bones)
    
    for b_cldr in props.colliders:
        cldr = ColliderBinary()
        cldr.has_name = b_cldr.has_name
        cldr.name = cldr.name.from_name(b_cldr.name)
        cldr.collider_type = 0 if b_cldr.dtype == "Sphere" else 1
        cldr.capsule_radius = b_cldr.radius
        cldr.capsule_height = b_cldr.height
        cldr.unknown_0x0A = [*b_cldr.r1, *b_cldr.r2, *b_cldr.r3, *b_cldr.r4]
        physics.colliders.append(cldr)
    physics.collider_count = len(physics.colliders)
    
    for i, b_link in enumerate(props.links):
        link = PhysicsBoneLinkBinary()
        link.parent_physics_bone = b_link.parent
        link.child_physics_bone  = b_link.child
        link.mass                = b_link.mass
        link.unknown_0x04        = b_link.unknown_0x04
        link.radius              = b_link.radius
        physics.physics_bone_links.append(link)
        
        if link.parent_physics_bone == -1:
            errorlog.log_error_message(f"Armature '{bpy_obj.name}' has a parent bone index of -1 on physics link {i}. Either remove this link from the GFS Physics or set the index to a valid physics bone index")
        if link.child_physics_bone == -1:
            errorlog.log_error_message(f"Armature '{bpy_obj.name}' has a child bone index of -1 on physics link {i}. Either remove this link from the GFS Physics or set the index to a valid physics bone index")
        
        if link.parent_physics_bone >= physics.physics_bone_count:
            errorlog.log_warning_message(f"Armature '{bpy_obj.name}' has a parent bone index that exceeds the total number of physics bones ({physics.physics_bone_count}) on physics link {i}")
        if link.child_physics_bone >= physics.physics_bone_count:
            errorlog.log_warning_message(f"Armature '{bpy_obj.name}' has a child bone index that exceeds the total number of physics bones ({physics.physics_bone_count}) on physics link {i}")
    physics.physics_bone_link_count = len(physics.physics_bone_links)

    # Remove physics bones for which the bone no longer exists
    for i, pbone in reversed(list(enumerate(physics.physics_bones))):
        if pbone.has_name:
            if pbone.name.string not in bone_names:
                errorlog.log_warning_message(f"Armature '{bpy_obj.name}' has bone physics attached to the non-existent bone '{pbone.name.string}'. This has not been exported")
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
                errorlog.log_warning_message(f"Armature '{bpy_obj.name}' has collider physics attached to the non-existent bone '{collider.name.string}'. This has not been exported")
                # OK to delete at index because we're traversing the list backwards
                del physics.colliders[i]
                physics.collider_count -= 1
                
    # If there's any physics to export, put it on the container
    if physics.physics_bone_count or physics.collider_count or physics.physics_bone_link_count:
        gfs.physics_data = physics
