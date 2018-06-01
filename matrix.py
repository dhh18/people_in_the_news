'''
Created on 1.6.2018

@author: Johneagle
'''

import sys, os

if __name__ == "__main__":
	list = []
	boolean = 0
	
	while boolean < 1:
		id = input('give magasine id (enter ends): ')
		if id == '':
			boolean = 1
		else: 
			list.append(id)
	
	csvMatrixPath = "csv/matrix.csv"
	matrix = {}	
		
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
					hits = parsed[1]+','+str(start)

					if place in matrix:
						matrix[place].append(hits)
					else:
						new = []
						new.append(hits)
						matrix[place] = new

	with open(csvMatrixPath, "w", encoding="utf-8") as f:
		headline = '"'
		for year in range(1870, 1911):
			headline += '","'+str(year)
		headline += '"'+'\n'
		f.write(headline)
		
		for place in matrix:
			data = matrix[place]
			floatYear = 1870
			line = '"'+place+'","'
			
			for pair in data:
				parse = pair.split(',')
				hits = parse[0]
				year = parse[1]
				
				while floatYear < int(year):
					line += '","'
					floatYear += 1
				
				line += str(hits)
			
			while floatYear < 1911:
				line += '","'
				floatYear += 1
			
			line += '"'+'\n'
			f.write(line)