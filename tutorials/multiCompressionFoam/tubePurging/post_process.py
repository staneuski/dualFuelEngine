#!/usr/bin/env python3
# %% [markdown]
# # `tubePurging/` cases post-processing
# %%
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

post_process_path = os.path.split(os.path.realpath(__file__))[0]
sys.path.insert(0, post_process_path + '/../../../src')
import foam2py.openfoam_case as openfoam_case
import foam2py.tabulated as tabulated
from foam2py.plot_values import *

solvers = ['multiCompressionFoam', 'rhoPimpleFoam', 'rhoCentralFoam']

# %% Create case set w/ dataframes
df = {'cells': openfoam_case.grep_value("nCells:",
                                        log=post_process_path
                                            + "/log.blockMesh",
                                        pattern='(\d+)')}
for solver in solvers:
    case_path = openfoam_case.rel_path(post_process_path, solver)
    df[solver] = dict(
        execution_time = openfoam_case.grep_value("ExecutionTime",
                                                  log=case_path
                                                      + f"log.{solver}"),
        volFieldValue = pd.read_csv(case_path + "postProcessing/"
                                                "volAverageFieldValues/"
                                                "0/volFieldValue.dat",
                                    sep='\t', header=3),
        flowRatePatch = dict(
            inlet = pd.read_csv(case_path + "postProcessing/"
                                            "flowRatePatch(name=inlet)/"
                                            "0/surfaceFieldValue.dat",
                                sep='\t', header=3, names=['time', "phi"]),
            outlet = pd.read_csv(case_path + "postProcessing/"
                                             "flowRatePatch(name=outlet)/"
                                             "0/surfaceFieldValue.dat",
                                 sep='\t', header=3, names=['time', "phi"]),
        ),
    )
    df[solver]['volFieldValue'] = (
        df[solver]['volFieldValue'].rename(columns={'# Time        ': 'time'})
    )
    df[solver]['volFieldValue']['volIntegrate(rho)'] = (
        pd.read_csv(case_path + "postProcessing/mass/0/volFieldValue.dat",
                    sep='\t', header=3)['volIntegrate(rho)']
    )
del case_path
print(tabulated.create_info(post_process_path, df))

# %% Mean volFieldValue() parameters
plt.figure(figsize=Figsize*2).suptitle('Mean parameters\nvolFieldValue',
                                     fontweight='bold', fontsize=Fontsize)
subplot = 321
for column, subplot_name, label in zip(
        df["rhoPimpleFoam"]['volFieldValue'].columns[1:].drop('volAverage(K)'),
        ["Pressure", "Temperature", "Density", "Energy", "Mass"],
        ["p, Pa", "T, K", "$\\rho, kg/m^3$", "E, J/kg", "M, kg"]
    ):
    plt.subplot(subplot).set_title(subplot_name + ", " + column,
                                   fontstyle='italic', fontsize=fontsize)
    color = 0
    for solver in solvers:
        plt.plot(df[solver]['volFieldValue']['time']*1e+3,
                 df[solver]['volFieldValue'][column],
                 label=solver, linewidth=linewidth)
        if ((solver == "multiCompressionFoam" or solver == "rhoPimpleFoam")
            and (column == "volAverage(e)")):
            plt.plot(df[solver]['volFieldValue']['time']*1e+3,
                     df[solver]['volFieldValue']["volAverage(K)"],
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
plt.savefig(post_process_path + "/postProcessing/volFieldValue(time).png")

# %% Mass flow rates flowRatePatch
plt.figure(figsize=Figsize).suptitle("Mass flow rates",
                                   fontweight='bold', fontsize=Fontsize)
for patch in ['inlet', 'outlet']:
    if patch == 'outlet':
        linestyle = '--'
    else:
        linestyle = '-'

    for solver, color in zip(solvers, ['C0', 'C1', 'C2']):
        plt.plot(df[solver]['flowRatePatch'][patch]['time']*1e+3,
                 df[solver]['flowRatePatch'][patch]['phi'],
                 label=(solver + ", " + patch),
                 linestyle=linestyle, linewidth=linewidth, color=color)
    del solver, color
del patch, linestyle

plt.gca().invert_yaxis()
plt.grid(True)
plt.legend(loc="best", fontsize=fontsize)
plt.xlabel("$\\tau$, ms", fontsize=fontsize)
plt.ylabel("$\\varphi$, kg/s", fontsize=fontsize)
plt.tick_params(axis="both", labelsize=fontsize)
plt.savefig(post_process_path + "/postProcessing/flowRatePatch(time).png")

# %% Execution times
execution_times = []
for solver in solvers:
    execution_times.append(df[solver]['execution_time'])

plt.figure(figsize=Figsize*0.7).suptitle('Execution time by solver',
                                       fontweight='bold', fontsize=Fontsize)
plt.bar(range(len(solvers)), execution_times,
        color=['C0', 'C1', 'C2'], zorder=3)
plt.grid(zorder=0)
plt.xticks(range(len(solvers)), solvers, fontsize=fontsize)
plt.yticks(fontsize=fontsize)
plt.ylabel("$\\tau$, s", fontsize=fontsize)
plt.savefig(post_process_path + "/postProcessing/ExecutionTime(solver).png")

print(tabulated.create_times(solvers, execution_times))