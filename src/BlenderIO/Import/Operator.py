import os

import bpy
from bpy_extras.io_utils import ImportHelper

from ...FileFormats.GFS import GFSInterface
from ..Utils.ErrorPopup import handle_errors
from .Import0x000100F8 import import_0x000100F8
from .ImportAnimations import create_rest_pose, import_animations
from .ImportMaterials import import_materials
from .ImportModel import import_pincushion_model
from .ImportPhysics import import_physics
from .ImportTextures import import_textures


class ImportGFS(bpy.types.Operator, ImportHelper):
    bl_idname = 'import_file.import_gfs'
    bl_label = 'Persona 5 Royal - PC (.GMD)'
    bl_options = {'REGISTER', 'UNDO'}
    filename_ext = "*.GMD"


    # filter_glob: bpy.props.StringProperty(
    #                                          default="*.GMD",
    #                                          options={'HIDDEN'},
    #                                      )
    
    def import_file(self, context, filepath):
        bpy.ops.object.select_all(action='DESELECT')

        gfs = GFSInterface.from_file(filepath)
        
        textures  = import_textures(gfs)
        materials = import_materials(gfs, textures)
        armature  = import_pincushion_model(gfs, os.path.split(filepath)[1].split('.')[0])
        
        create_rest_pose(gfs, armature)
        filename = os.path.splitext(os.path.split(filepath)[1])[0]
        import_animations(gfs, armature, filename)
        
        import_physics(gfs, armature)
        import_0x000100F8(gfs, armature)

        return {'FINISHED'}
    
    @handle_errors
    def execute(self, context):
        self.import_file(context, self.filepath)

        return {'FINISHED'}
