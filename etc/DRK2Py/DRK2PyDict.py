'''----------------------------------------------------------------------------
       ___       |
     _|˚_ |_     |   Language: Python
    /  ___| \    |   Version:  3.7
    \_| ____/    |   Website:  ¯\_(ツ)_/¯
      |__˚|      |
----------------------------------------------------------------------------'''

from math import pi



n                  = 92 # RPM

IPO                = 42 # ˚CA before BDC

IPC                = IPO # ˚CA after BDC

EVO                = 85 # ˚CA before BDC

EVC                = 46 # ˚CA after BDC

inletArea          = 1.092e-03 # m^2


injG_max           = 1.17 # kg/s, q_injGas = 95 (g), t_injGas = 0.0815 (s))

injCA2Max          = 10 # ˚CA

injArea            = pi*pow(0.85e-03, 2)/4*2 # m^2, area of the two injector orifices d = 0.85 (mm)


terminalOutput     = 'false' # true or false

saveFormat         = 'txt' # None, csv or txt (coordinates is writen in the .csv, velocities in the .txt)

cylParPlot         = 'false' # true or false

inOutParPlot       = 'false' # true or false

movingPartsPlot    = 'false' # true or false

inletInjectionPlot = 'true' # true or false


# *************************************************************************** #

# R = 518.3 # J/mol/K specific gas constant
