'''----------------------------------------------------------------------------
       ___       |
     _|˚_ |_     |   Language: Python
    /  ___| \    |   Version:  3.7
    \_| ____/    |   Website:  ¯\_(ツ)_/¯
      |__˚|      |
----------------------------------------------------------------------------'''

if not os.path.exists('DRK2Py.res'):    os.makedirs('DRK2Py.res')

#- Save U arrays
np.savetxt(
    "DRK2Py.res/pistonMotion.txt",
    np.array([
        np.arange(0, (EVO + 180)*degDeltaT, degDeltaT), # t
        pistonU
    ]).T,
    fmt='%.5e', delimiter=' '
)
np.savetxt(
    "DRK2Py.res/valveMotion.txt",
    np.array([
        np.arange(0, (EVO + 180)*degDeltaT, degDeltaT*valveCoordFrequency), # t
        valveU
    ]).T,
    fmt='%.5e', delimiter=' '
)

#- Save velocity arrays
np.savetxt(
    "DRK2Py.res/inletVelocity.txt",
    np.array([
        np.arange(0, (EVO + 180)*degDeltaT, degDeltaT), # t
        G_inlet
    ]).T,
    fmt='%.5e', delimiter=' '
)
np.savetxt(
    "DRK2Py.res/injectionVelocity.txt",
    np.array([
        np.arange(0, (EVO + 180)*degDeltaT, degDeltaT), # t
        G_injection
    ]).T,
    fmt='%.5e', delimiter=' '
)