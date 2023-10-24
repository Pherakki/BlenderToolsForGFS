import os


def get_git_hash(package_root):
    git_path = os.path.join(package_root, ".git")
    if not os.path.isdir(git_path):
        return
    
    head_file = os.path.join(git_path, "HEAD")
    if not os.path.isfile(head_file):
        return
    
    with open(head_file, 'r') as F:
        head_path = F.read()
    head_path = head_path.rstrip('\n').split("ref: ")[1]
    
    hash_path = os.path.join(git_path, *head_path.rstrip('\n').split('/'))
    
    if not os.path.isfile(hash_path):
        return
    
    with open(hash_path, 'r') as F:
        hash_value = F.read()
    
    return hash_value


def get_git_short_hash(package_root):
    full_hash = get_git_hash(package_root)
    if full_hash is None:
        return
    
    return full_hash[:7]
