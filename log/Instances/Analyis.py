import pandas as pd
import os
import glob

dir = "log\Instances"




instance_files = os.listdir(dir)

Results = []
test = [-1,-5,-10]
for file in glob.glob(os.path.join(dir, "*.csv")):
    df = pd.read_csv(file)
    df.columns = df.columns.str.strip() 
    df['difference'] = df['Cost Best'].pct_change() * 100
    
    
    for number in test:
        improved = df[df['difference'] < number]
        
        if not improved.empty:
            
            last_improved = improved.iloc[-1]
            Results.append({
                "file": os.path.basename(file),
                "iteration": int(last_improved["Iter"]),
                "threshhold" : number,
                "improvement (%)": last_improved["difference"]
            })
        else:
                Results.append({
                "file": os.path.basename(file),
                "iteration": None,
                "threshhold" : number,
                "improvement (%)": None
                })
            
    #print(impooved)

print(Results)

df = pd.DataFrame(Results)
df.to_csv("Itteraion.csv")

