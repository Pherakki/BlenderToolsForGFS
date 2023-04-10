import copy
import io

from .BinaryTargets import Reader, Writer, PointerCalculator, Context


class Serializable:
    """
    Provides an interface for symmetrically reading, writing, or otherwise
    operating on binary data.
    To use, inherit from Serializable, and define a "read_write" method.
    Calling "read" or "write" on the object will then excute this method,
    with a BinaryTarget as the operating object.
    """
    __slots__ = ("context",)

    def __init__(self, context=None):
        if context is None:
            self.context = Context()
        else:
            self.context = copy.deepcopy(context)

    def read(self, filepath, *args, **kwargs):
        with Reader(filepath) as rw:
            rw.rw_obj(self, *args, **kwargs)


    def unpack(self, bytestring, *args, **kwargs):
        rw = Reader(None)
        rw.bytestream = io.BytesIO()
        rw.bytestream.write(bytestring)
        rw.seek(0)
        rw.rw_obj(self, *args, **kwargs)

    def write(self, filepath, *args, **kwargs):
        with Writer(filepath) as rw:
            rw.rw_obj(self, *args, **kwargs)

    def pack(self, *args, **kwargs):
        rw = Writer(None)
        rw.bytestream = io.BytesIO()
        rw.rw_obj(self, *args, **kwargs)
        rw.bytestream.seek(0)
        return rw.bytestream.read()

    def calc_pointers(self):
        with PointerCalculator() as rw:
            rw.rw_obj(self)

    def read_write(self, rw):
        raise NotImplementedError

