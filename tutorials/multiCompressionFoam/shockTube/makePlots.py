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
    df[solver] = dict(
        execution_time = grep_execution_time(solver),
    )

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