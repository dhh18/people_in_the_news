'''
Created on 24.5.2018

@author: Johneagle
'''

import wget
import urllib

fristPart = 'https://korp.csc.fi/cgi-bin/korp.cgi?command=query&defaultcontext=1+sentence&start='
secondPart = '&end='
thirdPart = '&corpus=KLK_FI_19(19.18.17.16.15.14.13.12.11.10.09.08.07.06.05.04.03.02.01.00).KLK_FI_18(99.98.97.96.95.94.93.92.91.90.89.88.87.86.85.84.83.82.81.80.79.78.77.76.75.74.73.72.71.70.69.68.67.66.65.64.63.62.61.60.59.58.57.56.55.54.53.52.51.50.49.48.47.46.45.44.42.41.40.39.38.37.36.35.34.33.32.31.30.29.27.26.25.24.23.22.21.20).REITTIDEMO&context=&incremental=true&cqp=%5B'
lastPart = '%5D&defaultwithin=sentence&within=&loginfo=lang%3Dfi+search%3Dadv'

wordStart = 'word+%3D+%22'
wordEnd = '%22'

start = 0
end = 999999
word = input('spesific word (nothing = all): ')

saveFile = open('word.json','w')

if word != None and word != '':
	word = wordStart + word + wordEnd

path = fristPart + str(start) + secondPart + str(end) + thirdPart + str(word) + lastPart
f = urllib.request.urlopen(path)
saveFile.write(str(f.read()))

saveFile.close()


