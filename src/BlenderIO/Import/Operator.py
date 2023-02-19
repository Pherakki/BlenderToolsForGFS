import os

import bpy
from bpy_extras.io_utils import ImportHelper

from ...FileFormats.GFS import GFSInterface, UnsupportedVersionError, ParticlesError, HasParticleDataError
from .Import0x000100F8 import import_0x000100F8
from .ImportAnimations import create_rest_pose, import_animations
from .ImportMaterials import import_materials
from .ImportModel import import_model
from .ImportPinnedModel import import_pincushion_model
from .ImportPhysics import import_physics
from .ImportTextures import import_textures
from ..WarningSystem import handle_warning_system, ErrorLogger
from ..UI.HelpWindows import HelpWindow


class ImportGFS(bpy.types.Operator, ImportHelper):
    bl_idname = 'import_file.import_gfs'
    bl_label = 'Persona 5 Royal - PC (.GMD, .GFS)'
    bl_options = {'REGISTER', 'UNDO'}
    filename_ext = ".GMD"


    filter_glob: bpy.props.StringProperty(
                                              default='*.GMD;*.GFS',
                                              options={'HIDDEN'},
                                          )
    
    @handle_warning_system("The file you are trying to import.")
    def import_file(self, context, filepath):
        bpy.ops.object.select_all(action='DESELECT')
        
        # Try to load file and log any errors...
        errorlog = ErrorLogger()
        try:
            gfs = GFSInterface.from_file(filepath) 
        except UnsupportedVersionError as e:
            errorlog.log_error_message(f"The file you attempted to load is an unsupported version: {str(e)}.")
        except ParticlesError:
            errorlog.log_error_message("The file you attempted to load contains EPL data, which cannot currently be loaded.")
        except HasParticleDataError:
            errorlog.log_error_message("The file you attempted to load contains EPL data, which cannot currently be loaded.")
        if len(gfs.morphs):
            errorlog.log_error_message("The file you attempted to load contains morph data, which cannot currently be loaded.")
       
        # Report any file-loading errors
        if len(errorlog.errors):
            errorlog.digest_errors()
            return {'ERROR'}

        # Now import file data to Blender
        textures  = import_textures(gfs)
        materials = import_materials(gfs, textures)
        armature, gfs_to_bpy_bone_map = import_model(gfs, os.path.split(filepath)[1].split('.')[0])
        
        create_rest_pose(gfs, armature, gfs_to_bpy_bone_map)
        filename = os.path.splitext(os.path.split(filepath)[1])[0]
        import_animations(gfs, armature, filename)
        
        import_physics(gfs, armature)
        import_0x000100F8(gfs, armature)
        
        # Report any warnings that were logged
        errorlog.digest_warnings()

        return {'FINISHED'}
    
    def execute(self, context):
        self.import_file(context, self.filepath)

        return {'FINISHED'}


class ImportGAP(bpy.types.Operator, ImportHelper):
    bl_idname = 'import_file.import_gap'
    bl_label = 'Persona 5 Royal - PC (.GAP)'
    bl_options = {'REGISTER', 'UNDO'}
    filename_ext = "*.GAP"

    def fetch_armatures(self, context):
        armature_list = []
        for obj in bpy.data.objects:
            if obj.type == "ARMATURE":
                armature_list.append((obj.name, obj.name, obj.name, "OUTLINER_OB_ARMATURE", len(armature_list)))
        return tuple(armature_list)
    
    armature_name: bpy.props.EnumProperty(items=fetch_armatures,
                                     name="Armature")
    
    filter_glob: bpy.props.StringProperty(
                                              default="*.GAP",
                                              options={'HIDDEN'},
                                          )
    
    def find_selected_model(self, context):
        sel_obj = context.active_object
        if sel_obj is None:
            return None
        while sel_obj.parent is not None:
            sel_obj = sel_obj.parent
        if sel_obj.type == "ARMATURE":
            return sel_obj
        return None

    @handle_warning_system("The file you are trying to import.")
    def import_file(self, context, armature, filepath):
        bpy.ops.object.select_all(action='DESELECT')

        # Try to load file and log any errors...
        errorlog = ErrorLogger()            
        if self.armature_name is None:
            errorlog.log_error_message("No armatures exist in the scene. Animations cannot be imported")
        
        # Report an error if there's no armature
        if len(errorlog.errors):
            errorlog.digest_errors()
            return {'CANCELLED'}
        
        try:
            gfs = GFSInterface.from_file(filepath) 
        except UnsupportedVersionError as e:
            errorlog.log_error_message(f"The file you attempted to load is an unsupported version: {str(e)}.")
        except ParticlesError:
            errorlog.log_error_message("The file you attempted to load contains EPL data, which cannot currently be loaded.")
        except HasParticleDataError:
            errorlog.log_error_message("The file you attempted to load contains EPL data, which cannot currently be loaded.")

        # Report any file-loading errors
        if len(errorlog.errors):
            errorlog.digest_errors()
            return {'ERROR'}
        
        # Now import file data to Blender
        filename = os.path.splitext(os.path.split(filepath)[1])[0]
        import_animations(gfs, armature, filename)
        
        # Report any warnings that were logged
        errorlog.digest_warnings()

        return {'FINISHED'}
    
    def execute(self, context):
        self.import_file(context, bpy.data.objects[self.armature_name], self.filepath)

        return {'FINISHED'}
