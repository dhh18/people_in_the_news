'''
Created on 28.5.2018

@author: Johneagle
'''

import json, sys, os

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

def makeMap(givenJson, continentScv, countryScv, capitalScv, mittauslaitosScv, filePath):
	path = givenJson

	with open(path, "r", encoding="utf-8") as f:
		data = json.load(f)
		
	res = {}
	continentLocations = getLocations(continentScv)
	countryLocations = getLocations(countryScv)
	capitalLocations = getLocations(capitalScv)
	mittauslaitosLocations = getLocations(mittauslaitosScv)
	
	for row in data["kwic"]:
		place_name = row['tokens'][1]['lemma']
		issn = row['structs']['text_issue_title']
		
		if len(place_name) < 4:
			continue
		
		if place_name[0].islower():
			continue
		
		if place_name not in continentLocations:
			if place_name not in countryLocations:
				if place_name not in capitalLocations:
					if place_name not in mittauslaitosLocations:
						continue
		
		if issn not in res:
			res[issn] = [place_name]
		else:
			res[issn].append(place_name)
	
	with open(filePath, "w", encoding="utf-8") as f:
		for issn in res:
			places = res[issn]
			counter = {}
			
			for place in places:
				if place not in counter:
					counter[place] = 1
				else:
					amount = counter[place] + 1
					counter[place] = amount
			
			done = []
			
			for place in places:
				if place not in done:
					done.append(place)
					cords = []
					
					if place in continentLocations:
						cords = continentLocations[place]
					else:
						if place in countryLocations:
							cords = countryLocations[place]
						else:
							if place in capitalLocations:
								cords = capitalLocations[place]
							else:
								cords = mittauslaitosLocations[place]
					
					amount = counter[place]
					
					newStr = '"' + place + '","' + str(amount) + '","' + str(cords[0]) + '","' + str(cords[1])
					f.write(newStr)

if __name__ == "__main__":
	continentScv = sys.argv[1]
	countryScv = sys.argv[2]
	capitalScv = sys.argv[3]
	mittauslaitosScv = sys.argv[4]
	
	folder = os.listdir("data/")
	
	for folderName in folder:
		subFolder = os.listdir("data/"+folderName)
		
		yearPath = "csv/"+folderName
		if not os.path.exists(yearPath):
			os.mkdir(yearPath)
		
		for file in subFolder:
			parse = file.split(".")
			
			jsonPath = "data/"+folderName+"/"+file
			newCsvMap = "csv/"+folderName+"/"+parse[0]+".csv"
			makeMap(jsonPath, continentScv, countryScv, capitalScv, mittauslaitosScv, newCsvMap)




