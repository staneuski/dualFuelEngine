'''----------------------------------------------------------------------------
       ___       |
     _|˚_ |_     |   Language: Python
    /  ___| \    |   Version:  3.x
    \_| ____/    |   Website:  https://github.com/StasF1/dualFuelEngine
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
    plt.xlabel( '$\\varphi$, deg CA' )
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
    plt.xlabel( '$\\varphi$, deg CA' )
    plt.ylabel( 'T, K' )

    plt.savefig( 'DRK2Py.res/cylPars.png' )


# Inlet & outlet parameters
# ~~~~~~~~~~~~~~~~~~~~~~~~~
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
    plt.xlabel( '$\\varphi$, deg CA' )
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
    plt.xlabel( '$\\varphi$, deg CA' )
    plt.ylabel( 'T, K' )

    plt.savefig( 'DRK2Py.res/inOutPars.png' )


# Inlet & injection mass flow rate
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if inletInjectionPlot == 'true':

    if massFlowRatePar == 'rhoU':
        yLabel = '$\\rho U$, kg/m/s'
        yG_inlet     = rhoU_inlet
        yG_injection = rhoU_injection

    elif massFlowRatePar == 'G':
        yLabel = 'G, kg/s'
        yG_inlet     = G_inlet
        yG_injection = G_injection
    else:
        exit('Error: massFlowRatePar variable is incorrect!')

    plt.figure()
    plt.subplot().set_title(
        'Inlet & injection mass flow rate', fontweight = 'bold', fontsize = 12
    )
    plt.plot(
        range(-EVO, 180),
        yG_inlet,
        linewidth = 2,
        label = 'inlet'
    )
    # plt.plot(
    #     range(-EVO, 180),
    #     yG_injection,
    #     linewidth = 2,
    #     label = 'injection'
    # )
    plt.axvspan(-IPO, IPO, alpha=0.18, color='grey')
    plt.grid( True );    plt.legend( loc = 'best', fontsize = 12 )
    plt.xlabel( '$\\varphi$, deg CA' )
    plt.ylabel( yLabel )

    plt.savefig( 'DRK2Py.res/inletInjectionU.png' )


# Valve & piston positions
# ~~~~~~~~~~~~~~~~~~~~~~~~
if movingPartsPlot == 'true':

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
    plt.annotate(
        '(BDC)', (1, 1),
        xytext = (EVO/(EVO + 180)*1.19, -0.06), textcoords='axes fraction',
        horizontalalignment='right', verticalalignment='top'
    )
    plt.annotate(
        'IPC', xy=(-IPO, 12),  xycoords='data',
        xytext=(0.1, 0.95), textcoords='axes fraction',
        arrowprops=dict(arrowstyle="-", color="0.5", shrinkB=1),
        horizontalalignment='left', verticalalignment='top',
    )
    plt.annotate(
        'IPO', xy=(IPO, 12),  xycoords='data',
        xytext=(0.58, 0.95), textcoords='axes fraction',
        arrowprops=dict(arrowstyle="-", color="0.5", shrinkB=1),
        horizontalalignment='right', verticalalignment='top',
    )
    plt.axvspan(-IPC, IPO, alpha=0.18, color='grey')
    plt.axvline(x = 0, color='black', linestyle = '--')
    plt.grid( True );    plt.legend( loc = 'best', fontsize = 12 )
    plt.xlabel( '$\\varphi$, deg CA' )
    plt.ylabel( 'U, m/s' )

    plt.savefig( 'DRK2Py.res/motionParts.png' )