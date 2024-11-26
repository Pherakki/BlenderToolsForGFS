class EndianPairDescriptor:
    __slots__ = ("FUNCTION_NAME", "little_endian", "big_endian")
    
    def __init__(self, name, little_endian, big_endian):
        self.FUNCTION_NAME = name
        self.little_endian = little_endian
        self.big_endian    = big_endian
