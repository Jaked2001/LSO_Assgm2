# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 14:34:48 2022

@author: Original template by Rolf van Lieshout
"""

import Problem, Solution, Route
from ALNS import ALNS


testI = "instances/lc207.txt"
problem = Problem.PDPTW.readInstance(testI)
print(problem)
nDestroyOps = 4
nRepairOps = 3
alns = ALNS(problem,nDestroyOps,nRepairOps)
alns.execute()