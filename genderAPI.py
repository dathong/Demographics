import pandas as pd
from gender import getGenders
import time

df = pd.read_csv("user_names/name_sorted",header=None)

print(df)
nameList = df[0].values.tolist()

nameList = [str(x) for x in nameList]

index = 994
while index < len(nameList):
    try:
        name=nameList[index]
        print("name = ",name)
        gender = getGenders(name)
        print("gender = ",gender)
        # genderList.append(gender[0])
        with open("genderList.csv", "a") as op:
            op.write(name + "," + str(gender[0]) + "\n")
        index += 1
    except Exception as e:
        print("exept: " + str(e))
        time.sleep(3600)
        continue

print("Done")
