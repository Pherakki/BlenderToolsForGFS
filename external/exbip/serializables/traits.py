def ReadableTrait(Reader):
    class ReadableTraitImpl:
        def read(self, filepath, *args, **kwargs):
            reader = Reader()
            with reader.FileIO(filepath) as rw:
                rw.rw_obj(self, *args, **kwargs)

        def frombytes(self, byte_data, *args, **kwargs):
            reader = Reader()
            with reader.BytestreamIO(byte_data):
                reader.rw_obj(self, *args, **kwargs)

    return ReadableTraitImpl


def WriteableTrait(Writer):
    class WriteableTraitImpl:
        def write(self, filepath, *args, **kwargs):
            writer = Writer()
            with writer.FileIO(filepath) as rw:
                rw.rw_obj(self, *args, **kwargs)

        def tobytes(self, *args, **kwargs):
            writer = Writer()
            with writer.BytestreamIO():
                writer.rw_obj(self, *args, **kwargs)
                writer.seek(0)
                return writer._bytestream.read()

    return WriteableTraitImpl

def ValidatableTrait(Validator):
    class ValidableTraitImpl:
        def validate_file_against_file(self, primary_filepath, reference_filepath, *args, **kwargs):
            validator = Validator()
            
            with validator.PrimaryFileIO(primary_filepath).ReferenceFileIO(reference_filepath) as rw:
                rw.rw_obj(self, *args, **kwargs)
        
        def validate_file_against_bytes(self, primary_filepath, reference_bytes, *args, **kwargs):
            validator = Validator()
            
            with validator.PrimaryFileIO(primary_filepath).ReferenceBytestreamIO(reference_bytes) as rw:
                rw.rw_obj(self, *args, **kwargs)
        
        def validate_bytes_against_file(self, primary_bytes, reference_filepath, *args, **kwargs):
            validator = Validator()
            
            with validator.PrimaryBytestreamIO(primary_bytes).ReferenceFileIO(reference_filepath) as rw:
                rw.rw_obj(self, *args, **kwargs)
        
        def validate_bytes_against_bytes(self, primary_bytes, reference_bytes, *args, **kwargs):
            validator = Validator()
            
            with validator.PrimaryBytestreamIO(primary_bytes).ReferenceBytestreamIO(reference_bytes):
                validator.rw_obj(self, *args, **kwargs)
        
    return ValidableTraitImpl


def OffsetsTrackableTrait(OffsetTracker):
    class OffsetsTrackableTraitImpl:
        def calculate_offsets(self, *args, **kwargs):
            offset_calculator = OffsetTracker()
            offset_calculator.rw_obj(self, *args, **kwargs)
    
    return OffsetsTrackableTraitImpl
