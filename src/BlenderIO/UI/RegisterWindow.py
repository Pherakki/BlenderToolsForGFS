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
    
    invoked_xy: bpy.props.IntVectorProperty(size=2, default=[0, 0])
    first_run:  bpy.props.BoolProperty(default=True)
    
    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        # This would be nice but blender seems to have have bug where
        # the mouse pos isn't updated in the preferences window
        #self.invoked_xy = (event.mouse_x, event.mouse_y)
        #self.first_run = True;
        #context.window.cursor_warp(context.window.width//2, context.window.height//2);

        return context.window_manager.invoke_props_dialog(self, width=512)

    def check(self, context):
        """Allows the dialog to redraw"""
        return True

    def draw(self, context):
        # if self.first_run:
        #     self.first_run = False
        #     context.window.cursor_warp(self.invoked_xy[0], self.invoked_xy[1]);

        layout = self.layout

        text_row = layout.row()
        col      = text_row.column()

        message = "Blender Tools for GFS has been successfully activated. Please note that:\n"\
            "1) You should read the documentation to learn how to get started and how to use the plugin. The button at the bottom of this window will open the documentation for you. You can also open the documentation at any time from the Addon Preferences (click the drop-down arrow next to the checkbox used to enable the plugin).\n"\
            "2) You can edit the default import and export settings of the plugin from the Addon Preferences (click the drop-down arrow next to the checkbox used to enable the plugin).\n"\
            "3) Non-renderable or strictly controlled GFS data is commonly made available to edit in additional UI panels throughout the Blender UI. Refer to the documentation to learn more.\n"\
            "4) This plugin is complementary to existing tools such as GFDStudio, and should be used alongside them rather than as a pure replacement."

        col.scale_y = 0.8
        for submsg in message.split('\n'):
            col.separator(factor=0.4)
            for line in wrapText(submsg, 96):
                col.label(text=line)
        
        op_row = layout.row()
        # Need to add horizontal spacing
        op_row.operator(OpenDocumentation.bl_idname)
