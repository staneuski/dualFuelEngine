import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

from foam2py.plot_values import *

try:
    get_ipython
    plot_figures = True
except:
    plot_figures = False

MEAN_ERROR = 10

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


def volFieldValue(project_path, project, engine=False, rpm=92, evo=85, ipo=42):
    def calc_errors(df1, df2, solver, column='volAverage(p)'):
        df1, df2 = df1['volFieldValue'], df2['volFieldValue']
        f = interp1d(df2['time'], df2[column], fill_value="extrapolate")
        errs = (df1[column] - f(df1['time']))/df1[column]*100
        return (column, solver,
                (np.mean(errs) < MEAN_ERROR
                     or np.mean(errs) == np.Infinity),
                np.mean(errs), np.max(errs))

    solvers, colors = create_solvers_and_colors(project)

    checks = []
    for solver in solvers:
        for column in (project['rhoPimpleFoam']['volFieldValue'].columns[1:]
                            .drop('volAverage(e)').drop('volAverage(K)')
                            .drop('volAverage(rho)')):
            if solver != 'multiCompressionFoam':
                checks.append(
                    calc_errors(project['multiCompressionFoam'], project[solver],
                                solver=solver, column=column)
                )
    checks = pd.DataFrame(checks,
                          columns=['par', 'solver', 'passed', 'mean', 'max'])

    if plot_figures:
        plt.figure(figsize=Figsize*2).suptitle('Mean parameters\nvolFieldValue',
                                             fontweight='bold',
                                             fontsize=Fontsize)
        subplot = 321
        for column, subplot_name, label in zip(
                project['rhoPimpleFoam']['volFieldValue']
                       .columns[1:].drop('volAverage(K)'),
                ["Pressure", "Temperature", "Density", "Energy", "Mass"],
                ["p, Pa", "T, K", "$\\rho, kg/m^3$", "E, J/kg", "M, kg"]
            ):
            plt.subplot(subplot).set_title(subplot_name + ", " + column,
                                           fontstyle='italic', fontsize=fontsize)

            for solver, color in zip(solvers, colors):
                time = project[solver]['volFieldValue']['time']
                if engine:
                    time = time*6*rpm - 180 - evo
                plt.plot(time, project[solver]['volFieldValue'][column],
                        label=solver, linewidth=linewidth)
                if ((solver == "multiCompressionFoam"
                     or solver == "rhoPimpleFoam")
                    and (column == "volAverage(e)")):
                    plt.plot(time,
                             project[solver]['volFieldValue']["volAverage(K)"],
                            label=solver + " (K)", linestyle='--', linewidth=linewidth,
                            color=color)
            subplot += 1

            plt.ylabel(label, fontsize=fontsize)
            if engine:
                engine_plot_parameters(evo, ipo)
            else:
                plt.grid(True)
                plt.legend(loc="best", fontsize=fontsize)
                plt.xlabel("$\\tau$, ms", fontsize=fontsize)
                plt.tick_params(axis="both", labelsize=fontsize)
        plt.savefig(project_path + "/postProcessing/volFieldValue(time).png")
    return checks


def mass_flow_rate(project_path, project,
        engine=False, rpm=92, evo=85, ipo=42):

    solvers, colors = create_solvers_and_colors(project)
    checks = []
    for solver in solvers:
        for patch in list(project['multiCompressionFoam']
                                 ['flowRatePatch'].keys()):
            if solver != 'multiCompressionFoam':
                time1, phi1 = (
                    project['multiCompressionFoam']['flowRatePatch']
                           [patch]['time'],
                    project['multiCompressionFoam']['flowRatePatch']
                           [patch]['phi'],
                )
                time2, phi2 = (
                    project[solver]['flowRatePatch']
                           [patch]['time'],
                    project[solver]['flowRatePatch']
                           [patch]['phi'],
                )
                f = interp1d(time2, phi2, fill_value="extrapolate")
                errs = (phi1 - f(time1))/phi1*100
                checks.append([
                    patch, solver,
                    (np.mean(errs) < MEAN_ERROR
                     or np.mean(errs) == np.Infinity),
                    np.mean(errs), np.max(errs)
                ])
    checks = pd.DataFrame(checks,
                          columns=['patch', 'solver', 'passed', 'mean', 'max'])

    if plot_figures:
        plt.figure(figsize=Figsize).suptitle("Mass flow rates",
                                           fontweight='bold',
                                           fontsize=Fontsize)
        for patch in list(project['multiCompressionFoam']
                                 ['flowRatePatch'].keys()):
            if patch == 'outlet':
                linestyle = '--'
            elif patch == 'injection':
                linestyle = ':'
            else:
                linestyle = '-'

            for solver, color in zip(solvers, colors):
                time = project[solver]['flowRatePatch'][patch]['time']
                if engine:
                    time = time*6*rpm - 180 - evo
                plt.plot(time, project[solver]['flowRatePatch'][patch]['phi'],
                         label=(solver + ", " + patch), linestyle=linestyle,
                         linewidth=linewidth, color=color)

        plt.gca().invert_yaxis()
        plt.ylabel("$\\varphi$, kg/s", fontsize=fontsize)

        if engine:
            engine_plot_parameters(evo, ipo)
        else:
            plt.grid(True)
            plt.legend(loc="best", fontsize=fontsize)
            plt.tick_params(axis="both", labelsize=fontsize)
            plt.xlabel("$\\tau$, ms", fontsize=fontsize)
        plt.savefig(project_path + "/postProcessing/flowRatePatch(time).png")
    return checks


def execution_time(project_path, project):
    """Create execution times bar plot and return execution times array
    """
    solvers, colors = create_solvers_and_colors(project)
    checks = []
    for solver in solvers:
        delta = (project['multiCompressionFoam']['execution_time']
                 - project[solver]['execution_time'])
        checks.append([
            solver,
            delta <= 0,
            project[solver]['execution_time'],
            delta
        ])
    checks = pd.DataFrame(checks,
                          columns=['solver', 'passed', 'execution_time', 'delta'])

    if plot_figures:
        plt.figure(figsize=Figsize*0.7).suptitle('Execution time by solver',
                                               fontweight='bold',
                                               fontsize=Fontsize)
        plt.bar(range(len(solvers)), checks['execution_time'],
                color=['C0', 'C1', 'C2'], zorder=3)
        plt.grid(zorder=0)
        plt.xticks(range(len(solvers)), solvers,
                   fontsize=fontsize)
        plt.yticks(fontsize=fontsize)
        plt.ylabel("$\\tau$, s", fontsize=fontsize)
        plt.savefig(project_path
                   + "/postProcessing/ExecutionTime(solver).png")

    return checks
