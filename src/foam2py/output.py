import os
from tabulate import tabulate

try:
    get_ipython
    full_output = True
except:
    full_output = False

def info(project_path, project, checks):
    header = ['case          ', 'nCells']
    body = [os.path.basename(project_path), (project['cells'])]
    details = ''
    for key in list(checks.keys()):
        header.append(key)
        body.append(all(checks[key]['passed']))
        if not all(checks[key]['passed']):
            details += f"\nWARNING! '{key}' test is not passed:"
        else:
            details += f"\n'{key}' test is passed:"
        details += '\n' + str(checks[key]) + '\n'

    basics = tabulate([body], headers=header)

    # Write complete output to log.tests
    log = open(project_path + "/log.post_process", 'w+')
    log.write(basics + '\n' + details + '\nend\n')
    log.close()

    # Print output
    print(basics)
    if full_output:
        print(details)