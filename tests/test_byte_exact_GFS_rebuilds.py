import os

from ..src.FileFormats.GFS.GFSBinary.GFS0ContainerBinary import HasAnimationsError, UnsupportedVersionError
from ..src.FileFormats.GFS.GFSBinary import GFS0Binary
from ..src.FileFormats.GFS.GFSInterface import GFSInterface
from ..src.FileFormats.GFS.GFSBinary.AnimationBinary import ParticlesError
from ..src.FileFormats.GFS.GFSBinary.ModelBinary.SceneNodeBinary.NodeAttachmentBinary import HasParticleDataError, HasType9Error


def execute(data_root, error_out):
    #######################
    # VALIDATE ALL MODELS #
    #######################
    model_files = []
    model_root = data_root
    ignore = []
    ignore.append("C5931_000_00.GMD") # Contains non-UTF8 strings
    ignore.append("PS0003.GMD")       # Contains non-UTF8 strings
    ignore.append("PS0142.GMD")       # Contains non-UTF8 strings
    ignore.append("PS0298.GMD")       # Contains non-UTF8 strings
    ignore.append("PSZ0298.GMD")      # Contains non-UTF8 strings
    ignore.append("C9525_000_00.GMD") # Contains strings that do not hash correctly - hasher bug?
    ignore.append("M057_094.GMD")     # Contains non-UTF8 strings
    ignore.append("IT0726_001.GMD")     # Contains non-UTF8 strings
    ignore.append("IT0726_002.GMD")     # Contains non-UTF8 strings
    ignore.append("IT0749_000.GMD")     # Contains non-UTF8 strings
    ignore.append("IT0749_001.GMD")     # Contains non-UTF8 strings
    
    for root, _, files in os.walk(model_root):
        for file in files:
            if file.endswith(".GMD") and file not in ignore:
                model_files.append(os.path.join(root, file))
    
    model_files = sorted(model_files)
    
    anim_errors          = []
    particle_errors      = []
    anim_particles_error = []
    version_errors       = []
    type_9_errors        = []
    unspecified_errors   = []

    n_files = len(model_files)
    largest = max(len(os.path.split(f)[1]) for f in model_files)
    
    for i, file in enumerate(model_files):
        path, filename = os.path.split(file)
        print(f"\rValidating model {i+1}/{n_files}... [{filename.ljust(largest)}]", end="")

        gb = GFS0Binary()
        try:
            gb.read(file)
            gi = GFSInterface.from_binary(gb)
            gb2 = gi.to_binary()
            gb2.write("tmp.GMD")
            
            with open(file, 'rb') as F, open("tmp.GMD", 'rb') as G:
                fdata = F.read()
                gdata = G.read()
                
                for i, (b1, b2) in enumerate(zip(fdata, gdata)):
                    assert b1 == b2, f"{i}: {b1} {b2}"
                    
                assert len(fdata) == len(gdata)
                    
        except ParticlesError:
            anim_particles_error.append(file)
        except HasAnimationsError:
            anim_errors.append(file)
        except HasParticleDataError:
            particle_errors.append(file)
        except UnsupportedVersionError as e:
            version_errors.append((file + " " + str(e)))
        except HasType9Error:
            type_9_errors.append(file)
        except Exception as e:
            unspecified_errors.append(str(e))
            
    anim_error_count           = len(anim_errors)
    particle_error_count       = len(particle_errors)
    anim_particles_error_count = len(anim_particles_error)
    version_error_count        = len(version_errors)
    type_9_error_count         = len(type_9_errors)
    unspecified_error_count    = len(unspecified_errors)
    ignored_files_count        = len(ignore)
    
    error_out.extend((anim_errors, particle_errors, anim_particles_error, version_errors, type_9_errors, unspecified_errors))

    print()
    print("###############")
    if unspecified_error_count > 0:
        print("# TEST FAILED #")
    else:
        print("# TEST PASSED #")
    print("###############")
    print("Acceptable failures:")
    print("-", particle_error_count, "files failed due to containing EPL data")
    print("-", anim_error_count, "files failed due to containing animation data")
    print("-", anim_particles_error_count, "files failed due to containing animations with EPL data")
    print("-", version_error_count, "files failed due to containing unsupported versions")
    print("-", type_9_error_count, "files failed due to containing type 9 node attributes")
    print("-", ignored_files_count, "files failed due to being on the hardcoded 'ignore' list")
    
    if unspecified_error_count > 0:
        print("UNACCEPTABLE FAILURES:")
        print("-", unspecified_errors, "files failed due to unspecified errors")
        
    return unspecified_error_count > 0
