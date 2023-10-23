import os
import platform
import subprocess

import bpy

from ..modelUtilsTest.Utils.TextWrapping import wrapText
from .HelpWindows import OpenDocumentation


class RegisterWindow(bpy.types.Operator):
    bl_idname = "gfstools.registerwindow"
    bl_label = "Registration Successful"
    bl_options = {'REGISTER'}
    
    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=512)

    def check(self, context):
        """Allows the dialog to redraw"""
        return True

    def draw(self, context):
        layout = self.layout

        col = layout.column()

        message = "Blender Tools for GFS has been successfully added to your Blender installation. Please note that:\n"\
            "1) There are some aspects of using the export functions that are idiomatic, such as UV map names. You should read the relevant sections of the documentation, accessible via the button at the bottom of this window, if you run into errors or need information on how to successfully export.\n"\
            "2) You can add GFS data to Blender structures via new panels in the Blender UI, such as on the Mesh Data Properties panel. You can also find links to the documentation on these panels via the 'How to Use' buttons."\
            "3) You should view the plugin as COMPLEMENTARY to existing tools, NOT as a REPLACEMENT. This means that you should still post-process any output from the tools in e.g. GFD Studio, particularly if you need to create custom materials."

        for line in wrapText(message, 80):
            col.label(text=line)
            
        col.operator(OpenDocumentation.bl_idname)
