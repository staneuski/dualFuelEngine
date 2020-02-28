'''----------------------------------------------------------------------------
       ___       |
     _|˚_ |_     |   Language: Python
    /  ___| \    |   Version:  3.7
    \_| ____/    |   Website:  ¯\_(ツ)_/¯
      |__˚|      |
----------------------------------------------------------------------------'''

if not os.path.exists('DRK2Py.res'):    os.makedirs('DRK2Py.res')

#- Save Coord arrays
np.savetxt(
    "DRK2Py.res/pistonMotion.csv",
    np.array([
        np.arange(0, (EVO + 180)*degDeltaT, degDeltaT), # t
        pistonCoord
    ]).T,
    fmt='%.5e', delimiter=',', header="time [s], Z [m]", comments=""
)
np.savetxt(
    "DRK2Py.res/valveMotion.csv",
    np.array([
        np.arange(0, (EVO + 180)*degDeltaT, degDeltaT*valveCoordFrequency), # t
        valveCoord
    ]).T,
    fmt='%.5e', delimiter=',', header="time [s], Z [m]", comments=""
)

#- Save velocity arrays
np.savetxt(
    "DRK2Py.res/inletVelocity.csv",
    np.array([
        np.arange(0, (EVO + 180)*degDeltaT, degDeltaT), # t
        G_inlet
    ]).T,
    fmt='%.5e', delimiter=',', header="time [s], U [m/s]", comments=""
)
np.savetxt(
    "DRK2Py.res/injectionVelocity.csv",
    np.array([
        np.arange(0, (EVO + 180)*degDeltaT, degDeltaT), # t
        G_injection
    ]).T,
    fmt='%.5e', delimiter=',', header="time [s], U [m/s]", comments=""
)