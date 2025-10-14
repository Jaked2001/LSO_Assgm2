import Problem, Solution, Route
from ALNS import ALNS
from Parameters import Parameters
import numpy as np
import os
import time
import pandas as pd
import sys

instance_dir = "Instances"

# Get a list of all files in the Instances directory
instance_files = os.listdir(instance_dir)[0:2]
print(instance_files)

destroyList = [1]#,2,3,4]
repairList = [1]#,2,3]
tot_results = []

bestCombinations = []
for file in instance_files:
    inst = os.path.join(instance_dir, file)
    instName = inst.replace("Instances/", "")
    instName = instName.replace(".txt", ".csv")
    fileName = f"log/singleOpr/singleOprExp_{instName}"
    bestComb_sol = sys.maxsize
    print(f"My instance is {inst}")
    
    results = []

    # Run the problem
    starttime = time.time() # get the start time
    problem = Problem.PDPTW.readInstance(inst)
    print(problem)
    alns = ALNS(problem,4,3)
    starttime = time.time()        
    alns.execute()
    endtime = time.time() # get the end time
    cpuTime = round(endtime-starttime)
    normCost = alns.bestSolution.distance
    normCpuTime = cpuTime

    for destroyOpr in destroyList:
        for repairOpr in repairList:
            starttime = time.time() # get the start time
            Parameters.useBattery = False
            Parameters.overrideOpr = False
            Parameters.destroy = destroyOpr
            Parameters.repair = repairOpr

            
            # Run the problem
            problem = Problem.PDPTW.readInstance(inst)
            print(problem)
            alns = ALNS(problem,4,3)
            starttime = time.time()        
            alns.execute()

            endtime = time.time() # get the end time
            cpuTime = round(endtime-starttime)

            # Store solution into a dict
            result = {
                "destroyOpr": int(destroyOpr),
                "repairOpr": int(repairOpr),
                "cost": float(alns.bestSolution.distance),
                "cpuTime": int(cpuTime)
            }
            results.append(result)
            
            # Find best combination for inst
            currentComb_sol = alns.bestSolution.distance
            if currentComb_sol < bestComb_sol:
                bestComb_sol = currentComb_sol
                bestComb = (destroyOpr, repairOpr)
                bestCpuTime = cpuTime
    
    # Store best combination of inst
    bestCombination = {
        "inst": instName,
        "best Combination": bestComb,
        "cost": bestComb_sol,
        "cpuTime": bestCpuTime,
        "normCost": normCost,
        "normCpuTime": normCpuTime
    }
    bestCombinations.append(bestCombination)

    # Create list with all the results (useful for future reference)
    tot_results.append(results)

    # store results as csv
    results_df = pd.DataFrame(results)
    results_df.to_csv(fileName)

bestCombinations_df = pd.DataFrame(bestCombinations)
bestCombinations_df.to_csv("log/singleOpr/bestCombinationForEachInstance.csv")
