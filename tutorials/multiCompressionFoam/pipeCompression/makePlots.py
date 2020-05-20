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
linewidthLight = 1

#- Adiabatic compression paarmeters
frequency     = 1 # [s]

amplitude     = 2 # [m/s]

start         = 0.15 # [s]

area          = 1e-4 # [m^2]

Cp            = 1005 # [J/kg/K]

Cv            = Cp - 287 # [J/kg/K]

l             = 0.6 # [m]


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
#- multiCompressionFoam
multiCompressionFoam = [
    np.loadtxt(
        "pipeCompression_multiCompressionFoam/postProcessing/volAverageFieldValues/0/volFieldValue.dat",
        skiprows = 4
    ),
    np.loadtxt(
        "pipeCompression_multiCompressionFoam/postProcessing/mass/0/volFieldValue.dat",
        skiprows = 4
    )
]

#- rhoPimpleFoam
rhoPimpleFoam = [
    np.loadtxt(
        "pipeCompression_rhoPimpleFoam/postProcessing/volAverageFieldValues/0/volFieldValue.dat",
        skiprows = 4
    ),
    np.loadtxt(
        "pipeCompression_rhoPimpleFoam/postProcessing/mass/0/volFieldValue.dat",
        skiprows = 4
    )
]
# np.append(rhoPimpleFoam[3], rhoPimpleFoam[3][:,4] + rhoPimpleFoam[3][:,5]) # E = e + K

#- rhoPimpleFoam
rhoCentralFoam = [
    np.loadtxt(
        "pipeCompression_rhoCentralFoam/postProcessing/volAverageFieldValues/0/volFieldValue.dat",
        skiprows = 4
    ),
    np.loadtxt(
        "pipeCompression_rhoCentralFoam/postProcessing/mass/0/volFieldValue.dat",
        skiprows = 4
    )
]

#- Adiabatic compression
t = multiCompressionFoam[0][:, 0] # t
motionX =(
  - amplitude/2/np.pi/frequency*np.cos(
        2*np.pi*frequency*(t - start)
    )
)
v = (l - (motionX - motionX[0]))*area
print(f'Compression ratio: {round(max(v)/min(v), 2)}')

p   = multiCompressionFoam[0][0, 1]*pow(v[0]/v, Cp/Cv)     # p_IC*(V_IC/V)^(Cp/Cv)
T   = multiCompressionFoam[0][0, 2]*pow(v[0]/v, Cp/Cv - 1) # T_IC*(V_IC/V)^(Cp/Cv - 1)
rho = multiCompressionFoam[0][0, 3]*v[0]/v                 # rho_IC*(V_IC/V)
e   = multiCompressionFoam[0][0, 4]*pow(v[0]/v, Cp/Cv - 1) # e_IC*(V_IC/V)^(Cp/Cv - 1)

adiabaticProcess = [
    t, p, T, rho, e
]


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

    # - multiCompressionFoam
    if fields[i] != "e, J/kg":
        plt.plot(
            multiCompressionFoam[0][:, 0],
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
                multiCompressionFoam[0][:, 0],
                multiCompressionFoam[0][:, i + j + 1],
                label = f'multiCompressionFoam ({fields[i + j]})',
                linestyle = lineType,
                linewidth = linewidthLight,
                color = 'C0'
            )
        plt.ylabel( fields[i], fontsize = labelFontSize )

    #- rhoPimpleFoam
    if fields[i] != "e, J/kg":
        plt.plot(
            rhoPimpleFoam[0][:, 0],
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
                rhoPimpleFoam[0][:, 0],
                rhoPimpleFoam[0][:, i + j + 1],
                label = f'rhoPimpleFoam ({fields[i + j]})',
                linestyle = lineType,
                linewidth = linewidthLight,
                color = 'C1'
            )
        plt.ylabel( fields[i], fontsize = labelFontSize )

    #- rhoCentralFoam
    plt.plot(
        rhoCentralFoam[0][:, 0],
        rhoCentralFoam[0][:, i + 1],
        label = 'rhoCentralFoam',
        linewidth = linewidthLight,
        color = 'C2'
    )
    plt.ylabel( fields[i], fontsize = labelFontSize )

    #- Adiabatic compression
    plt.plot(
        adiabaticProcess[0],
        adiabaticProcess[i + 1],
        label = 'adiabatic compression',
        linewidth = linewidthLight,
        color = 'C3'
    )
    plt.ylabel( fields[i], fontsize = labelFontSize )

    plt.grid( True )
    plt.legend( loc = 'best', fontsize = legendFontSize )
    plt.xlabel( '$\\tau$, s', fontsize = labelFontSize )
plt.savefig( 'pipeCompression_multiCompressionFoam/postProcessing/volFieldValues.png' )


#- Mass
plt.figure(
    figsize = (xFigSize, yFigSize)
).suptitle(
    'Mass in the domain', fontweight = 'bold',  fontsize = titleFontSize
)
plt.plot(
    multiCompressionFoam[1][:, 0],
    multiCompressionFoam[1][:, 1]*100,
    label = 'multiCompressionFoam',
    linewidth = linewidthHeavy
)
plt.plot(
    rhoPimpleFoam[1][:, 0],
    rhoPimpleFoam[1][:, 1]*100,
    label = 'rhoPimpleFoam',
    linewidth = linewidthLight
)
plt.plot(
    rhoCentralFoam[1][:, 0],
    rhoCentralFoam[1][:, 1]*100,
    label = 'rhoCentralFoam',
    linewidth = linewidthLight
)
# plt.ylim(0.0196, 0.0197)
plt.grid( True )
plt.legend( loc = 'best', fontsize = legendFontSize )
plt.xlabel( '$\\tau$, s', fontsize = labelFontSize )
plt.ylabel( 'M, g', fontsize = labelFontSize )
plt.xticks( fontsize = ticksFontSize );  plt.yticks( fontsize = ticksFontSize )
plt.savefig( 'pipeCompression_multiCompressionFoam/postProcessing/masses.png' )

exit(plt.show())

# *****************************************************************************
