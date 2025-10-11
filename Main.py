# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 14:34:48 2022

@author: Original template by Rolf van Lieshout
"""

import Problem, Solution, Route
from ALNS import ALNS
#from ALNS import Parameters
from Parameters import Parameters

testI = "instances/lr112.txt"
problem = Problem.PDPTW.readInstance(testI)
print(problem)
nDestroyOps = 3
nRepairOps = 3
alns = ALNS(problem,nDestroyOps,nRepairOps)

alns.execute()

