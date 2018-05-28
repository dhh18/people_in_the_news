'''
Created on 28.5.2018

@author: Johneagle
'''

import json, sys

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

def makeMap(givenJson, givenCsv, filePath):
	path = givenJson

	with open(path, "r", encoding="utf-8") as f:
		data = json.load(f)
		
	res = {}
	locations = getLocations(givenCsv)

	for row in data["kwic"]:
		place_name = row['tokens'][1]['lemma']
		issn = row['structs']['text_issue_title']
		
		if len(place_name) < 4:
			continue
		
		if place_name[0].islower():
			continue
		
		if place_name not in locations:
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
					cords = locations[place]
					amount = counter[place]
					
					newStr = '"' + place + '","' + str(amount) + '","' + str(cords[0]) + '","' + str(cords[1])
					f.write(newStr)

if __name__ == "__main__":
	makeMap(sys.argv[1], sys.argv[2], "test.csv")
