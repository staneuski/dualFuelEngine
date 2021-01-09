#!/usr/bin/env python3
# %%
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from tabulate import tabulate

project_path = os.path.split(os.path.realpath(__file__))[0]
sys.path.insert(0, project_path + '/../../../src')

import foam2py.openfoam_case as openfoam_case
import foam2py.tests as tests
import foam2py.tabulated as tabulated

solvers = ["multiCompressionFoam", "rhoPimpleFoam", "rhoCentralFoam"]

# %% Create case set w/ dataframes
project = project = dict(
    cells = openfoam_case.grep_value("nCells:",
                                     log=project_path + "/log.blockMesh",
                                     pattern='(\d+)')
)
for solver in solvers:
    case_path = openfoam_case.rel_path(project_path, solver)
    project[solver] = dict(
        execution_time = openfoam_case.grep_value("ExecutionTime",
                                                  log=case_path
                                                      + f"/log.{solver}"),
    )
del case_path

# %% Figures
checks = {}

# Execution times
checks['execution_time'] = tests.execution_time(project_path, project)

# %% Output
print(tabulate([[os.path.basename(project_path),
                 str(project['cells']),
                 all(checks['execution_time']['passed'])]],
                headers=['case          ', 'nCells',
                         'execution_time']))

# if not all(checks['execution_time']['passed']):
#     print("\033[93mWARNING! Execution time test not passed "
#           f"for case {os.path.basename(project_path)}/\033[0m")
#     print(checks['execution_time'])
