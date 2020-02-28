output = f'''-------------------------------------------------------------------------------
       ___       |
     _|o_ |_     |   Language: Python
    /  ___| \    |   Version:  3.7
    \_| ____/    |   Website:  ¯\_(ツ)_/¯
      |__o|      |
-------------------------------------------------------------------------------

Scavenging duration: {round(max( np.arange(0, (EVO + 180)*degDeltaT, degDeltaT) ), 4)} s

Mean piston speed during scavenging: {max(pistonU)/2} m/s

Initial conditions:
- Parameters at EVO = {360 - EVO}˚ CA:
    Pressure: {round(p[360 - EVO])} Pa
    Temperature: {T[360 - EVO]} K
    Piston displacement: {abs(min(pistonCoord))} m from BDC

Boundary conditions:
- Mean parameters in the inlet port:
    Pressure: {round(np.mean(p_IP))} Pa
    Temperature: {round(np.mean(T_IP), 3)} K

- Mean parameters in the exhaust pipe:
    Pressure: {round(np.mean(p_exhPipe))} Pa
    Temperature: {round(np.mean(T_exhPipe), 3)} K

-------------------------------------------------------------------------------'''

report = open('DRK2Py.res/DRK2Py.log', 'w')
report.write(output)
report.close()

if terminalOutput == 'true':    print(output)
