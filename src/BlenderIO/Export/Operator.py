import array

import bpy
from bpy_extras.io_utils import ExportHelper
import numpy as np

from ...FileFormats.GFS import GFSInterface
from ..Utils.ErrorPopup import handle_errors, ReportableException
from .ExportNodes import export_node_tree
from .ExportMeshData import export_mesh_data

class ExportGFS(bpy.types.Operator, ExportHelper):
    bl_idname = 'export_file.export_gfs'
    bl_label = 'Persona 5 Royal - PC (.GMD, .GFS)'
    bl_options = {'REGISTER', 'UNDO'}
    filename_ext = "*.GMD, *.GFS"


    filter_glob: bpy.props.StringProperty(
                                              default="*.GMD;*.GFS",
                                              options={'HIDDEN'},
                                          )
    
    def export_file(self, context, filepath):
        # Figure out the mode sanitising later
        # current_mode = bpy.context.active_object.mode
        # bpy.ops.object.mode_set("OBJECT")
        
        gfs = GFSInterface()
        selected_model = find_selected_model()
        export_node_tree(gfs, selected_model)
        export_mesh_data(gfs, selected_model)
        
        #bpy.ops.object.mode_set(current_mode)
        
        gb = gfs.to_binary(0x01105100)
        gb.write(filepath)
        
        return {'FINISHED'}
    
    @handle_errors
    def execute(self, context):
        return self.export_file(context, self.filepath)


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
                    