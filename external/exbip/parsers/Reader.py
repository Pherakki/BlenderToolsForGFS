from ..framework.parsers.ReaderBase import ReaderBase
from ..descriptors import STANDARD_DESCRIPTORS
from ..descriptors import STANDARD_ENDIAN_DESCRIPTORS


class Reader(ReaderBase.extended_with(STANDARD_DESCRIPTORS, STANDARD_ENDIAN_DESCRIPTORS)):
    pass
