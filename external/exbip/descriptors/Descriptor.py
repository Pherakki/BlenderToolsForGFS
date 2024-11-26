class DescriptorDescriptor:
    FUNCTION_NAME = "rw_descriptor"

    def deserialize(binary_parser, descriptor, *args, **kwargs):
        return descriptor.deserialize(binary_parser, *args, **kwargs)

    def serialize(binary_parser, descriptor, *args, **kwargs):
        return descriptor.serialize(binary_parser, *args, **kwargs)
    
    def count(binary_parser, descriptor, *args, **kwargs):
        return descriptor.count(binary_parser, *args, **kwargs)
