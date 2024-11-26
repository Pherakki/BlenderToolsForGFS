class SectionExistsDescriptor:
    FUNCTION_NAME = "section_exists"
    
    def deserialize(binary_parser, offset, count):
        return offset >= 0
    
    def serialize(binary_parser, offset, count):
        return count >= 0
    
    def count(binary_parser, offset, count):
        return count >= 0
