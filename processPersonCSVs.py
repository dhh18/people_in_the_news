'''
Created on 24.5.2018

@author: petrileskinen
'''
import csv
import glob
import json
import re
import sys
import xml.etree.cElementTree as ET
from xml.etree import ElementTree
from xml.dom import minidom
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from platform import node

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
                    dct[key] = {'name':row['name'], 'links':[], 'degree':0}
                row2 = copyRow(row)
                dct[key]['links'].append(row2)
                
                rowkey = hashRow(row)
                if not rowkey in link_dct:
                    link_dct[rowkey]=[]
                link_dct[rowkey].append(key)
    
    
    arr = [(dct[d]['name'], len(dct[d]['links'])) for d in dct]
    arr = sorted(arr, key=lambda x:x[-1], reverse=True)
    
    for d in arr[:20]:
        print("{}\t{}".format(d[0],d[1]))
    
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
            
            if 4<graph_dct[x][y] and graph_dct[x][y]<1000:
                #x_label = dct[x]['name']
                #y_label = dct[y]['name']
                dct[x]['degree'] += 1
                dct[y]['degree'] += 1
                
                res.append([x, y, graph_dct[x][y]])
    """
    for d in dct:
        if dct[d]['degree']>0:
            print("{}\t{}".format(dct[d]['name'],"X"))
    """
    
    #    filter out pairs
    res = [x for x in res if dct[x[0]]['degree']>1 or dct[x[1]]['degree']>1 ]
    #    replace ids with real names
    res = [[dct[x[0]]['name'], dct[x[1]]['name'], x[2]] for x in res]
    res = sorted(res, key=lambda x:x[-1])
    
    if outfile:
        csvfile = open(outfile, 'w', newline='', encoding="utf-8")
        csvwriter = csv.writer(csvfile, delimiter=DELIMITER,
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(['Source', 'Target', 'Weigth'])
        for r in res:
            csvwriter.writerow(r)
        csvfile.close()
        print("Graph written to {}".format(outfile))
    else:
        for r in res:
            print("{}, {}:\t{}".format(r[0],r[1],r[2]))


def getKey(label):
        st = label.lower()
        st = re.sub(r'[áàâ]','a',st)
        st = re.sub(r'[éèêë]','e',st)
        st = re.sub(r'[óòö]','e',st)
        st = re.sub(r'W','V',st)
        st = re.sub(r'w','v',st)
        return re.sub(r'[. ;:\'-]','',st)

def copyRow(row):
    row2=row.copy()
    del row2['name']
    return row2

def hashRow(row):
    return ''.join([row[d] for d in CONTEXT_IDS])


  
if __name__ == '__main__':
    main(sys.argv[1], 
         sys.argv[2] if len(sys.argv)>2 else None)

