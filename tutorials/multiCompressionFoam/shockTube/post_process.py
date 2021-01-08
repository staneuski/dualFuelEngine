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

post_process_path = os.path.split(os.path.realpath(__file__))[0]
sys.path.insert(0, post_process_path + '/../../../src')
import foam2py.openfoam_case as openfoam_case
from foam2py.plot_values import *

solvers = ["multiCompressionFoam", "rhoPimpleFoam", "rhoCentralFoam"]

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
    )
del case_path


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

class Output:
    def execution_time(case):
        print(tabulate([['cells', str(df['cells'])]],
                       headers=['', case]), '\n')
        print(tabulate({"solver": solvers,
                        f"time, s": execution_times},
                       headers="keys"))
Output.execution_time('shockTube')