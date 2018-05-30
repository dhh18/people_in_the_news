'''
Created on 29.5.2018

@author: Johneagle
'''

import sys, os

if __name__ == "__main__":
	path = sys.argv[1]
	
	newPath = "mittauslaitosParsed.csv"
	newF = open(newPath, "w", encoding="utf-8")
	
	with open(path, "r", encoding="utf-8") as f:
		for line in f:
			parse = line.split(',')
			
			last = parse[1].split('\n')[0]
			cleaned = '"' + parse[10] + '","' + parse[8] + '","' + parse[0] + '","' + last + '"' + "\n"
			newF.write(str(cleaned))
	
	newF.close()