#!/usr/bin/env python3
# %% [markdown]
# # `shockTube/` cases post-processing
# %%
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

project_path = os.path.split(os.path.realpath(__file__))[0]
sys.path.insert(0, project_path + '/../../../src')
import foam2py.openfoam_case as openfoam_case
import foam2py.figure as figure
import foam2py.tabulated as tabulated

from foam2py.plot_values import *

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
print(tabulated.info(project_path, project))

# %% Execution times
execution_times = figure.execution_time(project_path, project)
print(tabulated.times(solvers, execution_times), '\n')