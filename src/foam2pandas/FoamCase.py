import os
import re
import glob

import pandas as pd
import numpy as np

class FoamCase:
    """Dictionaries with pandas dataframes with OpenFOAM case data
    """
    dircase = os.getcwd()
    def __init__(self, dircase=dircase, field_names=['p','T','Ma','rho','e']):
        def load_info(self):
            """Write case information into dictionary
            """
            log_solver = glob.glob('log.*Foam')[0]
            self.info = {
                'solver': log_solver.replace('log.', ''),
                'volume': float('NaN'),
                'nCells': self.grep_value('log.blockMesh', 'nCells', '(\d+)'),
                'exec_time': self.grep_value(log_solver, 'ExecutionTime'),
            }
            return self.info

        def load_post(self):
            """Load all .dat files into dictionary from the postProcessing/ folder
            """
            self.post = {}
            if os.path.isdir('postProcessing'):
                for (dirpath, _, filenames) in os.walk('postProcessing'):
                    for filename in filenames:
                        if '.dat' in filename:
                            # Drop '/0' from dirpath
                            post_func = os.path.basename(os.path.dirname(dirpath))

                            # Drop '(p,T,Ma,rho,e,alphaAir,alphaGas,alphaExh)'
                            # from cell(Min|Max)
                            # Read mesh or cellZone initial volume
                            if 'cellMin' in post_func or 'cellMax' in post_func:
                                post_func = re.sub('\(.*?\)', '', post_func)
                                self.info['volume'] = self.grep_value(
                                    os.path.join(dirpath, filename), 'Volume'
                                )

                            # Append dictionary with .dat file data
                            # as a pandas dataframe
                            self.post[post_func] = pd.read_csv(
                                os.path.join(dirpath, filename),
                                sep='\t', header=3, index_col=0
                            )

                # Rename keys
                for key in list(self.post.keys()):
                    self.post[key].index.names = ['time']

            return self.post

        def load_internal_fields(self, field_names):
            def list_times():
                times = set()
                for folder in os.listdir():
                    if os.path.isdir(folder):
                        times.add(folder)
                return list(times - {'0', 'constant', 'dynamicCode',
                                    'postProcessing', 'system'})

            def load_internal_field(self, time, field):
                # Check if internalField is uniform and create array from it - if not
                uniform = self.grep_value(os.path.join(time, field),
                                        "internalField   uniform", pattern='(\d+)')
                if (type(uniform) is bool) and (not uniform):
                    return np.loadtxt(os.path.join(time, field),
                                      skiprows=22, max_rows=self.info['nCells'])
                else:
                    return [uniform]

            self.fields = {}
            for field in field_names:
                self.fields[field] = pd.DataFrame()
                for time in list_times():
                    self.fields[field][time] = load_internal_field(self, time, field)
            return self.fields

        self.dir = os.path.realpath(dircase)
        os.chdir(self.dir)
        self.info = load_info(self)
        self.post = load_post(self)
        self.fields = load_internal_fields(self, field_names)

    def grep_value(self, log, key, pattern='(\d+.\d+)'):
        """Get value in line with key by pattern
        """
        found = []
        for line in open(log):
            if key in line:
                value = re.findall(pattern, line)
                found.append((key in line))
        found = any(found)

        if found and (pattern == '(\d+)'):
            return int(value[0])
        elif found and (pattern == '(\d+.\d+)'):
            return float(value[0])
        else:
            return found