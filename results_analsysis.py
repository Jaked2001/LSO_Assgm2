import pandas as pd


df = pd.read_csv("minNBHsize.csv")


overall_performance = df.groupby('minNBH')['average best distance'].mean().sort_values()

print("--- Overall Performance")
print(overall_performance)




best_k_per_instance = df.loc[df.groupby('minNBH')['average best distance'].idxmin()]


win_counts = best_k_per_instance['minNBH'].value_counts()

print(win_counts)