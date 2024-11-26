import io
from ...serialization.parsers import GFSReader
from ...serialization.parsers import GFSWriter


def pack_object(obj, version, rw=lambda wtr,obj,version: wtr.rw_obj(obj, version)):
    # Set up writer, stream, and object bytes
    wtr = GFSWriter()
    stream = io.BytesIO()
    wtr._bytestream = stream
    
    # Serialize
    wtr.rw_uint32(version)
    with wtr.new_origin():
        rw(wtr, obj, version)
    stream.seek(0)

    return ''.join(f"{elem:0>2X}" for elem in stream.read())


def unpack_object(data, ctor, rw=lambda rdr,obj,version: rdr.rw_obj(obj, version)):
    # Set up reader, stream, and object bytes
    rdr = GFSReader()
    stream = io.BytesIO()
    rdr._bytestream = stream
    objbytes = bytes.fromhex(data)
    
    # Extract version and write object data to stream
    obj = ctor()
    stream.write(objbytes)
    stream.seek(0)
    version = rdr.rw_uint32(None)
    with rdr.new_origin():
        # Read object
        rw(rdr, obj, version)
    return obj
