import os
from ..Utils.String import get_name_string


import bpy


def import_textures(gfs, external_textures, shares_textures, errorlog):
    textures = {}
    for tex in gfs.textures:
        # safety check... split off any paths from name
        name = get_name_string("Texture", tex.name_bytes, "shift-jis", errorlog).split("/")[-1].split("\\")[-1]
        if shares_textures and name in bpy.data.images:
            textures[name] = bpy.data.images[name]
            continue
        # Assume for now that duplicate images use the first image
        # Should test this in-game
        if name in textures:
            continue
        
        # Path for temporary file
        filepath = os.path.join(bpy.app.tempdir, name)
        # Try/finally seems to prevent a race condition between Blender and 
        # Python forming
        try:
            payload = external_textures.get(tex.name_bytes, tex.image_data)
            with open(filepath, 'wb') as F:
                F.write(payload)
            img = bpy.data.images.load(filepath)
            img.pack()
            img.filepath_raw = name
            textures[name] = img
                
            img.GFSTOOLS_ImageProperties.unknown_1 = tex.unknown_1
            img.GFSTOOLS_ImageProperties.unknown_2 = tex.unknown_2
            img.GFSTOOLS_ImageProperties.unknown_3 = tex.unknown_3
            img.GFSTOOLS_ImageProperties.unknown_4 = tex.unknown_4
        finally:
            os.remove(filepath)
    return textures
