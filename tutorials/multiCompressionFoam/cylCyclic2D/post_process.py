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

solvers = ['multiCompressionFoam', 'rhoPimpleFoam']

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
        execution_time = openfoam_case.grep_value("ExecutionTime",
                                                  log=case_path
                                                      + f"/log.{solver}"),
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
    # project[solver]['volFieldValue']['volIntegrate(rho)'] = (
    #     pd.read_csv(case_path + "/postProcessing/mass/0/volFieldValue.dat",
    #                 sep='\t', header=3)['volIntegrate(rho)']
    # )
del case_path

# %% Checks
checks = {}

# Execution times
checks['execution_time'] = tests.execution_time(project_path, project)

# Mean volFieldValue() parameters
checks['vol'] = tests.volFieldValue(project_path, project,
                                    engine=True, rpm=rpm, evo=evo, ipo=ipo)

# Mass flow rates flowRatePatch
checks['phi'] = tests.mass_flow_rate(project_path, project,
                                    engine=True, rpm=rpm, evo=evo, ipo=ipo)

# %% Output
print(tabulate([[os.path.basename(project_path),
                 str(project['cells']),
                 all(checks['execution_time']['passed']),
                 all(checks['vol']['passed']),
                 all(checks['phi']['passed'])]],
                headers=['case          ', 'nCells',
                         'execution_time', 'vol', 'phi']))

# if not all(checks['execution_time']['passed']):
#     print("\033[93mWARNING! Execution time test not passed "
#           f"for case {os.path.basename(project_path)}/\033[0m")
#     print(checks['execution_time'])

# if not all(checks['vol']['passed']):
#     print("\033[93mWARNING! Volume averaged test not passed "
#           f"for case {os.path.basename(project_path)}/\033[0m")
#     print(checks['vol'])