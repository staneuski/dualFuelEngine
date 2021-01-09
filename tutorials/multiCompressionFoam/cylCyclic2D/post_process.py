#!/usr/bin/env python3
# %%
import os, sys
project_path = os.path.split(os.path.realpath(__file__))[0]
sys.path.insert(0, project_path + '/../../../src')
from foam2py.imports import *

solvers = ['multiCompressionFoam', 'rhoPimpleFoam']

#- Engine parameters
rpm = 92 # [1/min]
evo = 85 # CA˚ before TDC [deg]
ipo = 42 # CA˚ before BDC [deg]
ipc = ipo # CA˚ after BDC [deg]

# %% Create case set w/ dataframes
project = project = dict(
    cells = openfoam_case.grep_value("nCells:",
                                     log=project_path + "/log.blockMesh",
                                     pattern='(\d+)')
)
for solver in solvers:
    case_path = openfoam_case.rel_path(project_path, solver)
    project[solver] = dict(
        execution_time = openfoam_case.grep_value("ExecutionTime",
                                                  log=case_path
                                                      + f"/log.{solver}"),
        volFieldValue = pd.read_csv(case_path + "/postProcessing/"
                                                "volAverageFieldValues/"
                                                "0/volFieldValue.dat",
                                    sep='\t', header=3),
        flowRatePatch = dict(
            inlet = pd.read_csv(case_path + "/postProcessing/"
                                            "flowRatePatch(name=inlet)/"
                                            "0/surfaceFieldValue.dat",
                                sep='\t', header=3, names=['time', "phi"]),
            injection = pd.read_csv(case_path + "/postProcessing/"
                                                "flowRatePatch(name=injection)/"
                                                "0/surfaceFieldValue.dat",
                                    sep='\t', header=3, names=['time', "phi"]),
            outlet = pd.read_csv(case_path + "/postProcessing/"
                                             "flowRatePatch(name=outlet)/"
                                             "0/surfaceFieldValue.dat",
                                 sep='\t', header=3, names=['time', "phi"]),
        ),
    )
    project[solver]['volFieldValue'] = (
        project[solver]['volFieldValue'].rename(columns={'# Time        ': 'time'})
    )
    # project[solver]['volFieldValue']['volIntegrate(rho)'] = (
    #     pd.read_csv(case_path + "/postProcessing/mass/0/volFieldValue.dat",
    #                 sep='\t', header=3)['volIntegrate(rho)']
    # )
del case_path
print(tabulated.info(project_path, project))

# %% Figures
if plot_figures:
    # Mean volFieldValue() parameters
    figure.volFieldValue(project_path, project,
                        engine=True, rpm=rpm, evo=evo, ipo=ipo)

    # Mass flow rates flowRatePatch
    figure.mass_flow_rate(project_path, project,
                        engine=True, rpm=rpm, evo=evo, ipo=ipo)

# Execution times
execution_times = figure.execution_time(project_path, project,
                                       create_figure=plot_figures)

# %% Output
print(tabulated.times(solvers, execution_times), '\n')