'''
Created on 25.5.2018

@author: Johneagle
'''

import sys, os

if __name__ == "__main__":
	path = sys.argv[1]
	
	newPath = "parsed.csv"
	newF = open(newPath, "w", encoding="utf-8")
	
	with open(path, "r", encoding="utf-8") as f:
		for line in f:
			parse = line.split('","')
			cleaned = '"' + parse[1] + '","' + parse[8] + '","' + parse[18] + '","' + parse[19] + '"' + "\n"
			newF.write(str(cleaned))
	
	newF.close()
