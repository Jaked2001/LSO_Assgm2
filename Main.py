# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 14:34:48 2022

@author: Original template by Rolf van Lieshout
"""

import Problem, Solution, Route
from ALNS import ALNS
from pathlib import Path
import os

# testI = "instances/lc102.txt"
# problem = Problem.PDPTW.readInstance(testI)
# print(problem)
# nDestroyOps = 3
# nRepairOps = 3
# alns = ALNS(problem,nDestroyOps,nRepairOps)
# alns.execute()

# Path to the directory containing the instances
instance_dir = "Instances"

# Get a list of all files in the Instances directory
instance_files = os.listdir(instance_dir)

# Loop over each instance file
for instance_file in instance_files: # this is AI genrated
    # Construct the full path to the instance file
    testI = os.path.join(instance_dir, instance_file)
    


    print(f"Running ALNS for instance: {testI}")
    
    problem = Problem.PDPTW.readInstance(testI)
    print(problem)
    nDestroyOps = 3
    nRepairOps = 3
    alns = ALNS(problem,nDestroyOps,nRepairOps)
    alns.execute()
