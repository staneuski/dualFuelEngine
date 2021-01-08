import os
from tabulate import tabulate

def info(project_path, case_data):
    """Create tabulated case information
    """
    return tabulate([['cells', str(case_data['cells'])]],
                    headers=['', os.path.basename(project_path)])

def times(solvers, execution_times):
    """Create tabulated execution times per solver
    """
    return tabulate({"solver": solvers, f"time, s": execution_times},
                    headers="keys")