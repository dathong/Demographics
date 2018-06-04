import sys
import os

outputFile = open("kaggle_name.csv","w")
outputFile.write("_unit_id,full_name,screen_name\n")
for fn in os.listdir("user_info_kaggle"):
	#print("fn = ",fn)
	if ".csv" in fn:
		#print("fn = ",fn)
		f = open("user_info_kaggle/" + fn,"r")
		s = f.read()
		#print("s = ",s[:100])
		s = [str(x) for x in s.split(",")]
		full_name = ""
		screen_name = ""
		for ss in s:
			if 'name=' in ss and 'screen_name=' not in ss:
				full_name = ss.split("=")[1].replace("'","")
			if 'screen_name=' in ss:
				screen_name = ss.split("=")[1].replace("'","")
		print(full_name,screen_name)
		outputFile.write(fn.replace(".csv","") + "," + full_name + "," + screen_name + "\n")

print("Done")
		
