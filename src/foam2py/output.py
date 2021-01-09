import os
from tabulate import tabulate

def info(project_path, project, checks):

    header = ['case          ', 'nCells']
    body = [os.path.basename(project_path), (project['cells'])]
    for key in list(checks.keys()):
        header.append(key)
        body.append(all(checks[key]['passed']))

    print(tabulate([body], headers=header))