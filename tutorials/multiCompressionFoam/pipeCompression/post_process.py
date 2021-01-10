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

solvers = ["multiCompressionFoam", "rhoPimpleFoam", "rhoCentralFoam"]
fields = ["alphaAir", "alphaExh", "alphaGas", "Ma", 'p', "phi", "rho", 'T']

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
        exec_time = openfoam_case.grep_value("ExecutionTime",
                                             log=case_path + f"/log.{solver}"),
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
checks['vol'] = tests.volFieldValue(project_path, project)

# %% Output
output.info(project_path, project, checks)
# print(f"Compression ratio: {max(v)/min(v):.3f}")
