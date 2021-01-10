import os
import re

def rel_path(project_path, solver):
    """Get relative to post_process.py script case path
    """
    if solver == "multiCompressionFoam":
        return project_path
    else:
        return os.path.realpath(project_path + f"/../../{solver}"
                                f"/{os.path.basename(project_path)}")

def grep_value(key, log="/log.checkMesh", pattern='(\d+.\d+)'):
    """Get value in line with key by pattern
    """
    found = []
    for line in open(log):
        if key in line:
            value = re.findall(pattern, line)
            found.append((key in line))
    found = any(found)

    if found and (pattern == '(\d+)'):
        return int(value[0])
    elif found and (pattern == '(\d+.\d+)'):
        return float(value[0])
    else:
        return found