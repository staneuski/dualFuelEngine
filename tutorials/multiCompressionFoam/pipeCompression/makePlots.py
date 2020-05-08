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

# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

# Get data
# ~~~~~~~~
multiCompressionFoam = [
    np.loadtxt(
        "pipeCompression_multiCompressionFoam/postProcessing/volAverageFieldValues/0/volFieldValue.dat",
        skiprows = 4,
        encoding = 'utf-8'
    ),
    np.loadtxt(
        "pipeCompression_multiCompressionFoam/postProcessing/mass/0/volFieldValue.dat",
        skiprows = 4,
        encoding = 'utf-8'
    )
]
rhoPimpleFoam = [
    np.loadtxt(
        "pipeCompression_rhoPimpleFoam/postProcessing/volAverageFieldValues/0/volFieldValue.dat",
        skiprows = 4,
        encoding = 'utf-8'
    ),
    np.loadtxt(
        "pipeCompression_rhoPimpleFoam/postProcessing/mass/0/volFieldValue.dat",
        skiprows = 4,
        encoding = 'utf-8'
    )
]
rhoCentralFoam = [
    np.loadtxt(
        "pipeCompression_rhoCentralFoam/postProcessing/volAverageFieldValues/0/volFieldValue.dat",
        skiprows = 4,
        encoding = 'utf-8'
    ),
    np.loadtxt(
        "pipeCompression_rhoCentralFoam/postProcessing/mass/0/volFieldValue.dat",
        skiprows = 4,
        encoding = 'utf-8'
    )
]

# np.append(rhoPimpleFoam[3], rhoPimpleFoam[3][:,4] + rhoPimpleFoam[3][:,5]) # E = e + K

# Create plots
# ~~~~~~~~~~~~
# - Mean parameters
plt.figure(
    figsize = (15, 10)
).suptitle(
    'Mean parameters', fontweight = 'bold'
)

for i in range (0, len(fields) - 2):
    plt.subplot(221 + i).set_title(
        f'{fieldNames[i]}', fontweight = 'bold'
    )
    if fields[i] != "e, J/kg":
        plt.plot(
            multiCompressionFoam[0][:, 0],
            multiCompressionFoam[0][:, i + 1],
            linewidth = 2,
            label = 'multiCompressionFoam'
        )
        plt.ylabel( fields[i] )
    else:
        for j in range(0, 2):
            plt.plot(
                multiCompressionFoam[0][:, 0],
                multiCompressionFoam[0][:, i + j + 1],
                linewidth = 2,
                label = f'multiCompressionFoam ({fields[i + j]})',
            )
        plt.ylabel( fields[i] )

    if fields[i] != "e, J/kg":
        plt.plot(
            rhoPimpleFoam[0][:, 0],
            rhoPimpleFoam[0][:, i + 1],
            linewidth = 2,
            label = 'rhoPimpleFoam'
        )
        plt.ylabel( fields[i] )
    else:
        for j in range(0, 2):
            plt.plot(
                rhoPimpleFoam[0][:, 0],
                rhoPimpleFoam[0][:, i + j + 1],
                linewidth = 2,
                label = f'rhoPimpleFoam ({fields[i + j]})',
            )
        plt.ylabel( fields[i] )

    if fields[i] != "e, J/kg":
        plt.plot(
            rhoCentralFoam[0][:, 0],
            rhoCentralFoam[0][:, i + 1],
            linewidth = 2,
            label = 'rhoCentralFoam'
        )
        plt.ylabel( fields[i] )

    plt.legend( loc = 'best' )
    plt.grid( True )
    plt.xlabel( '$\\theta$, s' )

plt.savefig( 'pipeCompression_multiCompressionFoam/postProcessing/volFieldValues.png' )


#- Mass
plt.figure(
    figsize = (15, 10)
).suptitle(
    'Mass in the domain', fontweight = 'bold'
)
plt.plot(
    multiCompressionFoam[1][:, 0],
    multiCompressionFoam[1][:, 1]*100,
    linewidth = 2,
    label = 'multiCompressionFoam'
)
plt.plot(
    rhoPimpleFoam[1][:, 0],
    rhoPimpleFoam[1][:, 1]*100,
    linewidth = 2,
    label = 'rhoPimpleFoam'
)
plt.plot(
    rhoCentralFoam[1][:, 0],
    rhoCentralFoam[1][:, 1]*100,
    linewidth = 2,
    label = 'rhoCentralFoam'
)
plt.legend( loc = 'best' )
plt.grid( True )
plt.xlabel( '$\\theta$, s' )
plt.ylabel( 'M, g' )
# plt.ylim(0.0196, 0.0197)

plt.savefig( 'pipeCompression_multiCompressionFoam/postProcessing/masses.png' )

exit(plt.show())

# *****************************************************************************
