#!/usr/bin/env python3
'''----------------------------------------------------------------------------
       ___       |
     _|˚_ |_     |   Language: Python
    /  ___| \    |   Version:  3.7
    \_| ____/    |   Website:  ¯\_(ツ)_/¯
      |__˚|      |
-------------------------------------------------------------------------------

File
    DRK2Python.py

Description
    Converter data from Diesel-RK to Python 3

----------------------------------------------------------------------------'''

import glob, os
import numpy as np
import matplotlib.pyplot as plt

from scipy import interpolate

from DRK2PyDict import *

# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

# Cylinder parameters
# ~~~~~~~~~~~~~~~~~~~
indMatrix = np.loadtxt(
    glob.glob('tmp*/*.ind')[0], skiprows = 19, encoding = "utf8"
)

alpha         = indMatrix[:,0]       # CA
p             = indMatrix[:,1]*1e+05 # Pa, cylinder pressure
T             = indMatrix[:,2]       # K, average cylinder temperature
V             = indMatrix[:,3]       # m^3, cylinder volume
alpha_w       = indMatrix[:,4]*1e+05 # Pa, heat transfer factor in cylinder (Woschni)
p_1ring       = indMatrix[:,5]       # W/m^2/K, pressure after first piston ring
G_bb          = indMatrix[:,6]       # kg/s, mass gas flow blowed-by through 1 piston ring
pistonFromBDC = indMatrix[:,7]*1e-03 # m, piston position from BDC
x             = indMatrix[:,8]       # heat release fraction


# Gas exchange parameters
# ~~~~~~~~~~~~~~~~~~~~~~~
gasMatrix = np.loadtxt(
    glob.glob('tmp*/*.gas')[0], skiprows = 31
)

p_exhPipe     = gasMatrix[:,5] *1e+05 # Pa, exhaust pipe pressure
T_exhPipe     = gasMatrix[:,6]        # T, exhaust pipe temperature
p_IP          = gasMatrix[:,12]*1e+05 # Pa, inlet port pressure
T_IP          = gasMatrix[:,13]       # T, inlet port temperature
G_inlet       = gasMatrix[:,14]       # kg/s, inlet mass flow rate
Lv_exh        = gasMatrix[:,19]*1e-03 # m, valve position BDC

# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

degDeltaT = 60/n/360

#- Create arrays of the moving parts
pistonCoord = np.roll(pistonFromBDC, EVO)[0:180 + EVO]
pistonCoord = pistonCoord - pistonCoord[0]
pistonU     = np.gradient(pistonCoord, np.arange(0, (EVO + 180)*degDeltaT, degDeltaT)) # dt/dt

valveCoordFrequency = 3

valveCoordObj = interpolate.CubicSpline(
    np.arange(0, (EVO + 180)*degDeltaT, degDeltaT), # t
  - np.pad(Lv_exh, (0, len(pistonCoord) - len(Lv_exh)), 'constant') # valveCoord
)
valveCoord = valveCoordObj(np.arange(0, (EVO + 180)*degDeltaT, degDeltaT*valveCoordFrequency))

valveU = np.gradient(valveCoord, np.arange(0, (EVO + 180)*degDeltaT, degDeltaT*valveCoordFrequency)) # dt/dt

#- Create inlet/injection arrays
G_injection = np.concatenate((
    np.zeros(EVO + EVC - 1),
    np.arange(0, injG_max + injG_max/injCA2Max, injG_max/injCA2Max),
    np.full(180 - (EVC + injCA2Max), injG_max)
))
rhoU_injection = G_injection/injArea

G_inlet = np.pad(
    G_inlet, (0, len(G_injection) - len(G_inlet)), 'constant'
)

# -1.7 is more than right min, set less grad(G) to the left min
# G_inlet[G_inlet < -1.7] = -1

rhoU_inlet = G_inlet/inletArea

# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

# Save files
if saveFormat == 'csv':
    exec( open(
        "etc/./saveCSVs.py"
    ).read() )

elif saveFormat == 'txt':
    exec( open(
        "etc/./saveTXTs.py"
    ).read() )

elif saveFormat == 'None':
    None

else:
    exit("Error: varible 'saveFormat' is incorrect!")

# Create plots
exec( open(
    "etc/./createPlots.py"
).read() )

# Get the results
exec( open(
    "etc/./reportGenerator.py"
).read() )

if (cylParPlot or inOutParPlot or movingPartsPlot or inletInjectionPlot == 'true'):
    exit( plt.show() )

# -----------------------------------------------------------------------------
