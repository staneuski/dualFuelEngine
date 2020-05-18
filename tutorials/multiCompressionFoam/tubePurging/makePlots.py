#!/usr/bin/env python3
'''----------------------------------------------------------------------------
       ___       |
     _|o_ |_     |   Language: Python 3.x
    /  ___| \    |   Website: https://github.com/StasF1/dualFuelEngine
    \_| ____/    |   Copyright (C) 2018-2020 Stanislau Stasheuski
      |__o|      |
----------------------------------------------------------------------------'''

import glob
import numpy as np
import matplotlib.pyplot as plt

# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

fieldNames = [
    "Pressure",
    "Temperature",
    "Density",
    "Energy"
]

fields = ["p, Pa", "T, K", "$\\rho, kg/m^3$", "e, J/kg", "K, J/kg", "E, J/kg"]


# Get data
# ~~~~~~~~
#- multiCompressionFoam
multiCompressionFoam = [
    np.loadtxt(
        'tubePurging_multiCompressionFoam/postProcessing/volAverageFieldValues/0/volFieldValue.dat',
        skiprows = 4,
        encoding = 'utf-8'
    ),
    np.loadtxt(
        'tubePurging_multiCompressionFoam/postProcessing/flowRatePatch(name=inlet)/0/surfaceFieldValue.dat',
        skiprows = 4,
        encoding = 'utf-8'
    ),
    np.loadtxt(
        'tubePurging_multiCompressionFoam/postProcessing/flowRatePatch(name=outlet)/0/surfaceFieldValue.dat',
        skiprows = 4,
        encoding = 'utf-8'
    ),
    np.loadtxt(
        "tubePurging_multiCompressionFoam/postProcessing/mass/0/volFieldValue.dat",
        skiprows = 4,
        encoding = 'utf-8'
    )
]

#- rhoPimpleFoam
rhoPimpleFoam = [
    np.loadtxt(
        'tubePurging_rhoPimpleFoam/postProcessing/volAverageFieldValues/0/volFieldValue.dat',
        skiprows = 4,
        encoding = 'utf-8'
    ),
    np.loadtxt(
        'tubePurging_rhoPimpleFoam/postProcessing/flowRatePatch(name=inlet)/0/surfaceFieldValue.dat',
        skiprows = 4,
        encoding = 'utf-8'
    ),
    np.loadtxt(
        'tubePurging_rhoPimpleFoam/postProcessing/flowRatePatch(name=outlet)/0/surfaceFieldValue.dat',
        skiprows = 4,
        encoding = 'utf-8'
    ),
    np.loadtxt(
        "tubePurging_rhoPimpleFoam/postProcessing/mass/0/volFieldValue.dat",
        skiprows = 4,
        encoding = 'utf-8'
    )
]

#- rhoCentralFoam
rhoCentralFoam = [
    np.loadtxt(
        'tubePurging_rhoCentralFoam/postProcessing/volAverageFieldValues/0/volFieldValue.dat',
        skiprows = 4,
        encoding = 'utf-8'
    ),
    np.loadtxt(
        'tubePurging_rhoCentralFoam/postProcessing/flowRatePatch(name=inlet)/0/surfaceFieldValue.dat',
        skiprows = 4,
        encoding = 'utf-8'
    ),
    np.loadtxt(
        'tubePurging_rhoCentralFoam/postProcessing/flowRatePatch(name=outlet)/0/surfaceFieldValue.dat',
        skiprows = 4,
        encoding = 'utf-8'
    ),
    np.loadtxt(
        "tubePurging_rhoCentralFoam/postProcessing/mass/0/volFieldValue.dat",
        skiprows = 4,
        encoding = 'utf-8'
    )
]


