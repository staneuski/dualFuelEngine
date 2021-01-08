def rel_path(post_process_path, solver):
    """Get relative to post_process.py script case path
    """
    import os
    if solver == "multiCompressionFoam":
        return post_process_path + '/'
    else:
        return (post_process_path
                + f"/../../{solver}/{os.path.basename(post_process_path)}/")

def grep_value(key, log="log.checkMesh", pattern='(\d+.\d+)'):
    """Get value in line with key by pattern
    """
    import re
    for grep in open(log):
        if key in grep:
            value = re.findall(pattern, grep)

    if pattern == '(\d+)':
        return int(value[0])
    elif pattern == '(\d+.\d+)':
        return float(value[0])
    else:
        return value[0]