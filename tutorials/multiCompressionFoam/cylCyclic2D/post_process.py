#!/usr/bin/env python3
# %% imports
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

project_path = os.path.split(os.path.realpath(__file__))[0]
os.chdir(project_path)
sys.path.insert(0, os.path.realpath((os.path.join(project_path, '../../../src'))))
from foam2pandas.FoamCase import FoamCase
from foam2pandas.Checks import Checks
from foam2pandas.make_io import make_io

# %% main
df_self, df_etalon = make_io(Checks(),
                             [FoamCase('../../rhoPimpleFoam/cylCyclic2D')])

# %% exit
try:
    get_ipython
except:
    exit( (not all(df_self.all())) ) # + (not all(df_etalon.all()))