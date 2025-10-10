import Problem, Solution, Route
from ALNS import ALNS
from Parameters import Parameters
import numpy as np
import os
import time
import pandas as pd


k = [1,2,3,4] # 1 is for greedy,500 stands for infinte

instance_dir = "Instances"

# Get a list of all files in the Instances directory
instance_files = os.listdir(instance_dir)





FinalResulats = []
for instance_file in instance_files: # this is AI genrated
# Construct the full path to the instance file
    for i in k:
        results = []
        
        for randomSeed in range(3):
            testI = os.path.join(instance_dir, instance_file)
            Parameters.randomSeed = randomSeed
            Parameters.Regretk = i
            testI = os.path.join(instance_dir, instance_file)
            problem = Problem.PDPTW.readInstance(testI)
            print(problem)
            nDestroyOps = 3
            nRepairOps = 3
            alns = ALNS(problem,nDestroyOps,nRepairOps)
            starttime = time.time()        
            alns.execute()                    
            #print(alns.bestSolution.distance)
                
                
            endtime = time.time() # get the end time
            cpuTime = round(endtime-starttime)
            results.append({'distance': alns.bestSolution.distance, 'time': cpuTime})
        
        #print(results)
        avg_distance = np.mean([res['distance'] for res in results])            
        avg_time = np.mean([res['time'] for res in results])
    
        FinalResulats.append({
    'instance' : os.path.basename(alns.problem.name),
    'k': i,
    'average best distance': alns.bestSolution.distance,
    'average time': avg_time
    })
    
#print(FinalResulats)
    
df = pd.DataFrame(FinalResulats)
df.to_csv("RegretInsertion.csv")
#print(df)
