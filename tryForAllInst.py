import Problem, Solution, Route
from ALNS import ALNS
from Parameters import Parameters
import numpy as np
import os
import time
import pandas as pd


instance_dir = "Instances"

# Get a list of all files in the Instances directory
instance_files = os.listdir(instance_dir)

file_paths = []
for path in instance_files:
    file_paths.append(str(f"{instance_dir}/{path}"))

results = []
for inst in file_paths:
    testI = inst
    problem = Problem.PDPTW.readInstance(testI)
    print(problem)
    nDestroyOps = 4
    nRepairOps = 3
    alns = ALNS(problem,nDestroyOps,nRepairOps)
    alns.execute()

    results.append(alns.bestSolution.distance)

print(results)
print(np.mean(results))
            

