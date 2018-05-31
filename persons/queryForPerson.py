#!/usr/bin/env python
# coding: utf-8

import csv
from collections import OrderedDict
import json
import re
import requests
import numpy as np

infile = "KBlist1830_1910.csv"
def main():
    count = 0
    with open(infile, newline='', encoding="utf-8") as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter='\t', quotechar='|')
        fields = csvreader.fieldnames
        
        for row in csvreader:
            try:
                familyName = row['familyName']
                givenNames = row['givenName']
                birthYear = int(row['birthDate'][:4])
                deathYear = int(row['deathDate'][:4])
                outfile = "kb_csv2/{} {} ({}-{}).csv".format(familyName, 
                                                            givenNames,
                                                            birthYear,
                                                            deathYear)
                makeQuery(givenNames, familyName, deathYear, outfile)
            
            except Exception as e:
                
                pass
                
    
def makeQuery(givenNames,familyName, deathYear, outfilename):
    
    endpoint="https://korp.csc.fi/cgi-bin/korp.cgi"
    
    fullname = "{} {}".format(givenNames, familyName)
    cqp = ' '.join(['[word = "{}"]'.format(s) for s in fullname.split()])
    
    years = list(range(1850,deathYear+1))
    corpus = 'KLK_FI_({})'.format('.'.join([str(y) for y in years]))
    data = {
        'command':'count',
        'groupby':'lemma,text_publ_id,text_issue_date',
        'corpus': corpus,
        'incremental':'true',
        'cqp': cqp,
        'defaultwithin':'sentence',
        'loginfo':'lang=fi+search=adv',
        'within':'',
        'split':'',
        'top':''
    }

    try:
        r = requests.post(endpoint,
                      data = data)
    except Exception as e:
        raise e
    
    dct = OrderedDict([(y,0) for y in list(range(1850,1910))])
    
    cont = json.loads(r.text)
    dta = cont['total']['absolute']
    for x in dta:
        issn, year = extractYear(x)
        if year in dct:
            val = int(dta[x])
            dct[year] += val
    
    total = sum([dct[x] for x in dct])
    # print(dct)
    print("Total {} for {} {}".format(total, givenNames, familyName))
    
    if total<1: return
    with open(outfilename, 'w', newline='', encoding="utf-8") as csvfile:
        csvwriter = csv.writer(csvfile, delimiter='\t',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(["year","count"])
        
        for x in dct:
            rowout = [x, dct[x]]
            csvwriter.writerow(rowout)
    print("Written to {}".format(outfilename))
    

def extractYear(st):
    m=re.match('[^/]+/(\S+) .*? \d*\.*\d*\.*(\d\d\d\d)$',st)
    if m:
        return m.group(1), int(m.group(2))
    return None, None
    

if __name__ == '__main__':
    main()
    
"""
https://korp.csc.fi/cgi-bin/korp.cgi?command=count&groupby=lemma%2Ctext_publ_id%2Ctext_issue_date&corpus=KLK_FI_18(99.98.97.96.95.94.93.92.91.90.89.88.87.86.85.84.83.82.81.80.79.78.77.76.75.74.73.72.71.70.69.68.67.66.65.64.63.62.61.60.59.58.57.56.55.54.53.52.51.50)&incremental=true&cqp=%5Bword+%3D+%22Sebastian%22%5D+%5Bword+%3D+%22Gripenberg%22%5D&defaultwithin=sentence&within=&split=&top=&loginfo=lang%3Dfi+search%3Dadv
"""
