#!/usr/bin/env python3
# %% [markdown]
# # `shockTube/` cases post-processing
# %%
import os
import re
import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate

solvers = ["multiCompressionFoam", "rhoPimpleFoam", "rhoCentralFoam"]

figsize = 8
figsize_xy_ratio = 1.2
fontsize = 12
linewidth = 2

Figsize = np.array([figsize*figsize_xy_ratio, figsize])
Fontsize = fontsize*figsize_xy_ratio

# %% Initialisation
def get_case_path(solver, case='shockTube'):
    case_path = os.path.split(os.path.realpath(__file__))[0] + '/'
    if solver != "multiCompressionFoam":
        case_path += f"../../{solver}/{case}/"
    return case_path

class GrepLog:
    def execution_time(solver):
        """Get execution time from the log
        """
        for grep in open(get_case_path(solver) + f"log.{solver}"):
            if "ExecutionTime" in grep:
                value = re.findall('(\d+.\d+)', grep)
        return float(value[0])

    def cells_number(solver):
        """Get cells number from the log
        """
        for grep in open(get_case_path(solver) + "log.checkMesh"):
            if "cells:" in grep:
                value = re.findall('(\d+)', grep)
        return int(value[0])

# %% Create case set w/ dataframes
df = {'cells': GrepLog.cells_number(solvers[0])}
for solver in solvers:
    df[solver] = dict(
        execution_time = GrepLog.execution_time(solver),
    )

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
plt.savefig(get_case_path(solvers[0])
           + "postProcessing/ExecutionTime(solver).png")

class Output:
    def execution_time(case):
        print(tabulate([['cells', str(df['cells'])]],
                       headers=['', case]), '\n')
        print(tabulate({"solver": solvers,
                        f"time, s": execution_times},
                       headers="keys"))
Output.execution_time('shockTube')