#!/usr/bin/env python3
# %% [markdown]
# # `tubePurging/` cases post-processing
# %% 
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tabulate import tabulate

solvers = ['multiCompressionFoam', 'rhoPimpleFoam', 'rhoCentralFoam']

#- Plot parameters
figsize = 8
figsize_xy_ratio = 1.2
fontsize = 12
linewidth = 2

Figsize = np.array([figsize*figsize_xy_ratio, figsize])
Fontsize = fontsize*figsize_xy_ratio

# %% Functions initialisation
def get_case_path(solver, case="tubePurging"):
    if solver == "multiCompressionFoam":
        case_path = ""
    else:
        case_path = f"../../{solver}/{case}/"
    return case_path

def grep_execution_time(solver):
    """Get execution time from the log
    """
    for grep in open(f"{get_case_path(solver)}log.{solver}"):
        if "ExecutionTime" in grep:
            execution_time = re.findall('(\d+.\d+)', grep)
    return float(execution_time[0])

# %% Create case set w/ dataframes
df = {}
for solver in solvers:
    case_path = get_case_path(solver)
    df[solver] = dict(
        execution_time = grep_execution_time(solver),
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

# %% Mean volFieldValue() parameters
plt.figure(figsize=Figsize*2).suptitle('Mean parameters\nvolFieldValue',
                                     fontweight='bold', fontsize=Fontsize)
subplot = 321
for column, subplot_name, label in zip(
        df["rhoPimpleFoam"]['volFieldValue'].columns[1:][1:-1],
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
plt.savefig("postProcessing/volFieldValue(time).png")

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
plt.savefig("postProcessing/flowRatePatch(time).png")

# %% Execution times
execution_times = []
for solver in solvers:
    execution_times.append(df[solver]['execution_time'])

print(tabulate({"Solver": solvers, "ExecutionTime": execution_times},
               headers="keys"))

plt.figure(figsize=Figsize*0.7).suptitle('Execution time by solver',
                                       fontweight='bold', fontsize=Fontsize)
plt.bar(range(len(solvers)), execution_times,
        color=['C0', 'C1', 'C2'], zorder=3)
plt.grid(zorder=0)
plt.xticks(range(len(solvers)), solvers, fontsize=fontsize)
plt.yticks(fontsize=fontsize)
plt.ylabel("$\\tau$, s", fontsize=fontsize)
plt.savefig("postProcessing/ExecutionTime(solver).png")