#!/usr/bin/env python3
'''----------------------------------------------------------------------------
       ___       |
     _|o_ |_     |   Language: Python 3.x
    /  ___| \    |   Website: https://github.com/StasF1/dualFuelEngine
    \_| ____/    |   Copyright (C) 2020 Stanislau Stasheuski
      |__o|      |
----------------------------------------------------------------------------'''

import re
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

solvers = ["multiCompressionFoam", "rhoPimpleFoam", "rhoCentralFoam"]

# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

def getExecutionTime(solver):
    ''' Get execution time from the log '''

    for grep in open(f"shockTube_{solver}/log.{solver}"):
        if "ExecutionTime" in grep:
            ExecutionTime = re.findall('(\d+.\d+)', grep)
    print(f"{solver} execution time: {ExecutionTime[0]} s")

    return float(ExecutionTime[0])


# Get data
# ~~~~~~~~
ExecutionTimes = [ ]
solverColors   = [ ]
for i in range(len(solvers)):
    ExecutionTimes.append(getExecutionTime(solvers[i]))
    solverColors.append(f"C{i}")


# Create plot
# ~~~~~~~~~~~
plt.figure(figsize = (xFigSize, yFigSize*0.75))
plt.title('Execution time by solver',
          fontweight = 'bold', fontsize = subplotFontSize)

plt.bar(range(len(ExecutionTimes)), ExecutionTimes,
        color = solverColors, zorder = 3)

plt.grid(zorder = 0)
plt.xticks(range(len(ExecutionTimes)), solvers, fontsize = labelFontSize)
plt.yticks(fontsize = ticksFontSize)
plt.ylabel('$\\tau$, s', fontsize = labelFontSize)
plt.savefig('shockTube_multiCompressionFoam/executionTimes.png')

exit(plt.show())

# *****************************************************************************