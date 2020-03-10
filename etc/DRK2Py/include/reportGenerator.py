output = f'''-------------------------------------------------------------------------------
       ___       |
     _|o_ |_     |   Language: Python
    /  ___| \    |   Version:  3.x
    \_| ____/    |   Website:  https://github.com/StasF1/dualFuelEngine
      |__o|      |
-------------------------------------------------------------------------------

Scavenging duration: {round(max( np.arange(0, (EVO + 180)*degDeltaT, degDeltaT) ), 4)} s

Piston velocity during scavenging:
    Max: {round(max(pistonU), 4)} m/s
    Mean: {S*n/30} m/s

Initial conditions:
- Parameters at EVO = {360 - EVO}˚ CA:
    Pressure: {round(p[360 - EVO]*1e-06, 4)} MPa
    Temperature: {T[360 - EVO]} K
    Piston displacement: {abs(min(pistonCoord))} m from BDC

Boundary conditions:
- Mean parameters in the inlet port:
    Pressure: {round(np.mean(p_IP)*1e-06, 4)} MPa
    Temperature: {round(np.mean(T_IP), 4)} K

- Mean parameters in the exhaust pipe:
    Pressure: {round(np.mean(p_exhPipe)*1e-06, 4)} MPa
    Temperature: {round(np.mean(T_exhPipe), 4)} K

-------------------------------------------------------------------------------'''

report = open('DRK2Py.res/DRK2Py.log', 'w')
report.write(output)
report.close()

if terminalOutput == 'true':    print(output)
