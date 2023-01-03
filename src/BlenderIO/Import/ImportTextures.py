import os

import bpy


def import_textures(gfs):
    textures = {}
    for tex in gfs.textures:
        filepath = os.path.join(bpy.app.tempdir, tex.name)
        # Try/finally seems to prevent a race condition between Blender and 
        # Python forming
        try:
            with open(filepath, 'wb') as F:
                F.write(tex.image_data)
            img = bpy.data.images.load(filepath)
            img.pack()
            img.filepath_raw = img.name
            
            # Assume for now that duplicate images use the first image
            # Should test this in-game
            if tex.name not in textures:
                textures[tex.name] = img
        finally:
            os.remove(filepath)
    return textures
