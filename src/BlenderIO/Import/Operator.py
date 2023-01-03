import os

import bpy
from bpy_extras.io_utils import ImportHelper

from ...FileFormats.GFS import GFSInterface
from ..Utils.ErrorPopup import handle_errors
from .ImportAnimations import create_rest_pose, import_animations
from .ImportMaterials import import_materials
from .ImportModel import import_pincushion_model
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
        
        textures                = import_textures(gfs)
        materials               = import_materials(gfs, textures)
        armature, bind_matrices = import_pincushion_model(gfs, os.path.split(filepath)[1].split('.')[0])
        
        create_rest_pose(armature, gfs.bones, bind_matrices)
        filename = os.path.splitext(os.path.split(filepath)[1])[0]
        # To adapt this to pure animation import: need to extract the info in the "model GFS"
        # from Blender somehow
        # "model gfs" is used to find the name and rest pose of each node
        # HOWEVER this appears to be a bug and should *also* get the bind pose
        # So it should be sufficient to:
        # - Only pass in an armature
        # - Check for an animation called "rest_pose" on the armature
        # - Pull out the rest pose data from the "rest_pose" action if it exists,
        #   else just use default identity element values
        # - Pull out the bind pose matrix _via_ the raw armature bone matrices
        # - The animations can then be constructed from those three bits of data
        import_animations(gfs, gfs, armature, filename)
        return {'FINISHED'}
    
    @handle_errors
    def execute(self, context):
        self.import_file(context, self.filepath)

        return {'FINISHED'}
