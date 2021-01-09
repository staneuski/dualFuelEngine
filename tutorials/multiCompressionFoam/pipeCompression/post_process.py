#!/usr/bin/env python3
# %% Import
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

# %% Initialisation
solvers = ['multiCompressionFoam', 'rhoPimpleFoam', 'rhoCentralFoam']

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
print(tabulated.info(project_path, project))

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
print(f"Compression ratio: {max(v)/min(v):.3f}")
del coord, v

# %% Figures
# Mean volFieldValue() parameters
figure.volFieldValue(project_path, project)

# Execution times
execution_times = figure.execution_time(project_path, project)

# %% Output
print(tabulated.times(solvers, execution_times), '\n')