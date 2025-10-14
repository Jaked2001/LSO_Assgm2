import numpy as np
import os

a = 0
b = 45
s = 5

values = np.arange(a, b, s).tolist()


instance_dir = "Instances"

# Get a list of all files in the Instances directory
instance_files = os.listdir(instance_dir)
inst = instance_files[0]
fileName = f"log/singleOpr/singleOprExp_{inst.replace("Instances/", "")}"

print(fileName)