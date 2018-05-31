#!/usr/bin/env python
# coding: utf-8

import csv
from collections import OrderedDict
import glob
import json
import re
import requests
import numpy as np

infolder = "kb_csv2/*.csv"
outfilename = "person_mentions_by_category.csv"
outfolder = "kb_ages"

def main():
    
    kb_dct = readSNB()
    files = glob.glob(infolder)
    hgram = {}
    pcount = {}
    
    for file in files:
        label, byear, dyear = extractYears(file)
        if label:
            key = simplify(label)
            categories = ['kaikki']
            if key in kb_dct:
                categories += re.split(r'(?<=[^-]);\s',kb_dct[key]['categories'])
                for c in categories:
                    if not c in hgram:
                        hgram[c]= [0]*100
                    if not c in pcount:
                        pcount[c] = 0
                if 'musiikki' in categories:
                    #print("{} {}".format(label,dyear-byear))
                    pass
            else:
                #print("Not found {}\t{}".format(label,simplify(label)))
                pass
            with open(file, newline='', encoding="utf-8") as csvfile:
                csvreader = csv.DictReader(csvfile, delimiter='\t', quotechar='|')
                fields = csvreader.fieldnames
                for row in csvreader:
                    year = int(row['year'])
                    age = year - byear
                    for c in categories:
                        hgram[c][age] += int(row['count'])
                for c in categories:
                    pcount[c] += 1
    # print(hgram)
    with open(outfilename, 'w', newline='', encoding="utf-8") as csvfile:
        csvwriter = csv.writer(csvfile, delimiter='\t',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(["category","people","5percentile","mean","95percentile"])
        for cat in hgram:
            gram = hgram[cat]
            #print("Category {}".format(cat))
            #print("Number of people {}".format(pcount[cat]))
            
            while gram[-1]==0 and len(gram)>1:
                del gram[-1]
                
            p05= getPercentile(gram, p=0.05)
            #print("5% percentile: {}".format(p05))
            
            p50= getPercentile(gram, p=0.5)
            #print("mean: {}".format(p50))
            
            p95= getPercentile(gram, p=0.95)
            #print("95% percentile: {}".format(p95))
            
            csvwriter.writerow([cat, pcount[cat], p05,p50,p95])
            
            
            with open("{}/{}.csv".format(outfolder,cat), 'w', newline='', encoding="utf-8") as csvfile2:
                csvwriter2 = csv.writer(csvfile2, delimiter='\t',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
                csvwriter2.writerow(["age","count"])
                
                for age,count in enumerate(gram):
                    rowout = [age, count]
                    csvwriter2.writerow(rowout)
    print("Written to {}".format(outfilename))



def extractYears(st):
    st = st.split('/')[-1]
    m=re.match(r'([^(]+)\((\d+)-(\d+)\)',st)
    if m:
        return m.group(1).strip(), int(m.group(2)), int(m.group(3))
    return None,None,None
    
    
def getPercentile(arr, p=0.5):
    carr=np.cumsum(arr)
    carr=carr/carr[-1]
    return np.count_nonzero(carr/carr[-1]<p)
    
def readSNB(infile='KBlist1830_1910.csv'):
    dct={}
    with open(infile, newline='', encoding="utf-8") as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter='\t', quotechar='|')
        fields = csvreader.fieldnames
        for row in csvreader:
            key = simplify((row['familyName']+row['givenName']))
            dct[key] = row
    
    return dct 

def simplify(st):
    
    st = re.sub(r'[Åáàâäå]','a',st)
    st = re.sub(r'[Öóòöô]','o',st)
    st = re.sub(r'[éèëê]','e',st)
    
    st = re.sub(r'\s','',st.lower())
    return re.sub(r'[^a-z]','', st)

def extractYear(st):
    m=re.match('[^/]+/(\S+) .*? \d*\.*\d*\.*(\d\d\d\d)$',st)
    if m:
        return m.group(1), int(m.group(2))
    return None, None
    

if __name__ == '__main__':
    main()


"""
gummerushermanerik
st_hlberggeorgiusgeorgii
sommerarthur
stenb_cklydia
uotilaaukusti
h_llstr_maxelgabriel
frosterusaugustjohan
f_rdigfranshjalmar
sohlmanjohangustaf
huberrobert
chydeniusemilia
_hbergviktorwilhelm
hagmansofia
hagelintobias
svanjohanedvard
sl__rkaarlo
sj_str_mfrans
johanssonjonatan
bj_rkmancharlotte
vonbrandenburgalexander
haapanenjaakko
rennerfeltrobertmauritzcecil
lylyjulius
erkkojohanhenrik
procop_viktornapoleon
munckaffulkilaalexander
vonnumershedvig
berghhanna
malmotto
kallioisakwilhelm
juseliusjakob
hackzellabrahamwilhelm
keckmanjohanalfred
yrj__koskinengeorgzacharias
inberghermanmauritz
nordenswanvictorine
forsmanfredrik
gestrinemilteodor
synnerberggeorgfredrikalexander
sederholmtheodor
parviainenjohan
holmstr_mnils
gyllenb_gelanderswilhelmleonard
alfthanjohannes
aspisa
hallonbladelisabeth
forbuskarladolf
nikolaialeksandrovitsh
brummerkarlmagnusemil
rosenlewwilhelm
aureniusaugustwilhelm
lundbeckhaquinus
forselljohanalfred
vonbrandenburgnikolai
castr_nrobert
lindholmkalle
gyld_nhugo
petandertiodolfjulius
herckmangustafernfrid
kalinenjohannestor
ellersedvard
r_berghgustafwilhelm
h_rm_l_ottoedvard
n_rhiotto
forsmanjaakko
kulhanennatanael
heinriciusivar
edelheimanna
vonschantzjohanfredrik
liljelundarvid
leinbergkarlgabriel
knorringgustafchristian
vonhaartmanhedvig
ekelundconstance
konsinviktoraugust
kauppilagustafhenrik
aspgeorg
vontroilsamuelwerner
svertschkoffisidor
h_glundgustaf
petterssonerikviktor
palinhjalmargeorg
bergbomkaarlo
hertzbergrafael
fleegeaxelaugustabraham
str_mborgjohanelias
raa_winterhjelmhedvigcharlotte
renlundkarlherman
schleussnerjohanrichardalfred
s_derhjelmwoldemar
hellst_nviktormagnus
stenbergerland
lemstr_mselim
hallikainenottoberndt
forseliusvictor
forssjohanantonimmanuel
jernstr_mjohannes
falkmanseverin
ichtydiusjacobusmatthiae
forsiusnicolauslaurentii
mattilajuhoheikkijuhonpoika
janssonkarlemanuel
synnerbergkonstantin
kekonifransoskar
lagerborgrobert
huhtinenkarlhenrik
krohnleopold
heikelmatiashenrik
neoviusfrithiof
granqvistjohanedvard
korsstr_mjohanevert
kivialeksis
j_rnefeltalexander
berndtsongunnar
salmelaineneero
palm_nfanny
vonhaartmanvictor
boldtjohandidrik
bergiuspetrusandreae
k_mpcarl
kontiosakari
mansnerhugoevald
tavaststjernakarlaugust
holmstr_mjohannes
langenski_ldnikolaiteodoralbrekt
procop_oskar
saxbergherman
flodinhilda
packal_nnilskristian
sj_rosjuho
heikkinenantti
savanderalexandra
grenqvistchristiangustaf
silfverbergida
soisalon_soinineneliel
kramsukaarlo
alipi
kailaaarne
jernstr_mcarlgustafalarik
gr_nbergkarlgustaf
hinkulamatts
holstludvig
neiglickhjalmar
heikelanna
fabritiusgustafedvin
gauffinkarljohan
gr_ndahlerikjohan
vilhooskari
mall_nreinholdwilliam
gripenbergjohannes
gummeruskarljakob
mielckernst
koponenabel
castr_nnatalia
jus_liusferdinand
vonwulffertmikaelgustafkonstantin
tudeerstencarl
schrammalexanderrostislav
vonbeckeradolf
aflindforsjakobjulius
rennerfeltselimideon
ongelinhanna
oppenheimmejer
karstenklasedvin
bergjohanalexander
andelincarloskarevert
aleksanteriiii
toppeliusmeri
edelfeltalbert
hellst_nakselaugust
blomqvistantongabriel
gr_nholmoskar
hagmanaugust
vonkothengustafaxel
avellancarlaxel
stjernvallgustavalexanderrobert
gottlebenjohanedvard
schulmancarlfredrik
weckmannilshenrikagaton
jahnssonevaldferdinand
hannulaherman
stigellrobert
t_rnuddgustaf
mendtedvardgeorgalexander
wallinolai
peranderfrithiof
sj_roskarlkristian
donnerotto
borgstr_mhenrik
hanneliusoskaraugust
vondaehnwoldemar
karstenerlandaugust
hasselgr_nerikgustaf
cronstedtjean
canthminna
montgomeryrobert
forstadiusalexanderwilhelm
brofeldtmortimer
bobrikovnikolaiivanovitsh
hellsberghermanludvig
melaaukustijuhana
knorringnikolaijohanferdinand
segercrantzcarlnapoleon
wetterhoffkarl
groundstroemfredrikoskar
steniusm_rtengabriel
ahlstedtfredrik
wegeliusmartin
lins_nmathilda
hjerpehegesippushippolytus
kivek_slauri
dunckerelis
kruegeradalbert
kinnunenmikael
ignatiuskarlferdinand
j_rnefeltaugustalexander
vonheidekencarljohan
frasaalina
vonschoultzkarllorenzadalbert
savanderrobertsalomon
b_ckjohannes
fromjohanwilhelm
krohnjulius
kyyni_augusthjalmar
forst_nlennartalfons
krankisakwilhelm
grundstr_mgeorg
l_fgrenviktor
malmgrenandersjohan
vonammondtedvardreinhold
geitlinjohangabriel
hultragnar
acht_lorenz
hammar_nlarsjohan
vonchristiersonlouise
kjellbergjosefverner
fagergustafemil
_str_mkarlrobert
t_rm_nenedvard
hougbergandersjohan
jus_liussigrid
rosl_fkustaa
procop_victornapoleon
sinebrychoffanna
larinparaske
kullaaleksander
colliandercarlviktorolivier
heleniusmatias
silfversvanalexanderjulius
forsblomandersgustaf
mexmontanfrans
meinanderludvig
henrikssonberndtjohan
kiviojaabel
rydzeffskythaddeusgeorgleonard
bergbomemilie
renvaldkonstantin
istoeetu
granrothaugustalexander
kotilainenmatiasfredrik
vannovskipjotrsemjonovitsh
malmstr_mkarlrobert
forsmanalina
ekmananders
weckmananna
aminoffjohanfredrikgustaf
fabritiusoskarhjalmarwaldemar
nystr_mhilda
konkolaseverus
weurlanderfridolf
havukainenmikko
kuitunenhiskias
lond_nludvig
lindbergsextusotto
tennbergadolffredrik
kurt_njoachim
kekonihenrik
vonrechenbergnikolai
karttunenkarl
ahlstedtnina
harlinernstrobert
suppanenaatto
riihim_kijuho
afenehjelmkurtfredrikleonard
grenqvistviktorreinholdleopold
johanssonwilhelm
forsellnikolaiheribert
huttunenpekka
grotenfeltnils
holmbergwerner
tawaststjernabrorleonardmagnusedvard
erkkoelias
vonplehwevjatsheslavkonstantinovitsh
h_llforsjohanaugust
j_rnefeltklaserik
kauffmannhermann
ramsayallangeorg
kuhlbergjohanwladimiralexander
jalavaantti
heikkil_andersgustaf
sp_rehenrikaugustvilhelm
_str_mhemming
ehrnroothadolfreinholdviktor
vendellherman
enebergwaldemar
langjoelnapoleon
castr_nkaarlealfred
johnssonjohanviktor
afschult_nmaximuswidekind
meinandernicolauspetrus
k_rkihenrikfabian
b_hrludwig
bergrothelis
henrikssonkarljohan
holmstr_maugust
hakkarainendavid
linderconstantin
enebergkarlfredrik
lindermarie
ramsayarchibaldviktor
borgstr_mleonard
rahkonenaleksanteri
lovenetzskijohanedgarmikael
fabritiusernst
aflindforsjulius
munsterhjelmhjalmar
jaakkolamatiasviktorinus
ikonenalexander
gyllenb_gelkarljohan
estlanderjakobaugust
vonschantzfilip
hellmanhilda
fagerlundbroremil
karikaarlokustaa
weckselljosefjulius
nordenski_ldadolferik
bromsanna
asphilda
saarelaalbertina
heininenjohan
s_derlundjohanwilhelm
vonkonowevertbrynolf
haraldpekka
brotherusalexandervalerian
haapojamatti
hirnkarldavidaxel
kyyhkynenjuho
johanssonelieser
schaumaneugen
alceniusmariacharlotta
beckerwaldemar
kajanderwilhelm
r_nnb_ckernst
lindeb_ckalexandermaximilian
h_gglundadolf
neoviusfritiofalfred
hirvinensalomon
hulkkonenniilo
hofstr_mkarlarndt
vonkothenfredrikoskarteodor
st_hlberghedvig
wetterhofffredrika
lekveendre
takanenjohannes
j_rvinennestor
aureniusnikolai
vonwrightmagnus
boxstr_manders
caloniusemilwilhelmmatias
h_nninenjohannes
henrikssonberndtrobert
hollmingfransvictor
hell_npauljohan
churbergfanny
fagerlundaugustviktor
hasselblattalexanderfridolf
forssellernstalbert
lavoniuswilhelm
chydeniusandersherman
koskikarlaxeladhemar
inbergfransbernhard
hiortaforn_scarlgustaf
sulinkarlwilhelm
hjeltalma
vonhertzenkarl
t_rneroosantti
vonetternikolaipaulkarl
serlachiusgustafadolf
antellhermanfrithiof
ordinkesarfilippovitsh
sundstr_mhans
neoviustomasfredrikbruno
hagelbergkarledvard
suomalainensamuli
andreaspetri
gestrinreinholdteodor
gripenbergcarlgustafcasimir
mellerida
salomaaaliina
krohnkarlgustaf
kaitilawilhelm
suuronenphilip
kurt_noskarludvig
skogmandavid
degeercarlwilhelmconstantin
carlssonwilhelm
johanssonjosua
heinemannkarl
hild_naugust
suutarlazefanias
idmankarljohan
hyrkstedtkarlaxel
haus_nkarljulius
hartmanjohannessakari
ingmanjonathan
hellmanalba
dippellwilhelm
gaddottoviktorinus
linderernst
"""
