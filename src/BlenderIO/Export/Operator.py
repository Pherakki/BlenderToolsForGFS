import array

import bpy
from bpy_extras.io_utils import ExportHelper
import numpy as np

from ...FileFormats.GFS import GFSInterface
from ..Utils.ErrorPopup import handle_errors, ReportableException
from .ExportNodes import export_node_tree
from .ExportMeshData import export_mesh_data
from .ExportMaterials import export_materials_and_textures
from .ExportLights import export_lights
from .ExportCameras import export_cameras
from .ExportPhysics import export_physics
from .Export0x000100F8 import export_0x000100F8
#from ..WarningSystem import WarningSystem, handle_warning_system


class ExportGFS(bpy.types.Operator, ExportHelper):
    bl_idname = 'export_file.export_gfs'
    bl_label = 'Persona 5 Royal - PC (.GMD, .GFS)'
    bl_options = {'REGISTER', 'UNDO'}
    filename_ext: bpy.props.EnumProperty(
        items=[
            ('.GMD', '.GMD', ''),
            ('.GFS', '.GFS', '')
        ],
        options={'HIDDEN'}
    )


    filter_glob: bpy.props.StringProperty(
                                              default="*.GMD;*.GFS",
                                              options={'HIDDEN'},
                                          )
    
    version: bpy.props.EnumProperty(items=(
            ("0x01104920", "0x01104920", ""),
            ("0x01104950", "0x01104950", ""),
            ("0x01105000", "0x01105000", ""),
            ("0x01105010", "0x01105010", ""),
            ("0x01105020", "0x01105020", ""),
            ("0x01105030", "0x01105030", ""),
            ("0x01105040", "0x01105040", ""),
            ("0x01105050", "0x01105050", ""),
            ("0x01105060", "0x01105060", ""),
            ("0x01105070", "0x01105070", ""),
            ("0x01105080", "0x01105080", ""),
            ("0x01105090", "0x01105090", ""),
            ("0x01105100", "0x01105100", "")
        ),
        name="Version",
        default="0x01105100"
    )
    
    def export_file(self, context, filepath):
        # Figure out the mode sanitising later
        # current_mode = bpy.context.active_object.mode
        # bpy.ops.object.mode_set("OBJECT")
        
        # Locate which model to expose based on what object the user has
        # selected.
        selected_model = find_selected_model()
        
        # Pre-process the model and check if there is any unexportable data
        # Throw any errors here if they exist, and take note of any warnings
        # if they shouldn't interrupt export.
        self.validate_model(selected_model)
        
        # Now export the model data since we've passed validation
        # If there are any exceptions that get thrown in here, this is
        # probably not good and should get thrown from the validation instead.
        # Therefore any exceptions that interrupt model export in this block
        # should be reported as bugs, and this should be communicated to the
        # user.
        gfs = GFSInterface()
        export_node_tree(gfs, selected_model)
        bpy_material_names = export_mesh_data(gfs, selected_model)
        export_materials_and_textures(gfs, bpy_material_names)
        export_lights(gfs, selected_model)
        export_cameras(gfs, selected_model)
        export_physics(gfs, selected_model)
        export_0x000100F8(gfs, selected_model)
        #bpy.ops.object.mode_set(current_mode)
        
        gfs.has_end_container = True # Put this somewhere else
        gb = gfs.to_binary(int(self.version, 0x10))
        gb.write(filepath)
        
        # Tell the user if there are any warnings they should be aware of.
        #WarningSystem.digest_warnings()
        
        return {'FINISHED'}
    
    #@handle_warning_system
    def execute(self, context):
        return self.export_file(context, self.filepath)
    
    
    def validate_model(self, selected_model):
        # Do model validation in here.
        # Validation may depend on exporter settings, so make it a method
        # of the operator.
        
        # Throw any errors that are found
        #WarningSystem.digest_errors()
        pass

def find_selected_model():
    try:
        parent_obj = bpy.context.selected_objects[0]
    except IndexError as e:
        raise ReportableException("You must select some part of the model you wish to export in Object Mode before attempting to export it. No model is currently selected.") from e
    except Exception as e:
        raise e

    sel_obj = None
    while parent_obj is not None:
        sel_obj = parent_obj
        parent_obj = sel_obj.parent
    parent_obj = sel_obj
    if parent_obj.type != "ARMATURE":
        raise ReportableException(f"An object is selected, but the top-level object \'{parent_obj.name}\' is not an Armature object - has type {parent_obj.type}.")
    return parent_obj

# def find_pinned_armatures(parent_obj):
#     out = []
#     for obj in bpy.data.objects:
#         if not obj.type == "ARMATURE":
#             continue
#         for constr in obj.constraints:
#             if constr.type != "CHILD_OF":
#                 continue
#             if constr.target == obj:
#                 continue
#             out.append(obj)
#     return out
                    