#!/usr/bin/env python3
'''----------------------------------------------------------------------------
       ___       |
     _|o_ |_     |   Language: Python 3.x
    /  ___| \    |   Website: https://github.com/StasF1/dualFuelEngine
    \_| ____/    |   Copyright (C) 2020 Stanislau Stasheuski
      |__o|      |
----------------------------------------------------------------------------'''

import re
import numpy as np
import matplotlib.pyplot as plt

# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
# User-defined parameters

#- Plot parameters
xFigSize       = 10
yFigSize       = 8

titleFontSize  = 16
subplotFontSize= 14
labelFontSize  = 16
legendFontSize = 12
ticksFontSize  = 12

linewidthHeavy = 2
linewidthLight = 1

fieldNames = [
    "Pressure",
    "Temperature",
    "Density",
    "Energy"
]
fields = ["p, Pa", "T, K", "$\\rho, kg/m^3$", "e, J/kg", "K, J/kg", "E, J/kg"]

solvers = [ "multiCompressionFoam", "rhoPimpleFoam", "rhoCentralFoam"]

# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

def getExecutionTime( solver ):
    ''' Get execution time from the log '''

    for grep in open(f"tubePurging_{solver}/log.{solver}"):
        if "ExecutionTime" in grep:
            ExecutionTime = re.findall('(\d+.\d+)', grep)
    print(f"{solver} execution time: {ExecutionTime[0]} s")

    return float(ExecutionTime[0])


# Get data
# ~~~~~~~~
#- multiCompressionFoam
multiCompressionFoam = [
    np.loadtxt(
        'tubePurging_multiCompressionFoam/postProcessing/volAverageFieldValues/0/volFieldValue.dat',
        skiprows = 4
    ),
    np.loadtxt(
        'tubePurging_multiCompressionFoam/postProcessing/flowRatePatch(name=inlet)/0/surfaceFieldValue.dat',
        skiprows = 4
    ),
    np.loadtxt(
        'tubePurging_multiCompressionFoam/postProcessing/flowRatePatch(name=outlet)/0/surfaceFieldValue.dat',
        skiprows = 4
    ),
    np.loadtxt(
        "tubePurging_multiCompressionFoam/postProcessing/mass/0/volFieldValue.dat",
        skiprows = 4
    )
]

#- rhoPimpleFoam
rhoPimpleFoam = [
    np.loadtxt(
        'tubePurging_rhoPimpleFoam/postProcessing/volAverageFieldValues/0/volFieldValue.dat',
        skiprows = 4
    ),
    np.loadtxt(
        'tubePurging_rhoPimpleFoam/postProcessing/flowRatePatch(name=inlet)/0/surfaceFieldValue.dat',
        skiprows = 4
    ),
    np.loadtxt(
        'tubePurging_rhoPimpleFoam/postProcessing/flowRatePatch(name=outlet)/0/surfaceFieldValue.dat',
        skiprows = 4
    ),
    np.loadtxt(
        "tubePurging_rhoPimpleFoam/postProcessing/mass/0/volFieldValue.dat",
        skiprows = 4
    )
]

#- rhoCentralFoam
rhoCentralFoam = [
    np.loadtxt(
        'tubePurging_rhoCentralFoam/postProcessing/volAverageFieldValues/0/volFieldValue.dat',
        skiprows = 4
    ),
    np.loadtxt(
        'tubePurging_rhoCentralFoam/postProcessing/flowRatePatch(name=inlet)/0/surfaceFieldValue.dat',
        skiprows = 4
    ),
    np.loadtxt(
        'tubePurging_rhoCentralFoam/postProcessing/flowRatePatch(name=outlet)/0/surfaceFieldValue.dat',
        skiprows = 4
    ),
    np.loadtxt(
        "tubePurging_rhoCentralFoam/postProcessing/mass/0/volFieldValue.dat",
        skiprows = 4
    )
]

#- Execution time for all solvers
ExecutionTimes = [ ]
solverColors   = [ ]
for i in range(len(solvers)):
    ExecutionTimes.append(getExecutionTime( solvers[i] ))
    solverColors.append(f"C{i}")


# Create plots
# ~~~~~~~~~~~~
#- Mean parameters
plt.figure(
    figsize = (xFigSize*2, yFigSize*2)
).suptitle(
    'Mean parameters', fontweight = 'bold', fontsize = titleFontSize
)
for i in range (0, len(fields) - 2):
    plt.subplot(221 + i).set_title(
        f'{fieldNames[i]}', fontweight = 'bold', fontsize = subplotFontSize
    )

    #- multiCompressionFoam
    if fields[i] != "e, J/kg":
        plt.plot(
            multiCompressionFoam[0][:, 0]*1e+03,
            multiCompressionFoam[0][:, i + 1],
            label = 'multiCompressionFoam',
            linewidth = linewidthHeavy
        )
        plt.ylabel( fields[i], fontsize = labelFontSize )
    else:
        for j in range(0, 2):
            if j == 0: lineType = '-'  # e
            else:      lineType = '--' # K
            plt.plot(
                multiCompressionFoam[0][:, 0]*1e+03,
                multiCompressionFoam[0][:, i + j + 1],
                label = f'multiCompressionFoam ({fields[i + j]})',
                linestyle = lineType,
                linewidth = linewidthHeavy,
                color = 'C0'
            )
        plt.ylabel( fields[i], fontsize = labelFontSize )

    #- rhoPimpleFoam
    if fields[i] != "e, J/kg":
        plt.plot(
            rhoPimpleFoam[0][:, 0]*1e+03,
            rhoPimpleFoam[0][:, i + 1],
            label = 'rhoPimpleFoam',
            linewidth = linewidthLight
        )
        plt.ylabel( fields[i], fontsize = labelFontSize )
    else:
        for j in range(0, 2):
            if j == 0: lineType = '-'  # e
            else:      lineType = '--' # K
            plt.plot(
                rhoPimpleFoam[0][:, 0]*1e+03,
                rhoPimpleFoam[0][:, i + j + 1],
                label = f'rhoPimpleFoam ({fields[i + j]})',
                linestyle = lineType,
                linewidth = linewidthLight,
                color = 'C1'
            )
        plt.ylabel( fields[i], fontsize = labelFontSize )

    #- rhoCentralFoam
    plt.plot(
        rhoCentralFoam[0][:, 0]*1e+03,
        rhoCentralFoam[0][:, i + 1],
        label = 'rhoCentralFoam',
        linewidth = linewidthLight,
        color = 'C2'
    )
    plt.ylabel( fields[i], fontsize = labelFontSize )

    plt.grid( True )
    plt.legend( loc = 'best', fontsize = legendFontSize )
    plt.xlabel( '$\\tau$, ms', fontsize = labelFontSize )
    plt.xticks( fontsize = ticksFontSize );  plt.yticks( fontsize = ticksFontSize )
