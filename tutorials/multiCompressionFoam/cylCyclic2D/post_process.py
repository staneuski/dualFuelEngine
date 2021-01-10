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
import foam2py.output as output

solvers = ["multiCompressionFoam", "rhoPimpleFoam"]
fields = ["alphaAir", "alphaExh", "alphaGas", "Ma", 'p', "phi", "rho", 'T']

#- Engine parameters
rpm = 92 # [1/min]
evo = 85 # CA˚ before TDC [deg]
ipo = 42 # CA˚ before BDC [deg]
ipc = ipo # CA˚ after BDC [deg]

# %% Create case set w/ dataframes
project = project = dict(
    cells = openfoam_case.grep_value("nCells:",
                                     log=project_path + "/log.blockMesh",
                                     pattern='(\d+)')
)
for solver in solvers:
    case_path = openfoam_case.rel_path(project_path, solver)
    project[solver] = dict(
        exec_time = openfoam_case.grep_value("ExecutionTime",
                                             log=case_path + f"/log.{solver}"),
        volFieldValue = pd.read_csv(case_path + "/postProcessing/"
                                                "volAverageFieldValues/"
                                                "0/volFieldValue.dat",
                                    sep='\t', header=3),
        flowRatePatch = dict(
            inlet = pd.read_csv(case_path + "/postProcessing/"
                                            "flowRatePatch(name=inlet)/"
                                            "0/surfaceFieldValue.dat",
                                sep='\t', header=3, names=['time', "phi"]),
            injection = pd.read_csv(case_path + "/postProcessing/"
                                                "flowRatePatch(name=injection)/"
                                                "0/surfaceFieldValue.dat",
                                    sep='\t', header=3, names=['time', "phi"]),
            outlet = pd.read_csv(case_path + "/postProcessing/"
                                             "flowRatePatch(name=outlet)/"
                                             "0/surfaceFieldValue.dat",
                                 sep='\t', header=3, names=['time', "phi"]),
        ),
    )
    project[solver]['volFieldValue'] = (
        project[solver]['volFieldValue'].rename(columns={'# Time        ': 'time'})
    )
del case_path

# %% Checks
checks = {}
checks['field_extremums'], extremums = [], {}
for field in fields:
    extremums[field] = tests.field_extremums(project_path, field=field,
                                            cells=project['cells'])
    checks['field_extremums'].append([field, all(extremums[field])])
checks['field_extremums'] = pd.DataFrame(checks['field_extremums'],
                                        columns=['field', 'passed'])

# Execution times
checks['exec_time'] = tests.execution_time(project_path, project)

# Mean volFieldValue() parameters
checks['vol'] = tests.volFieldValue(project_path, project,
                                    engine=True, rpm=rpm, evo=evo, ipo=ipo)

# Mass flow rates flowRatePatch
checks['phi'] = tests.mass_flow_rate(project_path, project,
                                    engine=True, rpm=rpm, evo=evo, ipo=ipo)

# %% Output
output.info(project_path, project, checks)
