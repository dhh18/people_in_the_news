'''
Created on 30.5.2018

@author: Johneagle
'''

import sys, os

if __name__ == "__main__":
	path = sys.argv[1]
	
	newPath = "continentDone.csv"
	newF = open(newPath, "w", encoding="utf-8")
	
	with open(path, "r", encoding="utf-8") as f:
		for line in f:
			parse = line.split(',')
			
			last = parse[2].split('\n')[0]
			cleaned = '"' + parse[0] + '","' + parse[0] + '","' + parse[1] + '","' + last + '"' + "\n"
			newF.write(str(cleaned))
	
	newF.close()