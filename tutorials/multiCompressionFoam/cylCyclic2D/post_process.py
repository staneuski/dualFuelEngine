#!/usr/bin/env python3
# %% [markdown]
# # `tubePurging/` cases post-processing
# %%
import sys
import os
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tabulate import tabulate

sys.path.insert(0, os.path.split(os.path.realpath(__file__))[0]
                   + '/../../../src')
from foam2py.plot_values import *


solvers = ['multiCompressionFoam', 'rhoPimpleFoam']

#- Engine parameters
rpm = 92 # [1/min]
evo = 85 # CA˚ before TDC [deg]
ipo = 42 # CA˚ before BDC [deg]
ipc = ipo # CA˚ after BDC [deg]

# %% Functions initialisation
def get_case_path(solver, case="cylCyclic2D"):
    case_path = os.path.split(os.path.realpath(__file__))[0] + '/'
    if solver != "multiCompressionFoam":
        case_path += f"../../{solver}/{case}/"
    return case_path

def grep_value(key, log="log.checkMesh", pattern='(\d+.\d+)'):
    """Get value in line with key by pattern
    """
    for grep in open(log):
        if key in grep:
            value = re.findall(pattern, grep)

    if pattern == '(\d+)':
        return int(value[0])
    elif pattern == '(\d+.\d+)':
        return float(value[0])
    else:
        return value[0]

def set_engine_plot_parameters():
    """Stardart for all engine plots parameters and annotations
    """
    plt.annotate('(BDC)', (1, 1), xytext=(evo/(evo + 180)*1.16, -0.04),
                 textcoords='axes fraction',
                 horizontalalignment='right', verticalalignment='top')
    plt.annotate('(TDC)', (1, 1), xytext=(0.985, -0.04),
                 textcoords='axes fraction',
                 horizontalalignment='right', verticalalignment='top')
    plt.axvline(x=-180, color ='black', linestyle='--', linewidth=1)
    plt.axvline(x=0, color='black', linestyle='--', linewidth=1)
    plt.axvspan(-ipo - 180, ipo - 180, alpha=0.18, color='grey')

    plt.grid(True)
    plt.legend(loc='best', fontsize=fontsize)
    plt.xlabel('$\\theta$, CA˚', fontsize=fontsize)

# %% Create case set w/ dataframes
df = {'cells': grep_value("nCells:",
                          log=get_case_path(solvers[0])+f"log.blockMesh",
                          pattern='(\d+)')}
for solver in solvers:
    case_path = get_case_path(solver)
    df[solver] = dict(
        execution_time = grep_value("ExecutionTime",
                                    log=case_path+f"log.{solver}"),
        volFieldValue = pd.read_csv(case_path + "postProcessing/"
                                                "volAverageFieldValues/"
                                                "0/volFieldValue.dat",
                                    sep='\t', header=3),
        flowRatePatch = dict(
            inlet = pd.read_csv(case_path + "postProcessing/"
                                            "flowRatePatch(name=inlet)/"
                                            "0/surfaceFieldValue.dat",
                                sep='\t', header=3, names=['time', "phi"]),
            injection = pd.read_csv(case_path + "postProcessing/"
                                                "flowRatePatch(name=injection)/"
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
    # df[solver]['volFieldValue']['volIntegrate(rho)'] = (
    #     pd.read_csv(case_path + "postProcessing/mass/0/volFieldValue.dat",
    #                 sep='\t', header=3)['volIntegrate(rho)']
    # )
del case_path

# %% Mean volFieldValue() parameters
plt.figure(figsize=Figsize*2).suptitle('Mean parameters\nvolFieldValue',
                                     fontweight='bold', fontsize=Fontsize)
subplot = 221
for column, subplot_name, label in zip(
        df["rhoPimpleFoam"]['volFieldValue'].columns[1:].drop('volAverage(K)'),
        ["Pressure", "Temperature", "Density", "Energy", "Mass"],
        ["p, Pa", "T, K", "$\\rho, kg/m^3$", "E, J/kg", "M, kg"]
    ):
    plt.subplot(subplot).set_title(subplot_name + ", " + column,
                                   fontstyle='italic', fontsize=fontsize)
    color = 0
    for solver in solvers:
        plt.plot(df[solver]['volFieldValue']['time']*6*rpm - 180 - evo,
                 df[solver]['volFieldValue'][column],
                 label=solver, linewidth=linewidth)
        if ((solver == "multiCompressionFoam" or solver == "rhoPimpleFoam")
            and (column == "volAverage(e)")):
            plt.plot(df[solver]['volFieldValue']['time']*6*rpm - 180 - evo,
                     df[solver]['volFieldValue']["volAverage(K)"],
                     label=solver + " (K)", linestyle='--', linewidth=linewidth,
                     color='C' + str(color))
            color += 1
    del color
    subplot += 1

    plt.ylabel(label, fontsize=fontsize)
    set_engine_plot_parameters()
del subplot, column, subplot_name, label
plt.savefig(get_case_path(solvers[0])
           + "postProcessing/volFieldValue(time).png")

# %% Mass flow rates flowRatePatch
plt.figure(figsize=Figsize).suptitle("Mass flow rates",
                                   fontweight='bold', fontsize=Fontsize)
for patch in ['inlet', 'injection', 'outlet']:
    if patch == 'outlet':
        linestyle = '--'
    elif patch == 'injection':
        linestyle = ':'
    else:
        linestyle = '-'

    for solver, color in zip(solvers, ['C0', 'C1', 'C2']):
        plt.plot(df[solver]['flowRatePatch'][patch]['time']*6*rpm - 180 - evo,
                 df[solver]['flowRatePatch'][patch]['phi'],
                 label=(solver + ", " + patch),
                 linestyle=linestyle, linewidth=linewidth, color=color)
    del solver, color
del patch, linestyle

plt.gca().invert_yaxis()
plt.ylabel("$\\varphi$, kg/s", fontsize=fontsize)
set_engine_plot_parameters()
plt.savefig(get_case_path(solvers[0])
           + "postProcessing/flowRatePatch(time).png")

# %% Execution times
execution_times = []
for solver in solvers:
    execution_times.append(df[solver]['execution_time'])

plt.figure(figsize=Figsize*0.5).suptitle('Execution time by solver',
                                       fontweight='bold', fontsize=Fontsize)
plt.bar(range(len(solvers)), execution_times,
        color=['C0', 'C1', 'C2'], zorder=3)
plt.grid(zorder=0)
plt.xticks(range(len(solvers)), solvers, fontsize=fontsize)
plt.yticks(fontsize=fontsize)
plt.ylabel("$\\tau$, s", fontsize=fontsize)
plt.savefig(get_case_path(solvers[0])
           + "postProcessing/ExecutionTime(solver).png")

class Output:
    def execution_time(case):
        print(tabulate([['cells', str(df['cells'])]],
                       headers=['', case]), '\n')
        print(tabulate({"solver": solvers,
                        f"time, s": execution_times},
                       headers="keys"))
Output.execution_time("cylCyclic2D")