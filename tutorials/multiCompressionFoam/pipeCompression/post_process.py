#!/usr/bin/env python3
# %% [markdown]
# # `pipeCompression/` cases post-processing
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

# %% Initialisation
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
    'volAverage(p)': (project['multiCompressionFoam']['volFieldValue']
                        ['volAverage(p)'][0]
                      *pow(v[0]/v, Cp/Cv)), # p_IC*(V_IC/V)^(Cp/Cv)
    'volAverage(T)': (project['multiCompressionFoam']['volFieldValue']
                        ['volAverage(T)'][0]
                      *pow(v[0]/v, Cp/Cv - 1)), # T_IC*(V_IC/V)^(Cp/Cv - 1)
    'volAverage(rho)': (project['multiCompressionFoam']['volFieldValue']
                          ['volAverage(rho)'][0]
                        *v[0]/v), # rho_IC*(V_IC/V)
    'volAverage(e)': (project['multiCompressionFoam']['volFieldValue']
                        ['volAverage(e)'][0]
                      *pow(v[0]/v, Cp/Cv - 1)), # e_IC*(V_IC/V)^(Cp/Cv - 1)
    'volIntegrate(rho)': np.full(shape=len(project['multiCompressionFoam']['volFieldValue']
                                             ['time']),
                                 fill_value=project['multiCompressionFoam']['volFieldValue']
                                             ['volIntegrate(rho)'][0])
}

print(f"Compression ratio: {max(v)/min(v):.3f}")
del coord, v

# %% Figures
# Mean volFieldValue() parameters
plt.figure(figsize=Figsize*2).suptitle('Mean parameters\nvolFieldValue',
                                     fontweight='bold', fontsize=Fontsize)
subplot = 321
for column, subplot_name, label in zip(
        project["rhoPimpleFoam"]['volFieldValue'].columns[1:].drop('volAverage(K)'),
        ["Pressure", "Temperature", "Density", "Energy", "Mass"],
        ["p, Pa", "T, K", "$\\rho, kg/m^3$", "E, J/kg", "M, kg"]
    ):
    plt.subplot(subplot).set_title(subplot_name + ", " + column,
                                   fontstyle='italic', fontsize=fontsize)
    color = 0
    for solver in ['multiCompressionFoam', 'rhoPimpleFoam', 'rhoCentralFoam',
                   'adiabatic_process']:
        plt.plot(project[solver]['volFieldValue']['time']*1e+3,
                 project[solver]['volFieldValue'][column],
                 label=solver, linewidth=linewidth)
        if ((solver == "multiCompressionFoam" or solver == "rhoPimpleFoam")
            and (column == "volAverage(e)")):
            plt.plot(project[solver]['volFieldValue']['time']*1e+3,
                     project[solver]['volFieldValue']["volAverage(K)"],
                     label=solver + " (K)", linestyle='--', linewidth=linewidth,
                     color='C' + str(color))
            color += 1
    del color
    subplot += 1

    plt.grid(True)
    plt.legend(loc="best", fontsize=fontsize)
    plt.xlabel("$\\tau$, ms", fontsize=fontsize)
    plt.ylabel(label, fontsize=fontsize)
    plt.tick_params(axis="both", labelsize=fontsize)
del subplot, column, subplot_name, label
plt.savefig(project_path + "/postProcessing/volFieldValue(time).png")

# Execution times
execution_times = figure.execution_time(project_path, project)

# %% Output
print(tabulated.times(solvers, execution_times), '\n')