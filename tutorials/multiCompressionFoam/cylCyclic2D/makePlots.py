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

rpm = 92 # [1/min]

EVO = 85 # CA˚ before TDC [CAD]

IPO = 42 # CA˚ before BDC [CAD]

IPC = IPO # CA˚ after BDC [CAD]

fieldNames = [
    "Pressure",
    "Temperature",
    "Density",
    "Energy"
]

fields = ["p, Pa", "T, K", "rho, kg/m^3", "e, J/kg", "K, J/kg", "E, J/kg"]

# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

# Get data
# ~~~~~~~~
rhoPimpleFoam = [
        np.loadtxt(
        "cylCyclic2D_rhoPimpleFoam/postProcessing/flowRatePatch(name=inlet)/0/surfaceFieldValue.dat",
        skiprows = 4,
        encoding = 'utf-8'
    ),
    np.loadtxt(
        "cylCyclic2D_rhoPimpleFoam/postProcessing/flowRatePatch(name=injection)/0/surfaceFieldValue.dat",
        skiprows = 4,
        encoding = 'utf-8'
    ),
    np.loadtxt(
        "cylCyclic2D_rhoPimpleFoam/postProcessing/volAverageFieldValues/0/volFieldValue.dat",
        skiprows = 4,
        encoding = 'utf-8'
    )
]

# np.append(rhoPimpleFoam[2], rhoPimpleFoam[2][:,4] + rhoPimpleFoam[2][:,5]) # E = e + K

# Create plots
# ~~~~~~~~~~~~
#- Mass flow rates
plt.figure(
    figsize = (15, 10)
).suptitle(
    'Mass flow rates', fontweight = 'bold'
)

# rhoPimpleFoam
plt.plot(
    rhoPimpleFoam[1][:,0]*6*rpm - 180 - EVO,
  - rhoPimpleFoam[0][:,1],
    linewidth = 2,
    label = 'rhoPimpleFoam (inlet)'
)
plt.plot(
    rhoPimpleFoam[1][:,0]*6*rpm - 180 - EVO,
  - rhoPimpleFoam[1][:,1],
    linewidth = 2,
    label = 'rhoPimpleFoam (injection)',
    color = 'C0',
    linestyle = '--'
)
plt.axvline(x = -180, color = 'black', linestyle = '--', linewidth = 1)
plt.axvline(x = 0, color = 'black', linestyle = '--', linewidth = 1)
plt.annotate(
    '(BDC)', (1, 1),
    xytext = (EVO/(EVO + 180)*1.11, -0.026), textcoords = 'axes fraction',
    horizontalalignment = 'right', verticalalignment = 'top'
)
plt.annotate(
    '(TDC)', (1, 1),
    xytext = (0.975, -0.026), textcoords = 'axes fraction',
    horizontalalignment = 'right', verticalalignment = 'top'
)
plt.axvspan(-IPO - 180, IPO - 180, alpha = 0.18, color = 'grey')
plt.legend( loc = 'best' )
plt.grid( True )
plt.xlabel( '$\\theta$, CA˚' )
plt.ylabel( '$\\varphi$, kg/s' )

plt.savefig( 'cylCyclic2D_rhoPimpleFoam/postProcessing/massFlowRate.png' )

# - Mean parameters
plt.figure(
    figsize = (15, 10)
).suptitle(
    'Mean parameters through time', fontweight = 'bold'
)

for i in range (0, len(fields) - 2):
    plt.subplot(221 + i).set_title(
        f'{fieldNames[i]}', fontweight = 'bold'
    )
    if fields[i] != "e, J/kg":
        plt.plot(
            # np.flip( - rhoPimpleFoam[2][:, 0]*6*rpm),
            rhoPimpleFoam[2][:, 0]*6*rpm - 180 - EVO,
            rhoPimpleFoam[2][:, i + 1],
            linewidth = 2,
            label = 'rhoPimpleFoam'
        )
        plt.ylabel( fields[i] )
    else:
        for j in range(0, 2):
            plt.plot(
                rhoPimpleFoam[2][:, 0]*6*rpm - 180 - EVO,
                rhoPimpleFoam[2][:, i + j + 1],
                linewidth = 2,
                label = f'rhoPimpleFoam ({fields[i + j]})'
            )
        plt.ylabel( fields[i] )

    plt.axvline(x = -180, color = 'black', linestyle = '--', linewidth = 1)
    plt.axvline(x = 0, color = 'black', linestyle = '--', linewidth = 1)
    plt.annotate(
        '(BDC)', (1, 1),
        xytext = (EVO/(EVO + 180)*1.18, -0.06), textcoords = 'axes fraction',
        horizontalalignment = 'right', verticalalignment = 'top'
    )
    plt.annotate(
        '(TDC)', (1, 1),
        xytext = (1, -0.06), textcoords = 'axes fraction',
        horizontalalignment = 'right', verticalalignment = 'top'
    )
    plt.axvspan(-IPO - 180, IPO - 180, alpha = 0.18, color = 'grey')
    plt.legend( loc = 'best' )
    plt.grid( True )
    plt.xlabel( '$\\theta$, CA˚' )

plt.savefig( 'cylCyclic2D_rhoPimpleFoam/postProcessing/volFieldValues.png' )

exit(plt.show())

# *****************************************************************************
