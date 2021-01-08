import numpy as np
import matplotlib.pyplot as plt
from foam2py.plot_values import *

def execution_time(case_data, post_process_path):
    """Create execution times bar plot and return execution times array
    """
    # Intersection array w/ solvers names
    solvers = np.intersect1d(
        ['multiCompressionFoam', 'rhoPimpleFoam', 'rhoCentralFoam'],
        np.array(list(case_data.keys()))
    )

    # Create execution times array
    execution_times, colors = [], []
    for i in range(len(solvers)):
        execution_times.append(case_data[solvers[i]]['execution_time'])
        colors.append('C' + str(i))

    # Plot bar figure
    plt.figure(figsize=Figsize*0.7).suptitle('Execution time by solver',
                                           fontweight='bold',
                                           fontsize=Fontsize)
    plt.bar(range(len(solvers)), execution_times,
            color=['C0', 'C1', 'C2'], zorder=3)
    plt.grid(zorder=0)
    plt.xticks(range(len(solvers)), solvers,
               fontsize=fontsize)
    plt.yticks(fontsize=fontsize)
    plt.ylabel("$\\tau$, s", fontsize=fontsize)
    plt.savefig(post_process_path
               + "/postProcessing/ExecutionTime(solver).png")

    return execution_times
