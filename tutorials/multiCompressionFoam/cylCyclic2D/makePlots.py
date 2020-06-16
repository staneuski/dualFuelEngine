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
linewidthLight = 1.5

#- Engine parameters
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

def enginePlot( labelFontSize, legendFontSize, ticksFontSize, EVO, IPO ):
    ''' Stardart for all engine plots parameters and annotations '''

    plt.annotate(
    '(BDC)', (1, 1),
    xytext = (EVO/(EVO + 180)*1.18, -0.04), textcoords = 'axes fraction',
    horizontalalignment = 'right', verticalalignment = 'top'
    )
    plt.annotate(
        '(TDC)', (1, 1),
        xytext = (1, -0.04), textcoords = 'axes fraction',
        horizontalalignment = 'right', verticalalignment = 'top'
    )
    plt.axvline( x = -180, color = 'black', linestyle = '--', linewidth = 1 )
    plt.axvline( x = 0, color = 'black', linestyle = '--', linewidth = 1 )
    plt.axvspan( -IPO - 180, IPO - 180, alpha = 0.18, color = 'grey' )
    plt.grid( True )
    plt.legend( loc = 'best', fontsize = legendFontSize )
    plt.xlabel( '$\\theta$, CA˚', fontsize = labelFontSize )
    plt.xticks( fontsize = ticksFontSize );  plt.yticks( fontsize = ticksFontSize )


# Get data
# ~~~~~~~~
rhoPimpleFoam = [
    np.loadtxt(
        "cylCyclic2D_rhoPimpleFoam/postProcessing/volAverageFieldValues/0/volFieldValue.dat",
        skiprows = 4
    ),
    np.loadtxt(
        "cylCyclic2D_rhoPimpleFoam/postProcessing/flowRatePatch(name=inlet)/0/surfaceFieldValue.dat",
        skiprows = 4
    ),
    np.loadtxt(
        "cylCyclic2D_rhoPimpleFoam/postProcessing/flowRatePatch(name=injection)/0/surfaceFieldValue.dat",
        skiprows = 4
    ),
    np.loadtxt(
        "cylCyclic2D_rhoPimpleFoam/postProcessing/flowRatePatch(name=outlet)/0/surfaceFieldValue.dat",
        skiprows = 4
    )
]
# np.append(rhoPimpleFoam[3], rhoPimpleFoam[3][:,4] + rhoPimpleFoam[3][:,5]) # E = e + K


# Create plots
# ~~~~~~~~~~~~
#- Mean parameters
plt.figure(
        figsize = (xFigSize*2, yFigSize*2)
).suptitle(
    'Mean parameters through time', fontweight = 'bold', fontsize = titleFontSize
)

for i in range (0, len(fields) - 2):
    plt.subplot(221 + i).set_title(
        f'{fieldNames[i]}', fontweight = 'bold', fontsize = subplotFontSize
    )

    #- rhoPimpleFoam
    if fields[i] != "e, J/kg":
        plt.plot(
            rhoPimpleFoam[0][:, 0]*6*rpm - 180 - EVO,
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
                rhoPimpleFoam[0][:, 0]*6*rpm - 180 - EVO,
                rhoPimpleFoam[0][:, i + j + 1],
                label = f'rhoPimpleFoam ({fields[i + j]})',
                linestyle = lineType,
                linewidth = linewidthLight,
                color = 'C1'
            )
        plt.ylabel( fields[i], fontsize = labelFontSize )

    enginePlot( labelFontSize, legendFontSize, ticksFontSize, EVO, IPO )
plt.savefig( 'cylCyclic2D_rhoPimpleFoam/postProcessing/volFieldValues.png' )

#- Mass flow rates
plt.figure(
    figsize = (xFigSize, yFigSize)
).suptitle(
    'Mass flow rates', fontweight = 'bold', fontsize = titleFontSize
)

#- rhoPimpleFoam
plt.plot(
    rhoPimpleFoam[1][:,0]*6*rpm - 180 - EVO,
  - rhoPimpleFoam[1][:,1],
    label = 'rhoPimpleFoam (inlet)',
    linewidth = linewidthLight,
    linestyle = '--',
    color = 'C1'
)
plt.plot(
    rhoPimpleFoam[2][:,0]*6*rpm - 180 - EVO,
  - rhoPimpleFoam[2][:,1],
    label = 'rhoPimpleFoam (injection)',
    linewidth = linewidthLight,
    linestyle = ':',
    color = 'C1'
)
plt.plot(
    rhoPimpleFoam[3][:,0]*6*rpm - 180 - EVO,
    rhoPimpleFoam[3][:,1],
    label = 'rhoPimpleFoam (outlet)',
    linewidth = linewidthLight,
    color = 'C1'
)

plt.ylabel( '$\\varphi$, kg/s', fontsize = labelFontSize )
enginePlot( labelFontSize, legendFontSize, ticksFontSize, EVO, IPO )

exit(plt.show())


# *****************************************************************************
