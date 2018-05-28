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
    
    #testXML()
    #return

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
                x_label = x # dct[x]['name']
                y_label = y # dct[y]['name']
                res.append([x_label,y_label, graph_dct[x][y]])
                
                dct[x]['check'] = True
                dct[y]['check'] = True
                
    
    res = sorted(res, key=lambda x:x[-1])

    dct = dict((d,dct[d]) for d in dct if 'check' in dct[d])

    xmlout = testXML(dct, res)
    if outfile:
        ofile = open(outfile, 'w', newline="", encoding="utf-8")
        ofile.write(xmlout)
        ofile.close()
        print("Output written to {}".format(outfile))
    else:
        print(xmlout)
    

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


def testXML(nodedict, edgelist):
    graphml = Element('graphml')
    
    graphml.append(Comment('property keys'))
    
    key0 = SubElement(graphml, 'key')
    
    key1 = SubElement(graphml, 'key')
        
    graph = SubElement(graphml, 'graph')
    
    graphml.append(Comment('graph keys'))
    
    data0 = SubElement(graphml, 'data')
    data1 = SubElement(graphml, 'data')
    data1.text=" "
    data1.text="1.0"
    #<data key="key0"></data>
    #<data key="key1">1.0</data>
   
    
    for e,p,v in [
            (graphml,   'xmlns',    "http://graphml.graphdrawing.org/xmlns"),
            (graphml,   'xmlns:xsi',"http://www.w3.org/2001/XMLSchema-instance"),
            (graphml,   'xsi:schemaLocation',"http://graphml.graphdrawing.org/xmlns http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd"),
            (key0,  'id', 'key0'),
            (key0,  'for', 'node'),
            (key0,  'attr.name', 'label'),
            (key0,  'attr.type', 'string'),
            
            # <key id="key1" for="edge" attr.name="weight" attr.type="float" />
            (key1,  'id', 'key1'),
            (key1,  'for', 'edge'),
            (key1,  'attr.name', 'weight'),
            (key1,  'attr.type', 'float'),
            
            # <graph id="G" edgedefault="undirected" parse.nodeids="canonical" parse.edgeids="canonical" parse.order="nodesfirst">
            (graph, 'id', 'G'),
            (graph, 'edgedefault',"undirected"),
            (graph, 'parse.nodeids',"canonical"), 
            (graph, 'parse.edgeids',"canonical"),
            (graph,  'parse.order',"nodesfirst"),
            
            (data0, 'key',"key0"),
            (data1, 'key',"key1")
            
        ]:
            e.set(p,v)
            
    graphml.append(Comment('vertices'))
    count = 0
    for v in nodedict:
        node = SubElement(graphml, 'node')
        data = SubElement(node, 'data')
        data.text = nodedict[v]['name']
        for e,p,v in [
            (node,   'id',   v),
            (data,  'key', 'key0')
            ]:
            e.set(p,v)
        count += 1
        #if count>10: break
    
    graphml.append(Comment('edges'))
    count=0
    print(edgelist)
    for i,e in enumerate(edgelist):
        #     <edge id="e0" source="n0" target="n1">
        #        <data key="key1">1.333</data>
        #    </edge>
        edge = SubElement(graphml, 'edge')
        data = SubElement(edge, 'data')
        data.text = str(float(e[-1]))
        for f,p,v in [
            (edge,   'id',   "e{}".format(i)),
            (edge,  'source', e[0]),
            (edge,  'target', e[1]),
            (data,  'key',  'key1')
            ]:
            f.set(p,v)
        count += 1
        # if count>10: break
        
    return prettify(graphml)

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

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
    
    

