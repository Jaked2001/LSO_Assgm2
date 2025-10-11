import Problem, Solution, Route
from ALNS import ALNS
from Parameters import Parameters
import numpy as np
import os
import time
import pandas as pd


#alphas = [0, 0.1, 0.25, 0.5, 0.75, 1]

tempControl = [0.05 ,0.1, 0.2, 0.3, 0.5, 0.8]
#colling_rate = [0.1,0.3,0.5,0.6,0.7,0.8,0.9]
instance_dir = "Instances"

# Get a list of all files in the Instances directory
instance_files = os.listdir(instance_dir)





FinalResulats = []
for instance_file in instance_files: # this is AI genrated
# Construct the full path to the instance file
    for temp in tempControl:
        results = []
        
        for randomSeed in range(3):
            testI = os.path.join(instance_dir, instance_file)
          
            Parameters.randomSeed = randomSeed
            Parameters.startTempControl = temp
         
            problem = Problem.PDPTW.readInstance(testI)
            print(problem)
            nDestroyOps = 4
            nRepairOps = 3
            alns = ALNS(problem,nDestroyOps,nRepairOps)
            starttime = time.time()        
            alns.execute()                    
            #print(alns.bestSolution.distance)
                
                

      
            results.append({'distance': alns.bestSolution.distance})
            
            break
        
        #print(results)
        avg_distance = np.mean([res['distance'] for res in results])            
        #avg_time = np.mean([res['time'] for res in results])
    
        FinalResulats.append({
    'instance' : os.path.basename(alns.problem.name),
    'temp': temp,
    'average best distance': alns.bestSolution.distance,
    #'average time': avg_time
    })
    
#print(FinalResulats)

df = pd.DataFrame(FinalResulats)
df.to_csv("tempControl.csv")
#print(df)