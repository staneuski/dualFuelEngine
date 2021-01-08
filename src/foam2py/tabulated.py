import os
from tabulate import tabulate

def create_info(post_process_path, case_data):
    """Create tabulated case information
    """
    return tabulate([['cells', str(case_data['cells'])]],
                    headers=['', os.path.basename(post_process_path)])

def create_times(solvers, execution_times):
    """Create tabulated execution times per solver
    """
    return tabulate({"solver": solvers, f"time, s": execution_times},
                    headers="keys")