#!/usr/bin/env python3
# %%
import os, sys
project_path = os.path.split(os.path.realpath(__file__))[0]
sys.path.insert(0, project_path + '/../../../src')
from foam2py.imports import *

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

# %% Figures
# Execution times
execution_times = figure.execution_time(project_path, project,
                                       create_figure=plot_figures)

# %% Output
print(tabulated.times(solvers, execution_times), '\n')