# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 14:34:48 2022

@author: Original template by Rolf van Lieshout
"""

import Problem, Solution, Route
from ALNS import ALNS

#lr112
instance_dir = "Instances"

# Get a list of all files in the Instances directory
instance_files = os.listdir(instance_dir)

testI = "instances/c202C16.txt"
problem = Problem.PDPTW.readInstance(testI)
print(problem)
nDestroyOps = 4
nRepairOps = 3
alns = ALNS(problem,nDestroyOps,nRepairOps)
alns.execute()
print(len(alns.bestSolution.routes))
for i in alns.bestSolution.routes:
    print(i.computeDistance())
