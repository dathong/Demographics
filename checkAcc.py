import pandas as pd
import numpy as np
import sys


checkFile = sys.argv[1]
 
df = pd.read_csv(checkFile,header=None)

n1 = df[0].values
n2 = df[1].values

n3 = np.equal(n1,n2)

print("n3 = ",n3)
print("acc = ",str(np.count_nonzero(n3 == 1)/len(n3)))

print("Done")
