import pandas as pd
from textblob import TextBlob
import os

directory = "drug_results"

for path, dirs, files in os.walk(directory):
	print(path)
	print(dirs)
	print(files)

print("done")
