f = open("predGender.csv","w")
for index, row in dfFull.iterrows():
			for fName in female_name_list:
							if str(fName) in str(row['full_name']).lower():
												print("pred female 1",index,str(fName))
															#row['gender_pred'] = "F"
																		f.write(row['gender'] + ",F\n" )
																					continue
																				for fName in male_name_list:
																								if str(fName) in str(row['full_name']).lower():
																													print("pred male 1",index,str(fName))
																																#row['gender_pred'] = "M"
																																			f.write(row['gender'] + ",M\n" )
																																						continue
																																					male_keywords = ['man','boy','guy','father']
																																						female_keywords = ['woman','girl','lady','mother']
																																							
																																								if any(str(x).lower() in str(row['description']).lower() for x in male_keywords):
																																												print("pred male 2",index)
																																														#row['gender_pred'] = "M"
																																																f.write(row['gender'] + ",M\n" )
																																																	if any(str(x).lower() in str(row['description']).lower() for x in female_keywords):
																																																					print("pred female 2",index)
																																																							#row['gender_pred'] = "F"
																																																									f.write(row['gender'] + ",F\n" )
