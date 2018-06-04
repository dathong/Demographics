import pandas as pd
import sys

inputFile = sys.argv[1]
outputFile = sys.argv[2]

df = pd.read_csv(inputFile,sep="|")

c = df.columns.values.tolist()

if 'retweetflag' in c:
	c.remove('retweetflag')
if 'IgnoreFlag' in c:
	c.remove('IgnoreFlag')

c = ['IgnoreFlag'] + c

df1 = df[c]

df1.to_csv(outputFile,index=False,sep="|")
