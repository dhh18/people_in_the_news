'''
Created on 24.5.2018

@author: petrileskinen
'''
import csv
import glob
import json
import re
import sys

#    PYTHONIOENCODING="utf-8" python3 extract_personnames_folder.py "data/*/*.json" persons/csv/Valvoja/
#    PYTHONIOENCODING='utf-8' python3 extract_personnames.py json/korp.json 

def main(infolder="data/*/*.json", outfolder=None):
    
    if not '*' in infolder:
        infolder = infolder + '*'
    
    files = glob.glob(infolder)
    
    for file in files:
        
        print("Reading {}".format(file))
        f = file.split('/')[-1]
        
        if outfolder[-1] != "/":
            outfolder += "/"
        
        outfile = outfolder+f
        outfile = file.replace('data/','persons/csv/Valvoja/')
        outfile = outfile.replace('.json','.csv')
        
        handleFile(file, outfile)
        print("Written to {}".format(outfile))
    
def handleFile(infile, outfile):
    with open(infile, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    res = []
    prev= ""
    counts = [0,0]
    if outfile:
        csvfile = open(outfile, 'w', encoding="utf-8")
        csvwriter = csv.writer(csvfile, delimiter='\t',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(['name', 'sentence_id', 'paragraph_id', 'text_issue_date', 'text_publ_id'])
    
    for d2 in data['kwic']:
        #print(d2.keys())
        publication_arr = [d2['structs'][x] for x in ['sentence_id', 'paragraph_id', 'text_issue_date', 'text_publ_id']]
        
        for i,d in enumerate(d2['tokens']):
            
            if 'structs' in d and 'open' in d['structs']:
            
                arr = d['structs']['open']
                if 'ne_fulltype EnamexPrsHum' in arr:
                    st = [x for x in arr if 'ne_name ' in x][0]
                    m = re.match(r'ne_name (.*?)$', st)
                    st = m.group(1)
                    counts[0] += 1
                    
                    if ' ' in st and (not re.match(r'^[A-ZÖÄÅ][.]*$', st)) and (not re.match(r'^[A-ZÖÄÅ][.]*\s[A-ZÖÄÅ][.]*$', st)):
                        res.append(st)
                        if outfile:
                            csvwriter.writerow([st]+ publication_arr)
                    else:
                        # print('Filtered {}'.format(st))
                        counts[1] += 1
    """
    # order so full names appear first
    res = sorted(res, key=lambda x:x.count('.'))

    dct = {}
    for st in res:
        prs = Person(st)
        for key in prs.keys:
            if not key in dct:
                dct[key] = prs
            #else:
            #    print("Matching {}".format(prs))
            #   print("Already {}".format(dct[key]))
    
    # dictionary to set
    lst = sorted(list(set(dct.values())))
    
    for prs in lst:
        print(prs)
    """
    print('Total entries {}'.format(counts[0]))
    print('Filtered entries {}'.format(counts[1]))
    # print('Total person {}'.format(len(lst)))

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
    
    

