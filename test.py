import numpy as np


a = 0
b = 45
s = 5

values = np.arange(a, b, s).tolist()

myList = []
for i in values:
    myList.append(i) 

print(myList)