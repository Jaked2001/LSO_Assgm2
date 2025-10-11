# -*- coding: utf-8 -*-

import Problem, Solution, Route
from ALNS import ALNS
from Parameters import Parameters
import os
#lr112

instance_dir = "Instances"
instance_files = os.listdir(instance_dir)


alphas = [0, 0.1, 0.25, 0.5, 0.75, 1]
results = []

for inst in instance_files:

    for alpha in alphas:
        Parameters.alpha = alpha
        Parameters.nIterations = 2
        testI = os.path.join(instance_dir, inst)
        problem = Problem.PDPTW.readInstance(testI)
        print(problem)
        nDestroyOps = 3
        nRepairOps = 3
        alns = ALNS(problem,nDestroyOps,nRepairOps)
        alns.execute()
        results.append((alpha, float(alns.bestSolution.distance)))
        

print(results)    


