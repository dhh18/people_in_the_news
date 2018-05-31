#!/usr/bin/env python
# coding: utf-8

import csv
import json
import requests

def main():
    outfile = "KBlist1830_1910.csv"
    
    #    shortcut for query: http://yasgui.org/short/rk37HaTvf
    query = """
 PREFIX owl: <http://www.w3.org/2002/07/owl#>  
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>  PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>  
PREFIX schema: <http://schema.org/>  
PREFIX dct: <http://purl.org/dc/terms/>  
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>  PREFIX skosxl: <http://www.w3.org/2008/05/skos-xl#>  
PREFIX xml: <http://www.w3.org/XML/1998/namespace>  
PREFIX bioc: <http://ldf.fi/schema/bioc/>  
PREFIX nbf: <http://ldf.fi/nbf/>  
PREFIX categories:    <http://ldf.fi/nbf/categories/>  PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>  PREFIX foaf: <http://xmlns.com/foaf/0.1/>  
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>  
PREFIX gvp:    <http://vocab.getty.edu/ontology#> 

SELECT DISTINCT ?id ?link ?familyName ?givenName ?gender ?birthDate ?birthPlace ?deathDate ?deathPlace  (group_concat(?category;separator="; ") as ?categories) 
WHERE {  
  ?id a nbf:PersonConcept ;
      foaf:focus ?prs ;
      skosxl:prefLabel ?plabel .
  FILTER (NOT EXISTS {?id owl:sameAs []})
  OPTIONAL { ?plabel schema:familyName ?familyName }
  OPTIONAL { ?plabel schema:givenName ?givenName }
  
  ?prs schema:gender/skos:prefLabel ?gender ;
        ^crm:P98_brought_into_life ?bir .
   OPTIONAL { ?bir nbf:place ?birthPlace . filter (isliteral(?birthPlace)) }               
          ?bir nbf:time/gvp:estStart ?birthDate . 
  
    OPTIONAL { ?prs ^crm:P100_was_death_of ?dea .
      OPTIONAL { ?dea nbf:time/gvp:estStart ?deathDate . }        
      OPTIONAL { ?dea nbf:place ?deathPlace . filter (isliteral(?deathPlace)) }        
    }                     
  FILTER ("1830-01-01"<=STR(?birthDate) && STR(?deathDate)<"1910-01-01")
    OPTIONAL { ?prs nbf:has_category/skos:prefLabel ?category . }
      OPTIONAL { ?id schema:relatedLink ?link . }
} GROUP BY ?id ?familyName ?givenName ?gender ?birthDate ?birthPlace ?deathDate ?deathPlace ?link ORDER BY ?birthDate ?familyName ?givenName   """
    
    endpoint = "http://ldf.fi/nbf/sparql"
    
    arr = makeSparqlQuery(query, endpoint)
    fields = [
        "id", 
        "familyName",
        "givenName",
        "gender",
        "birthDate", 
        "birthPlace", 
        "deathDate", 
        "deathPlace", 
        "categories",
        "link" 
        ]
    print("Query ready.")
    
    with open(outfile, 'w', newline='', encoding="utf-8") as csvfile:
        csvwriter = csv.writer(csvfile, delimiter='\t',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(fields)
        
        for row in arr:
            rowout = [row[f] if f in row else "" for f in fields]
            csvwriter.writerow(rowout)
            # print(', '.join(['"{}"'.format(p) for p in row]))
            # return
    print("{} results written to {}".format(len(arr),outfile))
    
def makeSparqlQuery(query, endpoint="http://ldf.fi/nbf/sparql"):
    
    try:
        r = requests.post(endpoint,
                      data = {'query': query, 'format': 'json'},
                      headers = dict({'Accept': 'application/sparql-results+json',
                                      'Authorization':"Basic c2Vjbzpsb2dvczAz" 
                                     }))
        cont = json.loads(r.text)
        fields = cont['head']['vars']
        
        bind = cont['results']['bindings']
        res = []
        for x in bind:
            row = {}
            for f in fields:
                if f in x and 'value' in x[f] and x[f]['value'] != "":
                    row[f] = x[f]['value']
            res.append(row)
        return  res
    except Exception as e:
        # KeyError: no result
        raise e
    return []


    

if __name__ == '__main__':
    main()
    
"""
https://korp.csc.fi/cgi-bin/korp.cgi?command=count&groupby=lemma%2Ctext_publ_id%2Ctext_issue_date&corpus=KLK_FI_18(99.98.97.96.95.94.93.92.91.90.89.88.87.86.85.84.83.82.81.80.79.78.77.76.75.74.73.72.71.70.69.68.67.66.65.64.63.62.61.60.59.58.57.56.55.54.53.52.51.50)&incremental=true&cqp=%5Bword+%3D+%22Sebastian%22%5D+%5Bword+%3D+%22Gripenberg%22%5D&defaultwithin=sentence&within=&split=&top=&loginfo=lang%3Dfi+search%3Dadv
"""
