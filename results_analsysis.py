import pandas as pd


df = pd.read_csv("tempControl.csv")


overall_performance = df.groupby('temp')['average best distance'].mean().sort_values()

print("--- Overall Performance")
print(overall_performance)




best_k_per_instance = df.loc[df.groupby('temp')['average best distance'].idxmin()]


win_counts = best_k_per_instance['temp'].value_counts()

print(win_counts)