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
    "Internal energy",
    "Density",
    "Air concentration",
    "Natural gas concentration",
    "Exhaust gas concentration"
]

fields = ["p, Pa", "T, K", "e, J/kg", "rho", "alphaAir", "alphaGas", "alphaExh"]


# Get data
# ~~~~~~~~
massFlowRate = np.loadtxt(
    'postProcessing/flowRatePatch(name=inlet)/0/surfaceFieldValue.dat',
    skiprows = 4,
    encoding = 'utf-8'
)

volFieldValues = np.loadtxt(
    'postProcessing/volFieldValue/0/volFieldValue.dat',
    skiprows = 4,
    encoding = 'utf-8'
)


# Create plots
# ~~~~~~~~~~~~
#- Inlet patch mass flow rate
plt.figure().suptitle(
    'Inlet patch mass flow rate', fontweight = 'bold'
)
plt.plot(
    massFlowRate[:,0]*1e+03,
    -massFlowRate[:,1],
    linewidth = 2,
    label = 'inlet'
)
plt.grid( True )
plt.xlabel( '$\\tau$, ms' )
plt.ylabel( '$\\varphi$, kg/s' )
plt.savefig( 'postProcessing/massFlowRate.png' )

#- Mean parameters
plt.figure(
    figsize = (15, 10)
).suptitle(
    'Mean parameters through time', fontweight = 'bold'
)

for i in range (0, len(fields) - 3):
    plt.subplot(221 + i).set_title(
        f'{fieldNames[i]}', fontweight = 'bold'
    )
    plt.plot(
        volFieldValues[:, 0],
        volFieldValues[:, i + 1],
        linewidth = 2,
        label = fields[i]
    )
    plt.grid( True )
    plt.xlabel( '$\\tau$, ms' )
    plt.ylabel( fields[i] )

    if fields[i] == "rho":
        for j in range (1, 4):
            plt.plot(
                volFieldValues[:, 0],
                volFieldValues[:, i + 1 + j],
                linewidth = 2,
                label = fields[i + j]
            )
        plt.legend( loc = 'best' )

plt.savefig( 'postProcessing/volFieldValues.png' )


exit(plt.show())

# *****************************************************************************
