'''----------------------------------------------------------------------------
       ___       |
     _|˚_ |_     |   Language: Python
    /  ___| \    |   Version:  3.7
    \_| ____/    |   Website:  ¯\_(ツ)_/¯
      |__˚|      |
----------------------------------------------------------------------------'''

# Paramaters in the cylinder
# ~~~~~~~~~~~~~~~~~~~~~~~~~~
if cylParPlot == 'true':
    plt.figure(
        figsize = (10, 6)#, dpi = 80, facecolor = 'w', edgecolor = 'k'
    ).suptitle(
        'Paramaters in the cylinder', fontweight='bold', fontsize = 14
    )

    plt.subplot(121).set_title(
        f'Pressure', fontweight = 'bold', fontsize = 12
    )
    plt.plot(
        p,
        linewidth = 2,
        label = 'p'
    )
    plt.scatter(360 - EVO, p[360 - EVO], s = 100, marker = 'o')
    plt.grid( True );    plt.legend( loc = 'best', fontsize = 12 )
    plt.xlabel( '$\\varphi$, deg' )
    plt.ylabel( 'p, Pa' )

    plt.subplot(122).set_title(
        f'Temperature', fontweight = 'bold', fontsize = 12
    )
    plt.plot(
        T,
        linewidth = 2,
        label = 'T'
    )
    plt.scatter(360 - EVO, T[360 - EVO], s = 100, marker = 'o')
    plt.grid( True );    plt.legend( loc = 'best', fontsize = 12 )
    plt.xlabel( '$\\varphi$, deg' )
    plt.ylabel( 'T, K' )

    plt.savefig( 'DRK2Py.res/cylPars.png' )


# Inlet & outlet parameters
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if inOutParPlot == 'true':
    plt.figure(
        figsize = (10, 6)#, dpi = 80, facecolor = 'w', edgecolor = 'k'
    ).suptitle(
        'Paramaters in the inlet & outlet ports', fontweight='bold', fontsize = 14
    )

    plt.subplot(121).set_title(
        'Inlet port & exhaust pipe pressures', fontweight = 'bold', fontsize = 12
    )
    plt.plot(
        p_IP,
        linewidth = 2,
        label = 'inlet port'
    )
    plt.plot(
        p_exhPipe,
        linewidth = 2,
        label = 'exhaust pipe'
    )
    plt.grid( True );    plt.legend( loc = 'best', fontsize = 12 )
    plt.xlabel( '$\\varphi$, deg' )
    plt.ylabel( 'p, Pa' )

    plt.subplot(122).set_title(
        'Inlet port & exhaust pipe temperatures', fontweight = 'bold', fontsize = 12
    )
    
    plt.plot(
        T_IP,
        linewidth = 2,
        label = 'inlet port'
    )
    plt.plot(
        T_exhPipe,
        linewidth = 2,
        label = 'exhaust pipe'
    )
    plt.grid( True );    plt.legend( loc = 'best', fontsize = 12 )
    plt.xlabel( '$\\varphi$, deg' )
    plt.ylabel( 'T, K' )

    plt.savefig( 'DRK2Py.res/inOutPars.png' )


# Valve & piston positions
# ~~~~~~~~~~~~~~~~~~~~~~~~
if movingPartsPlot == 'true':

    if saveFormat == 'csv':
        
        plt.figure()
        plt.subplot().set_title(
            'Valve & piston relative positions', fontweight = 'bold', fontsize = 12
        )

        plt.plot(
            range(-EVO, 180),
            pistonCoord
           /max(pistonCoord),
            linewidth = 2,
            label = 'piston'
        )
        plt.plot(
            range(-EVO, 180, valveCoordFrequency),
          - valveCoord
           /min(valveCoord),
            linewidth = 2,
            label = 'valve'
        )
        plt.axvspan(-IPO, IPO, alpha=0.18, color='grey')
        plt.grid( True );    plt.legend( loc = 'best', fontsize = 12 )
        plt.xlabel( '$\\varphi$, deg' )
        plt.ylabel( 'Relative motion' )


    else: # (if saveFormat == 'txt')
        plt.figure()
        plt.subplot().set_title(
            'Valve & piston velocity', fontweight = 'bold', fontsize = 12
        )

        plt.plot(
            range(-EVO, 180),
            pistonU,
            linewidth = 2,
            label = 'piston'
        )
        plt.plot(
            range(-EVO, 180, valveCoordFrequency),
            valveU,
            linewidth = 2,
            label = 'valve'
        )
        plt.axvspan(-IPO, IPO, alpha=0.18, color='grey')
        plt.grid( True );    plt.legend( loc = 'lower right', fontsize = 12 )
        plt.xlabel( '$\\varphi$, deg' )
        plt.ylabel( 'U, m/s' )
    

    plt.savefig( 'DRK2Py.res/motionParts.png' )


# Inlet & injection mass flow rate
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if inletInjectionPlot == 'true':
    plt.figure()
    plt.subplot().set_title(
        'Inlet & injection mass flow rate', fontweight = 'bold', fontsize = 12
    )

    plt.plot(
        range(-EVO, 180),
        G_inlet,
        linewidth = 2,
        label = 'inlet'
    )
    plt.plot(
        range(-EVO, 180),
        G_injection,
        linewidth = 2,
        label = 'injection'
    )

    plt.axvspan(-IPO, IPO, alpha=0.18, color='grey')
    plt.grid( True );    plt.legend( loc = 'lower right', fontsize = 12 )
    plt.xlabel( '$\\varphi$, deg' )
    plt.ylabel( 'U, m/s' )

    plt.savefig( 'DRK2Py.res/inletInjectionU.png' )
