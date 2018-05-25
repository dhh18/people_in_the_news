import wget, json, re, sys, os

def query(A, B):

    URL = 'https://korp.csc.fi/cgi-bin/korp.cgi?command=query&defaultcontext=1+sentence&show=sentence.ne_placename(._source)&show_struct=text_label.text_publ_(title.id).text_issue_(date.no.title).paragraph_id.text_(download_pdf_url.author.title.year).utterance_(id.participant.begin_time.end_time.duration.annex_link)&start=0&end=9999999&corpus=KLK_FI_' + A + '.REITTIDEMO&context=&incremental=true&cqp=%5B_.text_publ_id+%3D+"' + B + '"+%26+nertag+%3D+"EnamexLoc.*"%5D&defaultwithin=sentence'

    return URL


def open_paper_list(path):
    with open(path, "r", encoding="utf-8") as f:
        return  [x.replace("\n", "") for x in f]

if __name__ == "__main__":
	papers = open_paper_list(sys.argv[1])
	years = [int(x) for x in re.split("-", sys.argv[2])]
	
	for paper in papers:
		for year in range(years[0], years[1]):
			year = str(year)
			year_path = "data/"+year
			res_path = year_path+"/"+paper+".json"
			if not os.path.exists(year_path):
				os.mkdir(year_path)

			url = query(year, paper)
			wget.download(url, out=res_path)


