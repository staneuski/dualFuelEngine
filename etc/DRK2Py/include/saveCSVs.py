'''----------------------------------------------------------------------------
       ___       |
     _|˚_ |_     |   Language: Python
    /  ___| \    |   Version:  3.x
    \_| ____/    |   Website:  https://github.com/StasF1/dualFuelEngine
      |__˚|      |
----------------------------------------------------------------------------'''

if not os.path.exists('DRK2Py.res'):    os.makedirs('DRK2Py.res')

#- Save Coord arrays
np.savetxt(
    "DRK2Py.res/pistonMotionUz.csv",
    np.array([
        np.arange(0, (EVO + 180)*degDeltaT, degDeltaT), # t
        pistonU
    ]).T,
    fmt='%.5e', delimiter = ',', header = "Time [s], Uz [m/s]"
) 
np.savetxt(
    "DRK2Py.res/valveMotionUz.csv",
    np.array([
        np.arange(0, (EVO + 180)*degDeltaT, degDeltaT*valveCoordFrequency), # t
        valveU
    ]).T,
    fmt='%.5e', delimiter = ',', header = "Time [s], Uz [m/s]"
)

#- Save velocity arrays
np.savetxt(
    "DRK2Py.res/massFlowRate.csv",
    np.array([
        np.arange(0, (EVO + 180)*degDeltaT, degDeltaT), # t
        G_inlet
    ]).T,
    fmt='%.5e', delimiter = ',', header = "Time [s], inlet [kg/m^3]"
)