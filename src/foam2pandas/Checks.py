import pandas as pd
import numpy as np
from scipy.interpolate import interp1d

from foam2pandas.FoamCase import FoamCase

class Checks:
    basic_case = FoamCase()
    def __init__(self, basic_case=basic_case):
        def extremums(self, basic_case):
            self.extremums, self.case_extremums = {}, {}
            funcs = set(basic_case.post.keys()) & set(['cellMax', 'cellMin'])
            if len(funcs) > 0:
                for func in list(funcs):
                    self.case_extremums[func] = {}
                    extr = func.replace('cellM', 'm') # 'min' or 'max'
                    if extr == 'max':
                        self.extremums[func] = []
                        for col in basic_case.post[func]:
                            self.case_extremums[func][col] = basic_case.post[func][col].le(
                                self.LIMITS[extr][col.replace(extr,'')]
                            )
                            self.extremums[func].append([col,
                                                         all(self.case_extremums[func][col]),
                                                         max(basic_case.post[func][col])])
                        self.extremums[func] = pd.DataFrame(self.extremums[func],
                                                            columns=['field', 'passed', 'value'])
                        self.extremums[func] = self.extremums[func].set_index('field')
                    elif extr == 'min':
                        self.extremums[func] = []
                        for col in basic_case.post[func]:
                            self.case_extremums[func][col] = basic_case.post[func][col].ge(
                                self.LIMITS[extr][col.replace(extr,'')]
                            )
                            self.extremums[func].append([col,
                                                         all(self.case_extremums[func][col]),
                                                         min(basic_case.post[func][col])])
                        self.extremums[func] = pd.DataFrame(self.extremums[func],
                                                            columns=['field', 'passed', 'value'])
                        self.extremums[func] = self.extremums[func].set_index('field')
            return self.extremums['cellMin'].append(self.extremums['cellMax']), self.case_extremums

        def std(self):
            def std_along_convolved(par):
                """Calculate the standart deviation along the convolved data
                """
                par = par[abs(par - np.median(par))/np.median(par) < 0.4]
                par_conv = np.convolve(par, np.ones(4)/4, mode='same')
                return np.std((par_conv[2:-2] - par[2:-2])/par[2:-2])

            case_fields = self.case.fields
            self.std = pd.DataFrame(sorted(case_fields['p'].keys().astype(float)),
                                    columns=['time']).set_index('time')
            pars = list(case_fields)
            pars.remove('e')
            pars.remove('Ma')
            for par in pars:
                std_deviations = []
                for key in sorted(case_fields[par].keys()):
                    std_deviations.append(std_along_convolved(case_fields[par][key]))
                self.std[par] = std_deviations
            return self.std

        def mass(self):
            if 'volFieldValue(operation=volIntegrate,rho)' in self.case.post.keys():
                mass = self.case.post['volFieldValue(operation=volIntegrate,rho)']
                return float((mass.max() - mass.min())/mass.iloc[0])
            else:
                return None

        self.LIMITS = {'min': {'(p)': 1e4,
                               '(T)': 200,
                               '(Ma)': 0,
                               '(rho)': 0,
                               '(e)': -float('inf'),
                               '(alphaAir)': -0.1,
                               '(alphaGas)': -0.1,
                               '(alphaExh)': -0.1,},
                       'max': {'(p)': 1e8,
                               '(T)': 4000,
                               '(Ma)': 1,
                               '(rho)': 30,
                               '(e)': float('inf'),
                               '(alphaAir)': 1.1,
                               '(alphaGas)': 1.1,
                               '(alphaExh)': 1.1,}}
        self.case = basic_case
        self.extremums, self.case_extremums = extremums(self, basic_case)
        self.std = std(self)
        self.mass = mass(self)

    def get_delta(self, etalon_cases, func_name):
        if (len(etalon_cases)):
            delta = {}
            basic_volAverage = self.case.post[func_name]
            for etalon_case in etalon_cases:
                case_delta = []
                etalon_volAverage = etalon_case.post[func_name]
                for par in etalon_volAverage.keys():
                    f = interp1d(etalon_volAverage.index, etalon_volAverage[par],
                                 fill_value='extrapolate')
                    std_error = np.std(
                        (basic_volAverage[par] - f(basic_volAverage.index))/basic_volAverage[par]
                    )
                    case_delta.append([par, np.nan_to_num(std_error) < 0.15, std_error*100])
                case_delta = pd.DataFrame(case_delta,
                                          columns=['par', 'passed', 'std(error)'])
                delta[etalon_case.info['solver']] = case_delta.set_index('par')
            return delta

    def exec_time(self, etalon_cases):
        exec_time = []
        for etalon_case in etalon_cases:
            delta = etalon_case.info['exec_time'] - self.case.info['exec_time']
            exec_time.append([etalon_case.info['solver'], delta > 0, 
                                etalon_case.info['exec_time'], delta])
        exec_time = pd.DataFrame(exec_time, columns=['solver', 'passed', 'exec_time', 'gap'])
        return exec_time.set_index('solver')

    def compare_posts(self, etalon_cases):
        compared = {}
        func_names = list(self.case.post)
        func_names.remove('cellMax')
        func_names.remove('cellMin')
        for func_name in func_names:
            compared[func_name] = self.get_delta(etalon_cases, func_name)

        post_tests = {}
        for etalon_case in etalon_cases:
            joined_df = pd.DataFrame(columns=['par', 'passed', 'std(error)']).set_index('par')
            for func_name in func_names:
                post_func_test = compared[func_name][etalon_case.info['solver']]
                joined_df = joined_df.append(post_func_test)
            post_tests[etalon_case.info['solver']] = joined_df
        return post_tests

