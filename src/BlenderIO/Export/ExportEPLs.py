import io

import bpy

from ...FileFormats.GFS.Interface import EPLInterface
from ...FileFormats.GFS.SubComponents.CommonStructures.SceneNode.EPL.EPLBinary import EPLBinary
from ...serialization.BinaryTargets import Reader
from ..WarningSystem.Warning import ReportableError


def export_epls(gfs, armature, errorlog, export_policies):
    if export_policies.do_strip_epls:
        return
    
    # Export root node epls
    root_props = armature.data.GFSTOOLS_NodeProperties

    for epl_prop in root_props.epls:
        epl = EPLInterface()
        epl.node = 0
        epl.binary = unpack_epl_binary(epl_prop)
        gfs.epls.append(epl)
    
    # Export bone epls
    for bone in armature.data.bones:
        node_idx = [b.name for b in gfs.bones].index(bone.name)
        props = bone.GFSTOOLS_NodeProperties
        
        for epl_prop in props.epls:
            epl = EPLInterface()
            epl.node = node_idx
            epl.binary = unpack_epl_binary(epl_prop)
            gfs.epls.append(epl)
    

def unpack_epl_binary(epl_prop):
    stream = io.BytesIO()
    stream.write(bytes.fromhex(epl_prop.blob))
    stream.seek(0)
    rdr = Reader(None)
    rdr.bytestream = stream
    epl_binary = EPLBinary(endianness=">")
    rdr.rw_obj(epl_binary, 0x01105100)
    
    return epl_binary
