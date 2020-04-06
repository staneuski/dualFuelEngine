'''----------------------------------------------------------------------------
       ___       |
     _|˚_ |_     |   Language: Python
    /  ___| \    |   Version:  3.x
    \_| ____/    |   Website:  https://github.com/StasF1/dualFuelEngine
      |__˚|      |
----------------------------------------------------------------------------'''

from math import pi

# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

# Download MAN_BnW.drkres.zip file from the source code of the 0.5-alpha
# version and extract it at etc/DRK2Py/ as MAN_BnW-DieselRK.fvres/ folder
tmpFolder          = 'MAN_BnW-DieselRK.res/tmp2020-02*' # path to Diesel-RK results folder

terminalOutput     = 'true' # 'true' \ 'false', output log in the Terminal window

cylParPlot         = 'false' # 'true' \ 'false', integral cylinder parameters plot

inOutParPlot       = 'false' # 'true' \ 'false', integral manifolds parameters plot

inletInjectionPlot = 'false' # 'true' \ 'false', inlet & injection mass flow rate

massFlowRatePar    = 'rhoU' # 'rhoU' \ 'G', mass flow rate to plot (relative or not)

# Moving parts coordinates are writen in the .csv, velocities in the .txt
saveFormat         = 'txt' # 'None' \ 'csv' \ 'txt'

movingPartsPlot    = 'false' # 'true' \ 'false', moving parts (valve, piston) scheme

# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

n           = 92 # RPM

S           = 2.7 # m


IPO         = 42 # ˚CA before BDC

IPC         = IPO # ˚CA after BDC

EVO         = 85 # ˚CA before BDC

EVC         = 46 # ˚CA after BDC

inletArea   = 1092*191*1e-6 # m^2


injG_max    = 0.0983/0.0815/20 # kg/s, q_injGas/t_injGas

injCA2Max   = 10 # ˚CA

injDuration = 80 - 2*injCA2Max # ˚CA

injArea     = pi*pow(3.75e-03, 2)/4*2 # m^2, area which equals of the two injector orifices d = 3.75 (mm)

injT        = 380 # K (estimated)

injR        = 518.3 # J/mol/K specific gas constant


# *****************************************************************************