# Create plots
# ~~~~~~~~~~~~
#- Mean parameters
plt.figure(
    figsize = (15, 10)
).suptitle(
    'Mean parameters through time', fontweight = 'bold'
)
for i in range (0, len(fields) - 2):
    plt.subplot(221 + i).set_title(
        f'{fieldNames[i]}', fontweight = 'bold'
    )

    #- multiCompressionFoam
    if fields[i] != "e, J/kg":
        plt.plot(
            multiCompressionFoam[0][:, 0]*1e+03,
            multiCompressionFoam[0][:, i + 1],
            label = 'multiCompressionFoam',
            linewidth = 2
        )
        plt.ylabel( fields[i] )
    else:
        for j in range(0, 2):
            if j == 0: lineType = '-'  # e
            else:      lineType = '--' # K
            plt.plot(
                multiCompressionFoam[0][:, 0]*1e+03,
                multiCompressionFoam[0][:, i + j + 1],
                label = f'multiCompressionFoam ({fields[i + j]})',
                linestyle = lineType,
                color = 'C0',
                linewidth = 2
            )
        plt.ylabel( fields[i] )

    #- rhoPimpleFoam
    if fields[i] != "e, J/kg":
        plt.plot(
            rhoPimpleFoam[0][:, 0]*1e+03,
            rhoPimpleFoam[0][:, i + 1],
            label = 'rhoPimpleFoam',
            linewidth = 2
        )
        plt.ylabel( fields[i] )
    else:
        for j in range(0, 2):
            if j == 0: lineType = '-'  # e
            else:      lineType = '--' # K
            plt.plot(
                rhoPimpleFoam[0][:, 0]*1e+03,
                rhoPimpleFoam[0][:, i + j + 1],
                label = f'rhoPimpleFoam ({fields[i + j]})',
                linestyle = lineType,
                color = 'C1',
                linewidth = 2
            )
        plt.ylabel( fields[i] )

    #- rhoCentralFoam
    plt.plot(
        rhoCentralFoam[0][:, 0]*1e+03,
        rhoCentralFoam[0][:, i + 1],
        label = 'rhoCentralFoam',
        color = 'C2',
        linewidth = 2
    )
    plt.ylabel( fields[i] )

    plt.grid( True )
    plt.legend( loc = 'best' )
    plt.xlabel( '$\\tau$, ms' )
plt.savefig( 'tubePurging_multiCompressionFoam/postProcessing/volFieldValues.png' )

#- Inlet patch mass flow rate
plt.figure(
    figsize = (15, 10)
).suptitle(
    'Mass flow rates', fontweight = 'bold'
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
        color = 'C0',
        linewidth = 2
    )
    plt.plot(
        rhoPimpleFoam[i + 1][:, 0]*1e+03,
        rhoPimpleFoam[i + 1][:, 1]*flipPlot,
        label = f'rhoPimpleFoam ({subplotName})',
        linestyle = lineType,
        color = 'C1',
        linewidth = 2
    )
    plt.plot(
        rhoCentralFoam[i + 1][:, 0]*1e+03,
        rhoCentralFoam[i + 1][:, 1]*flipPlot,
        label = f'rhoCentralFoam ({subplotName})',
        linestyle = lineType,
        color = 'C2',
        linewidth = 2
    )

    plt.grid( True )
    plt.legend( loc = 'best' )
    plt.xlabel( '$\\tau$, ms' )
    plt.ylabel( '$\\varphi$, kg/s' )
plt.savefig( 'tubePurging_multiCompressionFoam/postProcessing/massFlowRates.png' )

# #- Mass
# plt.figure(
#     figsize = (15, 10)
# ).suptitle(
#     'Mass in the domain', fontweight = 'bold'
# )
# plt.plot(
#     multiCompressionFoam[3][:, 0]*1e+03,
#     multiCompressionFoam[3][:, 1]*100,
#     label = 'multiCompressionFoam',
#     linewidth = 2
# )
# plt.plot(
#     rhoPimpleFoam[3][:, 0]*1e+03,
#     rhoPimpleFoam[3][:, 1]*100,
#     label = 'multiCompressionFoam',
#     linewidth = 2
# )
# plt.plot(
#     rhoCentralFoam[3][:, 0]*1e+03,
#     rhoCentralFoam[3][:, 1]*100,
#     label = 'multiCompressionFoam',
#     linewidth = 2
# )
# plt.legend( loc = 'best' )
# plt.grid( True )
# plt.xlabel( '$\\tau$, ms' )
# plt.ylabel( 'M, g' )
# plt.savefig( 'tubePurging_multiCompressionFoam/postProcessing/masses.png' )

exit(plt.show())

# *****************************************************************************
