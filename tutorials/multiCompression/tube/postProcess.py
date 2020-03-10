#!/usr/bin/env python3
'''----------------------------------------------------------------------------
       ___       |
     _|o_ |_     |   Language: Python 3.x
    /  ___| \    |   Website: https://github.com/StasF1/dualFuelEngine
    \_| ____/    |   Copyright (C) 2019 Stanislau Stasheuski
      |__o|      |
-------------------------------------------------------------------------------

----------------------------------------------------------------------------'''

import glob
import numpy as np
import matplotlib.pyplot as plt

# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

# Get data
massFlowRate = np.loadtxt(
    glob.glob('postProcessing/flowRatePatch(name=inlet)/0/surfaceFieldValue.dat')[0],
    skiprows = 4,
    encoding = 'utf-8'
)

# Create plot
plt.subplot().set_title(
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

exit(plt.show())

# *****************************************************************************