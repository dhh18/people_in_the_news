'''
Created on 24.5.2018

@author: petrileskinen
'''
import csv
import glob
import json
import re
import sys

DELIMITER = "\t"
CONTEXT_IDS = ['text_publ_id', 'paragraph_id', 'text_issue_date']
#    PYTHONIOENCODING='utf-8' python3 extract_personnames.py json/korp.json 
 
def main(infolder="persons/csv/", outfile=None):
    
    def pairs(arr):
        arr = list(set(arr))
        for i in range(len(arr)-1):
            for j in range(i+1,len(arr)):
                if arr[i]<arr[j]:
                    yield arr[i],arr[j]
                else:
                    yield arr[j],arr[i]
    
    if infolder[-1]!="*":
        infolder = infolder + "*"
    print(infolder)
    files = glob.glob(infolder)
    
    dct = {}
    link_dct = {}
    
    for file in files:
        print("Reading {}".format(file))
        with open(file, newline='', encoding="utf-8") as csvfile:
            
            csvreader = csv.DictReader(csvfile, delimiter=DELIMITER)
            fields = csvreader.fieldnames
            for row in csvreader:
                label = row['name']
                key = getKey(label)
                if not key in dct:
                    dct[key] = {'name':row['name'], 'links':[]}
                row2 = copyRow(row)
                dct[key]['links'].append(row2)
                
                rowkey = hashRow(row)
                if not rowkey in link_dct:
                    link_dct[rowkey]=[]
                link_dct[rowkey].append(key)
                
    for d in dct:
        print(dct[d])
        #print("{}\t{}".format(dct[d]['name'], len(dct[d])))
    
    link_dct = dict((d, link_dct[d]) for d in link_dct if len(link_dct[d])>1)
    
    graph_dct = {}
    
    for d in link_dct:
        arr = link_dct[d]
        for x,y in pairs(arr):
            if not x in graph_dct:
                graph_dct[x]={}
            if not y in graph_dct[x]:
                graph_dct[x][y]=0
            graph_dct[x][y] += 1
    
    
    res = []
    for x in graph_dct:
        for y in graph_dct[x]:
            if 1<graph_dct[x][y] and graph_dct[x][y]<100:
                x_label = dct[x]['name']
                y_label = dct[y]['name']
                res.append([x_label,y_label, graph_dct[x][y]])
                
    res = sorted(res, key=lambda x:x[-1])
    
    if outfile:
        csvfile = open(outfile, 'w', newline='', encoding="utf-8")
        csvwriter = csv.writer(csvfile, delimiter=DELIMITER,
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(['to', 'from', 'weigth'])
        for r in res:
            csvwriter.writerow(r)
        csvfile.close()
        print("Graph written to {}".format(outfile))
    else:
        for r in res:
            print("{}, {}:\t{}".format(r[0],r[1],r[2]))
            
    # print(graph_dct)
    
    
    
    return


def getKey(label):
        st = label.lower()
        st = re.sub(r'[áàâ]','a',st)
        st = re.sub(r'[éèêë]','e',st)
        st = re.sub(r'[óòö]','e',st)
        return re.sub(r'[. -]','',st)

def copyRow(row):
    row2=row.copy()
    del row2['name']
    return row2

def hashRow(row):
    return ''.join([row[d] for d in CONTEXT_IDS])


class Person:
    
    def __init__(self, label):
        self.altLabels=[]
        self.label = label
        """
        #    P. T. Leskinen
        altLabel = re.sub(r'([A-ZÖÄÅ])\S+\s','\g<1>. ',label)
        if altLabel != label:
            self.altLabels.append(altLabel)
    
        #    Petri T. Leskinen
        altLabel = re.sub(r'(\S+)\s([A-ZÖÄÅ])\S+\s(.*)$','\g<1> \g<2>. \g<3>',label)
        if altLabel != label:
            self.altLabels.append(altLabel)
        """
    @property
    def key(self):
        st = self.label.lower()
        st = re.sub(r'[áàâ]','a',st)
        st = re.sub(r'[éèêë]','e',st)
        return re.sub(r'[. -]','',st)
    
    @property
    def keys(self):
        return [re.sub(r'[. -]','',st.lower()) for st in [self.label]+self.altLabels]
    
    def __lt__(self, other):
        return self.label.split(' ')[-1] < other.label.split(' ')[-1]
    
    def __str__(self):
        return self.label
        return ', '.join([self.label]+self.altLabels)
    
    
if __name__ == '__main__':
    main(sys.argv[1], 
         sys.argv[2] if len(sys.argv)>2 else None)
    
    

