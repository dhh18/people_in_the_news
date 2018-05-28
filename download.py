import json, re, sys, os
import wget

def query(A, B, C, D):

    URL = 'https://korp.csc.fi/cgi-bin/korp.cgi?command=query&'
    URL += 'defaultcontext=1+'+D+'&'
    URL += 'show=paragraph.lemma(.comp).msd.ne_(name.ex.type.subtype.fulltype).ne_placename(._source).ner(tag.bio)&'
    URL += 'show_struct=text_publ_id.text_issue_date.sentence_id.paragraph_id&'
    URL += 'cache=true&'
    URL += 'start=0&end=50000&'
    URL += 'corpus=KLK_FI_'+B+'&'
    URL += 'context=&'
    URL += 'incremental=true&'
    URL += 'cqp=%5Bnertag+%3D+%22Enamex'+C+'.*%22+%26+_.text_publ_id+%3D+"' +A+'"%5D&'
    URL += 'defaultwithin=sentence&'
    URL += 'within=&'
    URL += 'loginfo=lang%3Den+search%3Dadv'

    return URL

#cqp=%5B_.text_publ_id+%3D+"0013-6522"+%26+nertag+%3D+"EnamexLoc.*"%5D

def open_paper_list(path):
    with open(path, "r", encoding="utf-8") as f:
        return  [x.replace("\n", "") for x in f]

if __name__ == "__main__":

    #command line arguments:
    # 1. path to file containing list issn codes
    # 2. year interval to be searched in form eg. 1870-1875
    # 3. name type, "Prs" for people, "Loc" for place
    # 4. context: "sentence", "paragraph" or "none"
    
    papers = open_paper_list(sys.argv[1])
    years = [int(x) for x in re.split("-", sys.argv[2])]
    name_type = sys.argv[3]
    context = sys.argv[4]
    if context == "none":
        context = ""
    print(papers, years, name_type)
    for paper in papers:
        for year in range(years[0], years[1]):
            year = str(year)
            year_path = "../data/"+year
            res_path = year_path+"/"+paper+"_"+name_type+".json"
            if not os.path.exists(year_path):
                os.mkdir(year_path)

            url = query(paper, year, name_type, context)
            print(url)
            wget.download(url, out=res_path)

        


