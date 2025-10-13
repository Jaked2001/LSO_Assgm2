import Problem
from ALNS import ALNS
from Parameters import Parameters
import os
import pandas as pd

# --- Experiment Setup ---
instance_dir = "Instances"
output_csv_file = "log/two_opt_experiment_results.csv"

instance_files = os.listdir(instance_dir)
final_results = []

# Loop over each instance file
for instance_file in instance_files:
    # Loop over each 2-opt setting (True and False)
    for use_two_opt in [True,False]:
        
        
        Parameters.maketwoOpt = use_two_opt
        
        
        instance_path = os.path.join(instance_dir, instance_file)
        
        
        problem = Problem.PDPTW.readInstance(instance_path)
        

        alns = ALNS(problem, nDestroyOps=4, nRepairOps=3)
        alns.execute()
        

        final_results.append({
            'instance': instance_file,
            'used_two_opt': use_two_opt,
            'best_distance': alns.bestSolution.distance
        })

# --- Save Results to CSV ---
print("\n--- Experiment Complete! ---")
df = pd.DataFrame(final_results)
df.to_csv(output_csv_file, index=False)
print(f"Results saved to {output_csv_file}")
print(df)