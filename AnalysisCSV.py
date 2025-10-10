import pandas as pd


df = pd.read_csv("RegretInsertion.csv")


overall_performance = df.groupby('k')['average best distance'].mean().sort_values()

print("--- Overall Performance")
print(overall_performance)




best_k_per_instance = df.loc[df.groupby('instance')['average best distance'].idxmin()]


win_counts = best_k_per_instance['k'].value_counts()

print(win_counts)

