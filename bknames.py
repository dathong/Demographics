import pandas as pd
import csv
import os
import sys

fol = sys.argv[1]

finishedList = open(fol + "/finishedList.csv","w")

for fn in os.listdir(fol):
	if ".csv" in fn:
        #if fn in finishedList:
		print("fn = ",fn)
		finishedList.write(fn.replace(".csv","") + "\n")

print("Done")
	

