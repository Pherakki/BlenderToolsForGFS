from .ImportTextures import import_textures
from .ImportMaterials import import_materials
from . import ImportModel
from .ImportAnimations import create_rest_pose, import_animations
from .ImportPhysics import import_physics
from .Import0x000100F8 import import_0x000100F8
from . import ImportEPLs


def import_gfs_object(gfs, raw_gfs, name, errorlog, import_policies):
    textures  = import_textures(gfs)
    materials = import_materials(gfs, textures, errorlog)
    armature, gfs_to_bpy_bone_map = ImportModel.import_model(gfs, name, materials, errorlog, import_policies.merge_vertices, import_policies.bone_pose, raw_gfs, import_policies)
    
    create_rest_pose(gfs, armature, gfs_to_bpy_bone_map)
    import_animations(gfs, armature, name, is_external=False, gfs_to_bpy_bone_map=gfs_to_bpy_bone_map, import_policies=import_policies)
    
    import_physics(gfs, armature)
    import_0x000100F8(gfs, armature)
    
    ImportEPLs.import_epls(gfs, armature, gfs_to_bpy_bone_map, errorlog, import_policies)

    return armature
