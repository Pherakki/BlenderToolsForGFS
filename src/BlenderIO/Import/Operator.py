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
from .ImportEPLs import import_epls
from ..WarningSystem import handle_warning_system, ErrorLogger
from ..UI.HelpWindows import HelpWindow


def set_fps(self, context):
    if self.set_fps:
        context.scene.render.fps = 30

def define_set_fps():
    return bpy.props.BoolProperty(
        name="Set Blender Scene FPS to 30",
        description="Set the animation framerate of the current scene to 30, so that imported animations display at the correct speed",
        default=False
    )

class ImportGFS(bpy.types.Operator, ImportHelper):
    bl_idname = 'import_file.import_gfs'
    bl_label = 'Persona 5 Royal - PC (.GMD, .GFS)'
    bl_options = {'REGISTER', 'UNDO'}
    filename_ext = ".GMD"


    debug_mode: bpy.props.BoolProperty(
                                           default=False,
                                           options={'HIDDEN'},
                                      )

    filter_glob: bpy.props.StringProperty(
                                              default='*.GMD;*.GFS',
                                              options={'HIDDEN'},
                                          )
    
    set_fps: define_set_fps()
    
    merge_vertices: bpy.props.BoolProperty(
        name="Merge Vertices",
        description="Merge vertices with the same position data such that "\
                    "they form a smooth mesh that Blender can more accurately "\
                    "calculate normal and tangent vectors for. Merged GFS "\
                    "vertices become loops of the Blender vertices. Note that "\
                    "any vertices that are not part of faces are currently "
                    "dropped by this feature",
        default=True
    )
    
    @handle_warning_system("The file you are trying to import.")
    def import_file(self, context, filepath):
        if bpy.context.view_layer.objects.active is not None:        
            bpy.ops.object.mode_set(mode="OBJECT")
        bpy.ops.object.select_all(action='DESELECT')
        
        # Try to load file and log any errors...
        errorlog = ErrorLogger()
        warnings = []
        try:
            gfs = GFSInterface.from_file(filepath, warnings=warnings) 
        except UnsupportedVersionError as e:
            errorlog.log_error_message(f"The file you attempted to load is an unsupported version: {str(e)}.")

        # Add any file-loading warnings to the warnings list
        for warning_msg in warnings:
            errorlog.log_warning_message(warning_msg)
        
        # Report any file-loading errors
        if len(errorlog.errors):
            errorlog.digest_errors(self.debug_mode)
            return {'CANCELLED'}

        # Now import file data to Blender
        textures  = import_textures(gfs)
        materials = import_materials(gfs, textures, errorlog)
        armature, gfs_to_bpy_bone_map, mesh_node_map = import_model(gfs, os.path.split(filepath)[1].split('.')[0], materials, errorlog, self.merge_vertices)
        
        create_rest_pose(gfs, armature, gfs_to_bpy_bone_map)
        filename = os.path.splitext(os.path.split(filepath)[1])[0]
        import_animations(gfs, armature, filename, gfs_to_bpy_bone_map)
        
        import_physics(gfs, armature)
        import_0x000100F8(gfs, armature)
        
        import_epls(gfs, armature, gfs_to_bpy_bone_map, mesh_node_map)
        
        set_fps(self, context)
        
        # Report any warnings that were logged
        if len(errorlog.warnings):
            errorlog.digest_warnings(self.debug_mode)
            self.report({"INFO"}, "Import successful, with warnings.")
        else:
            self.report({"INFO"}, "Import successful.")
        
        return {'FINISHED'}
    
    def execute(self, context):
        return self.import_file(context, self.filepath)


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

    debug_mode: bpy.props.BoolProperty(
                                           default=False,
                                           options={'HIDDEN'},
                                      )
    
    set_fps: define_set_fps()
    
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
        if bpy.context.view_layer.objects.active is not None:        
            bpy.ops.object.mode_set(mode="OBJECT")
        bpy.ops.object.select_all(action='DESELECT')

        # Try to load file and log any errors...
        errorlog = ErrorLogger()            
        if self.armature_name is None:
            errorlog.log_error_message("No armatures exist in the scene. Animations cannot be imported")
        
        # Report an error if there's no armature
        if len(errorlog.errors):
            errorlog.digest_errors(self.debug_mode)
            return {'CANCELLED'}
        
        warnings = []
        try:
            gfs = GFSInterface.from_file(filepath, warnings=warnings) 
        except UnsupportedVersionError as e:
            errorlog.log_error_message(f"The file you attempted to load is an unsupported version: {str(e)}.")
        except ParticlesError:
            errorlog.log_error_message("The file you attempted to load contains EPL data, which cannot currently be loaded.")
        except HasParticleDataError:
            errorlog.log_error_message("The file you attempted to load contains EPL data, which cannot currently be loaded.")

        # Add any file-loading warnings to the warnings list
        for warning_msg in warnings:
            errorlog.log_warning_message(warning_msg)

        # Report any file-loading errors
        if len(errorlog.errors):
            errorlog.digest_errors(self.debug_mode)
            return {'ERROR'}
        
        # Now import file data to Blender
        filename = os.path.splitext(os.path.split(filepath)[1])[0]
        import_animations(gfs, armature, filename)
        
        # Report any warnings that were logged
        errorlog.digest_warnings(self.debug_mode)
        
        set_fps(self, context)
        
        self.report({"INFO"}, "Import successful.")
        
        return {'FINISHED'}
    
    def execute(self, context):
        return self.import_file(context, bpy.data.objects[self.armature_name], self.filepath)
