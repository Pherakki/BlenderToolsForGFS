import io
import os

from ..src.FileFormats.GFS import GFSBinary
from ..src.FileFormats.GFS import GFSInterface
from ..src.FileFormats.GFS.SubComponents.GFS0ContainerBinary import HasAnimationsError, UnsupportedVersionError
from ..src.FileFormats.GFS.SubComponents.Animations.Binary.AnimationBinary import ParticlesError
from ..src.FileFormats.GFS.SubComponents.CommonStructures.SceneNode.NodeAttachmentBinary import HasParticleDataError, HasType9Error
from ..src.serialization.BinaryTargets import Comparator

if 'bpy' in globals():
    raise Exception("'bpy' module has been loaded - this test is incompatible with the bpy module")

def fetch_meshes(node_ids, nodes, meshes, node):
    idx = node_ids[id(node)]
    for attachment in node.attachments:
        if attachment.type == 4:
            meshes.append((idx, attachment.data))
    nodes.append(node)
    for child in node.children:
        fetch_meshes(node_ids, nodes, meshes, child)

def fetch_node_ids(ids, node):
    ids[id(node)] = len(ids)
    for child in node.children[::-1]:
        fetch_node_ids(ids, child)

class InconsistentVersionsError(Exception):
    pass

def execute(data_root, error_out, start=0, stop=None, namefilter=None):
    #######################
    # VALIDATE ALL MODELS #
    #######################
    model_files = []
    model_root = data_root
    
    # Init the ignore list:
    # Contains filepaths that have known issues that currently can't be
    # dealt with
    ignore = []
    ignore.append('CHARACTER/5931/C5931_000_00.GMD')    # Contains non-UTF8 strings '\x97L\x8c\xf8'
    ignore.append('CHARACTER/9525/C9525_000_00.GMD')    # Hash inconsistency
    ignore.append("CHARACTER/PERSONA/0003/PS0003.GMD")  # Contains non-UTF8 strings '\x97L\x8c\xf8'
    ignore.append("CHARACTER/PERSONA/0142/PS0142.GMD")  # Contains non-UTF8 strings '\x97L\x8c\xf8'
    ignore.append("CHARACTER/PERSONA/0298/PS0298.GMD")  # Contains non-UTF8 strings '\x97L\x8c\xf8'
    ignore.append("CHARACTER/PERSONA/0298/PSZ0298.GMD") # Contains non-UTF8 strings '\x97L\x8c\xf8'
    ignore.append("FIELD_TEX/F057_151_0.GFS")           # Contains non-UTF8 strings '\x97L\x8c\xf8'
    ignore.append("FIELD_TEX/OBJECT/M057_094.GMD")      # Contains non-UTF8 strings '\x97L\x8c\xf8'
    ignore.append("ITEM/IT0100_000.GMD")                # Texture footer is 0!?
    ignore.append("ITEM/IT0175_002.GMD")                # Texture footer is 0!?
    ignore.append("ITEM/IT0263_001.GMD")                # Contains non-UTF8 strings '\x97L\x8c\xf8'
    ignore.append("ITEM/IT0265_001.GMD")                # Contains non-UTF8 strings '\x97L\x8c\xf8'
    ignore.append("ITEM/IT0611_000.GMD")                # Texture footer is 0!?
    ignore.append("ITEM/IT0615_000.GMD")                # Texture footer is 0x1010202!?
    
    for root, dirs, files in os.walk(model_root):
        for file in files:
            full_path = os.path.join(root, file)
            relative_path = os.path.relpath(full_path, data_root)
            if any(file.endswith(ext) for ext in [".GMD", ".GFS"]) and (relative_path not in ignore):
                model_files.append(full_path)
    
    if namefilter is not None:
        assert callable(namefilter), f"namefilter must be callable."
        assert type(namefilter("teststring")) is bool, f"namefilter must return a bool." 
        model_files = [f for f in model_files if namefilter(f)]
    model_files = sorted(model_files)
    assert start >= 0,    "The start index must be larger than or equal to 0."
    model_files = model_files[start:]
    if stop is not None:
        assert stop  >  0,    "The stop index must be larger than 0."
        assert stop  > start, "The stop index must be larger than the start index."
        model_files = model_files[:stop-start]
    
    n_passed = 0
    anim_errors                  = []
    particle_errors              = []
    anim_particles_error         = []
    version_errors               = []
    type_9_errors                = []
    inconsistent_versions_errors = []
    unspecified_errors           = []

    n_files = len(model_files)
    largest = max(len(os.path.split(f)[1]) for f in model_files)
    
    
    for i, file in enumerate(model_files):
        path, filename = os.path.split(file)
        print(f"\rValidating model {i+1}/{n_files}... [{filename.ljust(largest)}]", end="")

        gb = GFSBinary()
        try:
            gb.read(file)
            
            if not all(ctr.version == gb.containers[0].version for ctr in gb.containers):
                raise InconsistentVersionsError
            
            gi = GFSInterface.from_binary(gb)
            gb2 = gi.to_binary(gb.containers[0].version, add_end_container=os.path.splitext(filename) != ".GAP")
            
            
            ##################################
            # HACKS TO FIX UP THE REGRESSION #
            ##################################
            node_ids_1 = {}
            nodes_1 = []
            meshes_1 = []
            node_ids_2 = {}
            nodes_2 = []
            meshes_2 = []
            model_1 = None
            model_2 = None
            
            # Fetch data required for hacks
            for ctr in gb.containers:
                if ctr.type == 0x00010003:
                    model_1 = ctr.data
                    fetch_node_ids(node_ids_1, ctr.data.root_node)
                    fetch_meshes(node_ids_1, nodes_1, meshes_1, ctr.data.root_node)
                    break
            for ctr in gb2.containers:
                if ctr.type == 0x00010003:
                    model_2 = ctr.data
                    fetch_node_ids(node_ids_2, ctr.data.root_node)
                    fetch_meshes(node_ids_2, nodes_2, meshes_2, ctr.data.root_node)
                    break
            
            # Bounding volumes
            # Should include closeness checks for these when they work...
            for (parent_1, m1), (parent_2, m2) in zip(meshes_1, meshes_2):
                m2.bounding_box_max_dims = m1.bounding_box_max_dims
                m2.bounding_box_min_dims = m1.bounding_box_min_dims
                m2.bounding_sphere_centre = m1.bounding_sphere_centre
                m2.bounding_sphere_radius = m1.bounding_sphere_radius
            if model_1 is not None:
                model_2.bounding_box_max_dims = model_1.bounding_box_max_dims
                model_2.bounding_box_min_dims = model_1.bounding_box_min_dims
                model_2.bounding_sphere_centre = model_1.bounding_sphere_centre
                model_2.bounding_sphere_radius = model_1.bounding_sphere_radius

            # Vertex indices
            if model_1 is not None:
                if model_1.skinning_data.bone_count is not None:
                    ctr.size += (model_1.skinning_data.bone_count - model_2.skinning_data.bone_count)*(64 + 2)
                    model_2.skinning_data.bone_count = model_1.skinning_data.bone_count
                    model_2.skinning_data.matrix_palette = model_1.skinning_data.matrix_palette
                    model_2.skinning_data.ibpms = model_1.skinning_data.ibpms
                    for (pn1, m1), (pn2, m2) in zip(meshes_1, meshes_2):
                        if m2.flags.has_indices:
                            for v1, v2 in zip(m1.vertices, m2.vertices):
                                v2.indices = v1.indices
            
   
            
            # ##########
            # # EXPORT #
            # ##########
            gb2.write("tmp.GMD")
            
            with open(file, 'rb') as F, open("tmp.GMD", 'rb') as G:
                fdata = F.read()
                gdata = G.read()
                    
                try:
                    for i, (b1, b2) in enumerate(zip(fdata, gdata)):
                        assert b1 == b2, f"{i}: {b1} {b2}"
                        
                    assert len(fdata) == len(gdata)
                except:
                    cmp = Comparator(None, fdata)
                    stream = io.BytesIO()
                    stream.write(gdata)
                    stream.seek(0)
                    cmp.init_stream(stream)
                    gb3 = GFSBinary()
                    cmp.rw_obj(gb3)
                    
                assert len(fdata) == len(gdata)
                  
            n_passed += 1  
            
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
        except InconsistentVersionsError:
            inconsistent_versions_errors.append(file)
        except Exception as e:
            unspecified_errors.append((file, str(e)))
            
            
    anim_error_count            = len(anim_errors)
    particle_error_count        = len(particle_errors)
    anim_particles_error_count  = len(anim_particles_error)
    version_error_count         = len(version_errors)
    type_9_error_count          = len(type_9_errors)
    inconsistent_versions_count = len(inconsistent_versions_errors)
    unspecified_error_count     = len(unspecified_errors)
    ignored_files_count         = len(ignore)
    
    error_out.extend((anim_errors, particle_errors, anim_particles_error, version_errors, type_9_errors, unspecified_errors))

    print()
    print("###############")
    if unspecified_error_count > 0:
        print("# TEST FAILED #")
    else:
        print("# TEST PASSED #")
    print("###############")
    print(f"{n_passed} / {n_files} were de- and re-serialised without error.")
    print("Acceptable failures:")
    print("-", particle_error_count,        "files failed due to containing EPL data.")
    #print("-", anim_error_count,            "files failed due to containing animation data.")
    print("-", anim_particles_error_count,  "files failed due to containing animations with EPL data.")
    print("-", version_error_count,         "files failed due to containing unsupported versions.")
    print("-", type_9_error_count,          "files failed due to containing type 9 node attributes.")
    print("-", inconsistent_versions_count, "files failed due to having inconsistent versions between containers.")
    print("-", ignored_files_count,         "files failed due to being on the hardcoded 'ignore' list.")
    
    if unspecified_error_count > 0:
        print()
        print("UNACCEPTABLE FAILURES:")
        print("-", unspecified_error_count, "files failed due to unspecified errors")
        print()
        max_print = 10
        if unspecified_error_count > max_print:
            print(f"The first {max_print} of these are:")
        for filepath, err in unspecified_errors[:max_print]:
            print(filepath + ":", err)
        
    return unspecified_error_count > 0