plt.savefig( 'tubePurging_multiCompressionFoam/postProcessing/volFieldValues.png' )


#- Mass flow rates
plt.figure(
    figsize = (xFigSize, yFigSize)
).suptitle(
    'Mass flow rates', fontweight = 'bold', fontsize = titleFontSize
)
for i in range (0, 2):
    if i == 0:
        subplotName = 'inlet'
        flipPlot = -1 # flip plot around Y axis = 'true'
        lineType = '-'
    else:
        subplotName = 'outlet'
        flipPlot = 1 # flip plot around Y axis = 'false'
        lineType = '--'

    plt.plot(
        multiCompressionFoam[i + 1][:, 0]*1e+03,
        multiCompressionFoam[i + 1][:, 1]*flipPlot,
        label = f'multiCompressionFoam ({subplotName})',
        linestyle = lineType,
        linewidth = linewidthHeavy,
        color = 'C0'
    )
    plt.plot(
        rhoPimpleFoam[i + 1][:, 0]*1e+03,
        rhoPimpleFoam[i + 1][:, 1]*flipPlot,
        label = f'rhoPimpleFoam ({subplotName})',
        linestyle = lineType,
        linewidth = linewidthLight,
        color = 'C1'
    )
    plt.plot(
        rhoCentralFoam[i + 1][:, 0]*1e+03,
        rhoCentralFoam[i + 1][:, 1]*flipPlot,
        label = f'rhoCentralFoam ({subplotName})',
        linestyle = lineType,
        linewidth = linewidthLight,
        color = 'C2'
    )

    plt.grid( True )
    plt.legend( loc = 'best', fontsize = legendFontSize )
    plt.xlabel( '$\\tau$, ms', fontsize = labelFontSize )
    plt.ylabel( '$\\varphi$, kg/s', fontsize = labelFontSize )
    plt.xticks( fontsize = ticksFontSize );  plt.yticks(fontsize = ticksFontSize )
plt.savefig( 'tubePurging_multiCompressionFoam/postProcessing/massFlowRates.png' )


# #- Mass
# plt.figure(
#     figsize = (xFigSize, yFigSize)
# ).suptitle(
#     'Mass in the domain', fontweight = 'bold', fontsize = titleFontSize
# )
# plt.plot(
#     multiCompressionFoam[3][:, 0]*1e+03,
#     multiCompressionFoam[3][:, 1]*100,
#     label = 'multiCompressionFoam',
#     linewidth = linewidthHeavy
# )
# plt.plot(
#     rhoPimpleFoam[3][:, 0]*1e+03,
#     rhoPimpleFoam[3][:, 1]*100,
#     label = 'multiCompressionFoam',
#     linewidth = linewidthLight
# )
# plt.plot(
#     rhoCentralFoam[3][:, 0]*1e+03,
#     rhoCentralFoam[3][:, 1]*100,
#     label = 'multiCompressionFoam',
#     linewidth = linewidthLight
# )
# plt.grid( True )
# plt.legend( loc = 'best', fontsize = legendFontSize )
# plt.xlabel( '$\\tau$, ms', fontsize = labelFontSize )
# plt.ylabel( 'M, g', fontsize = labelFontSize )
# plt.xticks( fontsize = ticksFontSize );  plt.yticks( fontsize = ticksFontSize )
# plt.savefig( 'tubePurging_multiCompressionFoam/postProcessing/masses.png' )


#- Execution time bar plot
plt.figure(
    figsize = (xFigSize, yFigSize*0.65)
).suptitle(
    'Execution time by solver', fontweight = 'bold', fontsize = subplotFontSize
)
plt.bar(
    range(len(ExecutionTimes)), ExecutionTimes,
    color = solverColors,
    zorder = 3
)
plt.grid( zorder = 0 )
plt.xticks( range(len(ExecutionTimes)), solvers, fontsize = labelFontSize )
plt.yticks( fontsize = ticksFontSize )
plt.ylabel( '$\\tau$, s', fontsize = labelFontSize )
plt.savefig( 'tubePurging_multiCompressionFoam/postProcessing/executionTimes.png' )

exit( plt.show() )

# *****************************************************************************
