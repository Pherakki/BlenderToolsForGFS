import os
import platform
import subprocess

import bpy

from ..Utils.TextWrapping import wrapText


class HelpWindow(bpy.types.Operator):
    bl_idname = "gfsblendertools.helpwindow"
    bl_label = "How To Use"
    bl_options = {'REGISTER'}
    
    message = None

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

        for line in wrapText(self.message, 80):
            col.label(text=line)
            
        col.operator(OpenDocumentation.bl_idname)
     
def defineHelpWindow(subid, msg):
    class SubHelpWindow(HelpWindow):
        bl_idname = f"gfsblendertools.{subid}helpwindow".lower()
        message = msg + "\n\nFurther information can be found in the documentation, which can be accessed by clicking the button below."
    
    return SubHelpWindow

class OpenDocumentation(bpy.types.Operator):
    bl_idname = "gfsblendertools.opendocs"
    bl_label = "Open Docs"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        self.open_documentation()
        return {'FINISHED'}
    
    @staticmethod
    def open_documentation():
        current_path = os.path.realpath(__file__)
        docs_path = os.path.join(current_path, 
                                 os.path.pardir,
                                 os.path.pardir,
                                 os.path.pardir,
                                 os.path.pardir,
                                 "docs",
                                 "documentation.pdf")
        
        if platform.system() == 'Windows':
            os.startfile(docs_path) # Windows
        elif platform.system() == 'Darwin':
            subprocess.call(('open', docs_path)) # Mac
        else:
            subprocess.call(('xdg-open', docs_path)) # Linux
