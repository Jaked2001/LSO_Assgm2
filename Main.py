# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 14:34:48 2022

@author: Original template by Rolf van Lieshout
"""

import Problem, Solution, Route
from Parameters import Parameters
from ALNS import ALNS
import numpy as np
import os
import pandas as pd


instance_dir = "Instances"
# Get a list of all files in the Instances directory
instance_files = os.listdir(instance_dir)

results_log = []
for testI in instance_files:
    Parameters.useBattery = False
    inst = os.path.join(instance_dir, testI)
    problem = Problem.PDPTW.readInstance(inst)
    print(problem)
    nDestroyOps = 4
    nRepairOps = 3
    alns = ALNS(problem,nDestroyOps,nRepairOps)
    alns.execute()
    print(len(alns.bestSolution.routes))
    results_log.append({
        "inst": testI,
        "cost": alns.bestSolution.distance,
        "cpuTime": alns.cpuTime
    })
results_log_df = pd.DataFrame(results_log)
results_log_df.to_csv("bestSolutionOfEachInstance.csv")
