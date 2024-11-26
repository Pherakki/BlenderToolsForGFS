import io

import bpy

from ...FileFormats.GFS.Interface import EPLInterface
from ...FileFormats.GFS.SubComponents.CommonStructures.SceneNode.EPL.EPLBinary import EPLBinary
from ..Utils.Serialization import unpack_object


def export_epls(gfs, armature, errorlog, export_policies):
    if export_policies.do_strip_epls:
        return
    
    # Export root node epls
    root_props = armature.data.GFSTOOLS_NodeProperties

    for epl_prop in root_props.epls:
        epl = EPLInterface.from_binary(0, unpack_epl_binary(epl_prop))
        gfs.epls.append(epl)
    
    # Export bone epls
    for bone in armature.data.bones:
        node_idx = [b.name for b in gfs.bones].index(bone.name)
        props = bone.GFSTOOLS_NodeProperties
        
        for epl_prop in props.epls:
            epl = EPLInterface.from_binary(node_idx, unpack_epl_binary(epl_prop))
            gfs.epls.append(epl)
    

def unpack_epl_binary(epl_prop):
    epl_binary = unpack_object(epl_prop.blob, EPLBinary)
    return epl_binary
