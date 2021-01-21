import os
import pandas as pd

from foam2pandas.FoamCase import FoamCase
from foam2pandas.Checks import Checks

def make_io(checks, etalon_cases):
    # Self-tests
    df_self = pd.DataFrame(
        [[os.path.basename(checks.case.dir),
          checks.case.info['nCells'],
          (checks.case.info['exec_time']),
          all(checks.extremums['passed']),
          all(checks.std < 0.05)]],
        columns=['case', 'nCells', 'exec_time',
                'extremums', 'std(convolved)']
    )
    if checks.mass:
        df_self['mass'] = (checks.mass < 0.005)
    df_self = df_self.set_index('case')

    # Etalon tests
    etalon_checks = checks.compare_posts(etalon_cases=etalon_cases)
    df_etalon = pd.DataFrame()
    for solver in etalon_checks:
        df_etalon[solver] = etalon_checks[solver]['passed']
    etalon_checks = checks.exec_time(etalon_cases=etalon_cases)
    df_etalon = df_etalon.append(etalon_checks['passed'])
    df_etalon = df_etalon.rename(index={'passed': 'exec_time'})
    df_etalon.index.names = ['test']

    # Write log-file
    log = open(os.path.join(checks.case.dir, "log.postProcess"), 'w+')
    log.write('Tests summary\n')
    log.write(df_self.to_string() + '\n\n')

    log.write('Etalon tests\n')
    log.write(df_etalon.to_string() + '\n\n\n')

    log.write('Self-tests\n')
    log.write('- is all extremums in the limits:\n')
    log.write(checks.extremums.to_string() + '\n\n')
    log.write('- is standart deviation along the convolved data less then 5%:\n')
    log.write(
        checks.std.join(
            (checks.std < 0.05).rename(columns={'p': 'passed(p)',
                                                    'T': 'passed(T)',
                                                    'rho': 'passed(rho)'})
        ).to_string()
        + '\n\n'
    )
    log.write('end\n')
    log.close()

    print(df_self, '\n\n', df_etalon)
    return df_self, df_etalon