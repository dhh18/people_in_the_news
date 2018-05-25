'''
Created on 24.5.2018

@author: petrileskinen
'''

import json
import re
import sys

#    PYTHONIOENCODING='utf-8' python3 extract_personnames.py json/korp.json 
 
def main(infile="json/korp.json"):
    
    with open(infile, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    res = []
    prev= ""
    
    for d2 in data['kwic']:
        
        for i,d in enumerate(d2['tokens']):
    
            if 'structs' in d and 'open' in d['structs']:
                arr = d['structs']['open']
                if 'ne_fulltype EnamexPrsHum' in arr:
                    st = [x for x in arr if 'ne_name ' in x][0]
                    m = re.match(r'ne_name (.*?)$', st)
                    st = m.group(1)
                    
                    #    check for I. J. Familyname
                    check = False
                    if i>0:
                        prev = d2['tokens'][i-1]
                        if 'lemma' in prev and re.match(r'^([A-ZÖÄÅ][.]|von|van|la)$', prev['lemma']):
                                #print("prev {}".format(prev))
                                st = "{} {}".format(prev['lemma'],st)
                                #print("found {}".format(st))
                                check = True
                                if i>1:
                                    prev = d2['tokens'][i-2]
                                    if 'lemma' in prev and re.match(r'^[A-ZÖÄÅ][.]$', prev['lemma']):
                                            #print("prev {}".format(prev))
                                            st = "{} {}".format(prev['lemma'],st)
                                            #print("found {}".format(st))
                                # print("before found {}".format(st))

                    #    check for Familyname, I.
                    if check == False and i+2<len(d2['tokens']):
                        nxt = d2['tokens'][i+1]
                        
                        #    read the comma
                        if 'lemma' in nxt and nxt['lemma']==",":
                            nxt = d2['tokens'][i+2]
                            
                            #    read initial after comma
                            if 'lemma' in nxt and re.match(r'^[A-ZÖÄÅ][.]$', nxt['lemma']):
                                st = "{} {}".format(nxt['lemma'], st)
                                
                                nxt = d2['tokens'][i+3]
                                #    read possible second initial after comma
                                if 'lemma' in nxt and re.match(r'^[A-ZÖÄÅ][.]$', nxt['lemma']):
                                    st = "{} {}".format(nxt['lemma'], st)
                                
                                # print("after found {}".format(st))
                    
                    if ' ' in st and (not re.match(r'^[A-ZÖÄÅ][.]*$', st)) and (not re.match(r'^[A-ZÖÄÅ][.]*\s[A-ZÖÄÅ][.]*$', st)):
                        res.append(st)
    
    for st in res:
        print('{}'.format(st))


if __name__ == '__main__':
    main(sys.argv[1])
    
    

