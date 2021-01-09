import numpy as np
import matplotlib.pyplot as plt
from foam2py.plot_values import *


def create_solvers_and_colors(project):
    solvers = np.intersect1d(
        ['multiCompressionFoam', 'rhoPimpleFoam', 'rhoCentralFoam'],
        list(project.keys())
    )

    colors = []
    for i in range(len(solvers)):
        colors.append('C' + str(i))

    return solvers.tolist(), colors


def engine_plot_parameters(evo, ipo):
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


def mass_flow_rate(project_path, project, engine=False, rpm=92, evo=85, ipo=42):
    plt.figure(figsize=Figsize).suptitle("Mass flow rates",
                                       fontweight='bold', fontsize=Fontsize)
    for patch in list(project['multiCompressionFoam']
                             ['flowRatePatch'].keys()):
        if patch == 'outlet':
            linestyle = '--'
        elif patch == 'injection':
            linestyle = ':'
        else:
            linestyle = '-'

        solvers, colors = create_solvers_and_colors(project)
        for solver, color in zip(solvers, colors):
            time = project[solver]['flowRatePatch'][patch]['time']
            if engine:
                time = time*6*rpm - 180 - evo
            plt.plot(time, project[solver]['flowRatePatch'][patch]['phi'],
                     label=(solver + ", " + patch),
                     linestyle=linestyle, linewidth=linewidth, color=color)
        del solvers, colors, solver, color, time
    del patch, linestyle

    if engine:
        engine_plot_parameters(evo, ipo)
    else:
        plt.gca().invert_yaxis()
        plt.grid(True)
        plt.legend(loc="best", fontsize=fontsize)
        plt.tick_params(axis="both", labelsize=fontsize)
        plt.xlabel("$\\tau$, ms", fontsize=fontsize)

    plt.ylabel("$\\varphi$, kg/s", fontsize=fontsize)

    plt.savefig(project_path + "/postProcessing/flowRatePatch(time).png")


def execution_time(project_path, project):
    """Create execution times bar plot and return execution times array
    """
    # Create execution times array
    execution_times = []
    solvers, colors = create_solvers_and_colors(project)
    for solver in solvers:
        execution_times.append(project[solver]['execution_time'])

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
    plt.savefig(project_path
               + "/postProcessing/ExecutionTime(solver).png")
    return execution_times

