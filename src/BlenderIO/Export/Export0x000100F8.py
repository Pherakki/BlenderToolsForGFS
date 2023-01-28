import io

from ...serialization.BinaryTargets import Reader
from ...FileFormats.GFS.SubComponents.CommonStructures.Blob import Blob


def export_0x000100F8(gfs, bpy_obj):
    data = Blob()
    if bpy_obj.data.GFSTOOLS_ModelProperties.has_external_emt:
        data.data = b'\x00\x00\x00\x01\x00\x00\x00\t\x00\x0eapp_uniq_emote\xfe\x8dSQ\x00\x00\x00\x03 \n\n'
        gfs.data_0x000100F8 = data
