#!/usr/bin/env python3
# %% [markdown]
# # `pipeCompression/` cases post-processing
# %% 
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tabulate import tabulate

solvers = ['multiCompressionFoam', 'rhoPimpleFoam', 'rhoCentralFoam']

#- Adiabatic compression parameters
frequency = 1 # [s]
amplitude = 2 # [m/s]
start = 0.15 # [s]
Cp = 1005 # [J/kg/K]
Cv = Cp - 287 # [J/kg/K]
AREA = 1e-4 # [m^2]
LENGTH = 0.6 # [m]

#- Plot parameters
figsize = 8
figsize_xy_ratio = 1.2
fontsize = 12
linewidth = 2

Figsize = np.array([figsize*figsize_xy_ratio, figsize])
Fontsize = fontsize*figsize_xy_ratio

# %% Functions initialisation
def get_case_path(solver, case="pipeCompression"):
    if solver == "multiCompressionFoam":
        case_path = ""
    else:
        case_path = f"../../{solver}/{case}/"
    return case_path

class GrepLog:
    def execution_time(solver):
        """Get execution time from the log
        """
        for grep in open(get_case_path(solver) + f"log.{solver}"):
            if "ExecutionTime" in grep:
                value = re.findall('(\d+.\d+)', grep)
        return float(value[0])

    def cells_number():
        """Get cells number from the log
        """
        for grep in open("log.checkMesh"):
            if "cells:" in grep:
                value = re.findall('(\d+)', grep)
        return int(value[0])

# %% Create case set w/ dataframes
df = {'cells': GrepLog.cells_number()}
for solver in solvers:
    case_path = get_case_path(solver)
    df[solver] = dict(
        execution_time = GrepLog.execution_time(solver),
        volFieldValue = pd.read_csv(case_path + "postProcessing/"
                                                "volAverageFieldValues/"
                                                "0/volFieldValue.dat",
                                    sep='\t', header=3),
    )
    df[solver]['volFieldValue'] = (
        df[solver]['volFieldValue'].rename(columns={'# Time        ': 'time'})
    )
    df[solver]['volFieldValue']['volIntegrate(rho)'] = (
        pd.read_csv(case_path + "postProcessing/mass/0/volFieldValue.dat",
                    sep='\t', header=3)['volIntegrate(rho)']
    )
del case_path

# Adiabatic process calculation
coord = -amplitude/2/np.pi/frequency*np.cos(
    2*np.pi*frequency*(df['multiCompressionFoam']['volFieldValue']['time']
                       - start)
)
v = (LENGTH - (coord - coord[0]))*AREA

df['adiabatic_process'] = {}
df['adiabatic_process']['volFieldValue'] = {
    'time': df['multiCompressionFoam']['volFieldValue']['time'],
    'volAverage(p)': (df['multiCompressionFoam']['volFieldValue']
                        ['volAverage(p)'][0]
                      *pow(v[0]/v, Cp/Cv)), # p_IC*(V_IC/V)^(Cp/Cv)
    'volAverage(T)': (df['multiCompressionFoam']['volFieldValue']
                        ['volAverage(T)'][0]
                      *pow(v[0]/v, Cp/Cv - 1)), # T_IC*(V_IC/V)^(Cp/Cv - 1)
    'volAverage(rho)': (df['multiCompressionFoam']['volFieldValue']
                          ['volAverage(rho)'][0]
                        *v[0]/v), # rho_IC*(V_IC/V)
    'volAverage(e)': (df['multiCompressionFoam']['volFieldValue']
                        ['volAverage(e)'][0]
                      *pow(v[0]/v, Cp/Cv - 1)), # e_IC*(V_IC/V)^(Cp/Cv - 1)
    'volIntegrate(rho)': np.full(shape=len(df['multiCompressionFoam']['volFieldValue']
                                             ['time']),
                                 fill_value=df['multiCompressionFoam']['volFieldValue']
                                             ['volIntegrate(rho)'][0])
}

print(f"Compression ratio: {max(v)/min(v):.3f}")
del coord, v

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
    for solver in ['multiCompressionFoam', 'rhoPimpleFoam', 'rhoCentralFoam',
                   'adiabatic_process']:
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
plt.savefig("postProcessing/ExecutionTime(solver).png")

class Output:
    def execution_time(case):
        print(tabulate([['cells', str(df['cells'])]],
                       headers=['', case]), '\n')
        print(tabulate({"solver": solvers,
                        f"time, s": execution_times},
                       headers="keys"))
Output.execution_time("pipeCompression")