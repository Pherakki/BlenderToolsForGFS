import os
from ..Utils.String import get_name_string


import bpy


def import_textures(gfs, errorlog):
    textures = {}
    for tex in gfs.textures:
        # safety check... split off any paths from name
        name = get_name_string("Texture", tex.name_bytes, "shift-jis", errorlog).split("/")[-1].split("\\")[-1]
        filepath = os.path.join(bpy.app.tempdir, name)
        # Try/finally seems to prevent a race condition between Blender and 
        # Python forming
        try:
            with open(filepath, 'wb') as F:
                F.write(tex.image_data)
            img = bpy.data.images.load(filepath)
            img.pack()
            img.filepath_raw = name
            
            # Assume for now that duplicate images use the first image
            # Should test this in-game
            if tex.name not in textures:
                textures[tex.name] = img
                
            img.GFSTOOLS_ImageProperties.unknown_1 = tex.unknown_1
            img.GFSTOOLS_ImageProperties.unknown_2 = tex.unknown_2
            img.GFSTOOLS_ImageProperties.unknown_3 = tex.unknown_3
            img.GFSTOOLS_ImageProperties.unknown_4 = tex.unknown_4
        finally:
            os.remove(filepath)
    return textures
