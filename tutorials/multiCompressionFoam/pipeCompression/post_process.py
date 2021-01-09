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

solvers = ['multiCompressionFoam', 'rhoPimpleFoam', 'rhoCentralFoam']

#- Adiabatic compression parameters
frequency = 1 # [s]
amplitude = 2 # [m/s]
start = 0.15 # [s]
Cp = 1005 # [J/kg/K]
Cv = Cp - 287 # [J/kg/K]
AREA = 1e-4 # [m^2]
LENGTH = 0.6 # [m]

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
    )
    project[solver]['volFieldValue'] = (
        project[solver]['volFieldValue'].rename(columns={'# Time        ': 'time'})
    )
    project[solver]['volFieldValue']['volIntegrate(rho)'] = (
        pd.read_csv(case_path + "/postProcessing/mass/0/volFieldValue.dat",
                    sep='\t', header=3)['volIntegrate(rho)']
    )
del case_path

# Adiabatic process calculation
coord = -amplitude/2/np.pi/frequency*np.cos(
    2*np.pi*frequency*(project['multiCompressionFoam']['volFieldValue']['time']
                       - start)
)
v = (LENGTH - (coord - coord[0]))*AREA

project['adiabatic_process'] = {}
project['adiabatic_process']['volFieldValue'] = {
    'time': project['multiCompressionFoam']['volFieldValue']['time'],
    # p_IC*(V_IC/V)^(Cp/Cv)
    'volAverage(p)': (project['multiCompressionFoam']
                             ['volFieldValue']['volAverage(p)'][0]
                      *pow(v[0]/v, Cp/Cv)),
    # T_IC*(V_IC/V)^(Cp/Cv - 1)
    'volAverage(T)': (project['multiCompressionFoam']
                             ['volFieldValue']['volAverage(T)'][0]
                      *pow(v[0]/v, Cp/Cv - 1)),
    # rho_IC*(V_IC/V)
    'volAverage(rho)': (project['multiCompressionFoam']
                               ['volFieldValue']['volAverage(rho)'][0]
                        *v[0]/v),
    # e_IC*(V_IC/V)^(Cp/Cv - 1)
    'volAverage(e)': (project['multiCompressionFoam']
                             ['volFieldValue']['volAverage(e)'][0]
                      *pow(v[0]/v, Cp/Cv - 1)),
    'volIntegrate(rho)': np.full(shape=len(project['multiCompressionFoam']
                                                  ['volFieldValue']['time']),
                                 fill_value=project['multiCompressionFoam']
                                                  ['volFieldValue']
                                                  ['volIntegrate(rho)'][0])
}
del coord, v

# %% Figures
checks = {}

# Execution times
checks['execution_time'] = tests.execution_time(project_path, project)

# Mean volFieldValue() parameters
checks['vol'] = tests.volFieldValue(project_path, project)

# %% Output
# print(f"Compression ratio: {max(v)/min(v):.3f}")

print(tabulate([[os.path.basename(project_path),
                 str(project['cells']),
                 all(checks['execution_time']['passed']),
                 all(checks['vol']['passed'])]],
                headers=['case          ', 'nCells',
                         'execution_time', 'vol']))

# if not all(checks['execution_time']['passed']):
#     print("\033[93mWARNING! Execution time test not passed "
#           f"for case {os.path.basename(project_path)}/\033[0m")
#     print(checks['execution_time'])

# if not all(checks['vol']['passed']):
#     print("\033[93mWARNING! Volume averaged test not passed "
#           f"for case {os.path.basename(project_path)}/\033[0m")
#     print(checks['vol'])