'''
Created on 29.5.2018

@author: petrileskinen
'''
import csv
import re
import glob
DELIMITER = "\t"

def main():
    arr = [('persons/graph_Tmies_1907.csv', 'Työmies'),
           ('persons/graph_US_1907.csv', 'Uusi Suometar'),
           ('persons/graph_HS_1907.csv', 'Helsingin Sanomat')
           ]
    outfile = 'persons/personTagList.csv'
    kansanedustajat = 'persons/1907_kansanedustajat.csv'
    dct_ke = readKansanedustajat(kansanedustajat)
    #print(dct_ke)
    #return
    dct = {}
    for file, tag in arr:
        with open(file, newline='', encoding="utf-8") as csvfile:
            
            csvreader = csv.DictReader(csvfile, delimiter=DELIMITER)
            fields = csvreader.fieldnames
            
            for row in csvreader:
                for label in [row[fields[0]], row[fields[1]]]:
                    key = getKey(label)
                    if not key in dct:
                        dct[key] = {'label':label, 
                                    'tags':set(),
                                    'party':None,
                                    'district':None}
                    if key in dct_ke:
                        dct[key]['party'] = dct_ke[key]['party']
                        dct[key]['district'] = dct_ke[key]['district']
                        
                    dct[key]['tags'].add(tag)
    
    if outfile:
        csvfile = open(outfile, 'w', newline='', encoding="utf-8")
        csvwriter = csv.writer(csvfile, delimiter=DELIMITER,
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(['Source', 'tags', 'party', 'district'])
        for d in dct:
            csvwriter.writerow([dct[d]['label'], 
                                ';'.join(dct[d]['tags']),
                                dct[d]['party'],
                                dct[d]['district']
                                ])
        csvfile.close()
        print("Data written to {}".format(outfile))


def readKansanedustajat(infile):
    dct = {}
    with open(infile, newline='', encoding="iso-8859-1") as csvfile:
        csvreader = csv.DictReader(csvfile, 
                                   fieldnames=('name','party','district','note'),
                                   delimiter=';')
        for row in csvreader:
            row = dict([(x,row[x].strip()) for x in row])
            label = row['name']
            key = getKey(label)
            dct[key]=row
    return dct


def getKey(label):
        st = label.lower()
        st = re.sub(r'[áàâ]','a',st)
        st = re.sub(r'[éèêë]','e',st)
        st = re.sub(r'[óòö]','e',st)
        st = re.sub(r'W','V',st)
        st = re.sub(r'w','v',st)
        return re.sub(r'[. -]','',st)
    
if __name__ == '__main__':
    main()