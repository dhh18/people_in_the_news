'''
Created on 30.5.2018

@author: Johneagle
'''

import sys, os

def getLocations(scvPath):
	scv = {}
	
	with open(scvPath, "r", encoding="utf-8") as f:
		for line in f:
			parse = line.split('","')
			cords = [parse[2], parse[3]]
			name = parse[0].split('"')[1]
			
			if name not in scv:
				scv[name] = cords 
	
	return scv

if __name__ == "__main__":
	list = []
	boolean = 0
	
	while boolean < 1:
		id = input('give magasine id (enter ends): ')
		if id == '':
			boolean = 1
		else: 
			list.append(id)
	
	sums = {}
	
	for id in list:
		start = 1870
		end = 1911
		
		while start < end:
			filePath = "csv/"+str(start)+"/"+str(id)+".csv"
			start += 1
			
			if not os.path.exists(filePath):
				continue
			
			with open(filePath, "r", encoding="utf-8") as f:
				for line in f:
					parsed = line.split('","')
					place = parsed[0]
					
					if place in sums:
						add = sums[place]
						
						hits = int(add[1]) + int(parsed[1])
						add[1] = hits
						
						sums[place] = add
					else: 
						sums[place] = parsed
	
	sumCsvFilePath = "csv/conclusion_"+str(list)+".csv"
	continentplaces = getLocations(sys.argv[1])
	countryplaces = getLocations(sys.argv[2])
	capitalplaces = getLocations(sys.argv[3])
	
	with open(sumCsvFilePath, "w", encoding="utf-8") as f:
		for data in sums:
			parsed = sums[data]
			which = "kotimaa"
			test = data.split('"')[1]
			
			if test in continentplaces:
				which = "ulkomaa"
			else:
				if test in countryplaces:
					which = "ulkomaa"
				else:
					if test in capitalplaces:
						which = "ulkomaa"
			
			last = parsed[3].split("\n")[0]
			strRow = parsed[0]+'","'+str(parsed[1])+'","'+parsed[2]+'","'+last+',"'+which+'"'+'\n'
			f.write(strRow)