'''
Created on 30.5.2018

@author: Johneagle
'''

import sys, os

if __name__ == "__main__":
	path = sys.argv[1]
	
	newPath = "capitalsDone.csv"
	newF = open(newPath, "w", encoding="utf-8")
	
	with open(path, "r", encoding="utf-8") as f:
		for line in f:
			parse = line.split(',')
			
			frist = parse[2].split('\n')[0]
			cleaned = '"' + frist + '","' + frist + '","' + parse[0] + '","' + parse[1] + '"' + "\n"
			newF.write(str(cleaned))
	
	newF.close()