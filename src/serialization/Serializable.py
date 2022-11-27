import copy

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

    def read(self, filepath):
        with Reader(filepath) as rw:
            rw.rw_obj(self)

    def write(self, filepath):
        with Writer(filepath) as rw:
            rw.rw_obj(self)

    def calc_pointers(self):
        with PointerCalculator() as rw:
            rw.rw_obj(self)

    def read_write(self, rw):
        raise NotImplementedError

