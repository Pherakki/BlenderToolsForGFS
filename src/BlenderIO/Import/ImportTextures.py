import os
from ..Utils.String import get_name_string


import bpy

def get_texname(name_bytes, errorlog):
    return get_name_string("Texture", name_bytes, "shift-jis", errorlog).split("/")[-1].split("\\")[-1]

def create_bpy_img(filepath, name, payload):
    with open(filepath, 'wb') as F:
        F.write(payload)
    img = bpy.data.images.load(filepath)
    img.pack()
    img.filepath_raw = name
    return img

def import_textures(gfs, external_textures, shares_textures, errorlog):
    textures = {}
    unused_textures = {nm: idx for idx, nm in enumerate(external_textures)}
    for tex in gfs.textures:
        # safety check... split off any paths from name
        name = get_texname(tex.name_bytes, errorlog)
        if tex.name_bytes in unused_textures:
            del unused_textures[tex.name_bytes]
        
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
            img = create_bpy_img(filepath, name, payload)
            textures[name] = img
                
            img.GFSTOOLS_ImageProperties.unknown_1 = tex.unknown_1
            img.GFSTOOLS_ImageProperties.unknown_2 = tex.unknown_2
            img.GFSTOOLS_ImageProperties.unknown_3 = tex.unknown_3
            img.GFSTOOLS_ImageProperties.unknown_4 = tex.unknown_4
        finally:
            os.remove(filepath)
            
    # Deal with unused textures
    out_unused_textures = {}
    for texname in unused_textures:
        name = get_texname(texname, errorlog)
        filepath = os.path.join(bpy.app.tempdir, name)
        try:
            payload = external_textures[texname]
            img = create_bpy_img(filepath, name, payload)
            out_unused_textures[name] = img
        finally:
            os.remove(filepath)
    
    return textures, out_unused_textures
