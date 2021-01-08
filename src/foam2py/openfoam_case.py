import os
import re

def rel_path(project_path, solver):
    """Get relative to post_process.py script case path
    """
    if solver == "multiCompressionFoam":
        return project_path + '/'
    else:
        return (project_path
                + f"/../../{solver}/{os.path.basename(project_path)}/")

def grep_value(key, log="log.checkMesh", pattern='(\d+.\d+)'):
    """Get value in line with key by pattern
    """
    for grep in open(log):
        if key in grep:
            value = re.findall(pattern, grep)

    if pattern == '(\d+)':
        return int(value[0])
    elif pattern == '(\d+.\d+)':
        return float(value[0])
    else:
        return value[0]