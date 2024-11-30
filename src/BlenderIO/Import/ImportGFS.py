from .ImportTextures import import_textures
from .ImportMaterials import import_materials
from . import ImportModel
from .ImportAnimations import create_rest_pose, import_animations
from .ImportPhysics import import_physics
from .Import0x000100F8 import import_0x000100F8
from . import ImportEPLs


def import_gfs_object(gfs, raw_gfs, name, external_textures, errorlog, import_policies):
    has_external_tex = len(external_textures) > 0
    shares_textures  = False
    # 'shares_textures' should be set to true in some cases
    textures, unused_textures = import_textures(gfs, external_textures, shares_textures, errorlog)
    materials = import_materials(gfs, textures, errorlog)
    
    armature, gfs_to_bpy_bone_map = ImportModel.import_model(gfs, name, materials, errorlog, import_policies.merge_vertices, import_policies.bone_pose, raw_gfs, import_policies)
    mprops = armature.data.GFSTOOLS_ModelProperties
    if    shares_textures:  mprops.texture_mode = "BORROW"
    elif  has_external_tex: mprops.texture_mode = "MULTIFILE"
    else:                   mprops.texture_mode = "EMBEDDED"
    
    for nm, img in unused_textures.items():
        utex = mprops.unused_textures.add()
        utex.name    = nm
        utex.texture = img
        utex.export  = True
    
    create_rest_pose(gfs, armature, gfs_to_bpy_bone_map)
    import_animations(gfs, armature, name, is_external=False, gfs_to_bpy_bone_map=gfs_to_bpy_bone_map, import_policies=import_policies, errorlog=errorlog)
    
    import_physics(gfs, armature, errorlog)
    import_0x000100F8(gfs, armature)
    
    ImportEPLs.import_epls(gfs, armature, gfs_to_bpy_bone_map, errorlog, import_policies)

    for nm, (bpy_material, gfs_material) in materials.items():
        bpy_material.GFSTOOLS_MaterialProperties.build_default_nodetree()

    return armature
