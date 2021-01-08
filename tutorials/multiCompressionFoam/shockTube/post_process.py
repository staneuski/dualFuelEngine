#!/usr/bin/env python3
# %% [markdown]
# # `shockTube/` cases post-processing
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

solvers = ["multiCompressionFoam", "rhoPimpleFoam", "rhoCentralFoam"]

# %% Functions initialisation
def get_case_path(solver, case='shockTube'):
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

# %% Create case set w/ dataframes
df = {'cells': grep_value("nCells:",
                          log=get_case_path(solvers[0])+f"log.blockMesh",
                          pattern='(\d+)')}
for solver in solvers:
    df[solver] = dict(
        execution_time = grep_value("ExecutionTime",
                                    log=get_case_path(solver)+f"log.{solver}"),
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