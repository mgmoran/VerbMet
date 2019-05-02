import sys
from bs4 import BeautifulSoup as Soup
import lxml.html
from lxml import etree
import lxml.html.soupparser
import csv

def XMLParse(a1,a2,a3):
    with open('IAACalculations.csv','w') as f:
        ### Grabbing all shared verbs tagged in the last 100 lines
        writer = csv.writer(f,delimiter=",")
        exceptions = ["am", "are", "is", "were", "was", "been", "be", "being", "has", "have", "had", "do", "done", "compared", "aware","used","said", "overlap", "noted","think", "Performing","go","seems","uses","says","raising","appear","received","boost","reciting","reprove","responded","leave"]
        annotator1 = etree.parse(a1)
        tags1 = annotator1.iter()
        tags1 = {e: (e.attrib['spans'].split('~'), e.attrib['text']) for e in tags1 if e.tag=='VERB' and int(e.attrib['id'][1:]) > 233 and e.attrib['text'] not in exceptions}
        tags1 = sorted(tags1, key= lambda x: tags1[x][0][0])
        verbids1 = [e.attrib['id'] for e in tags1]
        mismatches1 = [e for e in annotator1.iter() if e.tag=='MISMATCH']
        for mismatch in mismatches1:
            print(mismatch.attrib['fromText'])
        mismatches1 = [e for e in mismatches1 if e.attrib['toID'] in verbids1]
        print(mismatches1)
        annotator2 = etree.parse(a2)
        tags2 = annotator2.iter()
        tags2 = {e: (e.attrib['spans'].split('~'), e.attrib['text']) for e in tags2 if e.tag == 'VERB' and int(e.attrib['id'][1:]) > 192 and e.attrib['text'] not in exceptions}
        tags2 = sorted(tags2, key=lambda x: tags2[x][0][0])
        verbids2 = [e.attrib['id'] for e in tags2]
        mismatches2 = [e for e in annotator2.iter() if e.tag == 'MISMATCH'  and 'toID' in e.attrib]
        #mismatches2 = [e for e in mismatches2 if e.attrib['toID'] in verbids2]
        #print(mismatches2)
        annotator3 = etree.parse(a3)
        tags3 = annotator3.iter()
        tags3 = {e: (e.attrib['spans'].split('~'), e.attrib['text']) for e in tags3 if e.tag == 'VERB' and int(e.attrib['id'][1:]) > 235 and e.attrib['text'] not in exceptions}
        tags3 = sorted(tags3, key=lambda x: tags3[x][0][0])
        verbids3 = [e.attrib['id'] for e in tags3]
        mismatches3 = [e for e in annotator3.iter() if e.tag == 'MISMATCH']
        mismatches3 = [e for e in mismatches3 if e.attrib['toID']  in verbids3]
        print(mismatches3)
        verbentities = zip(tags1,tags2,tags3)
        ## Creates a csv, "IAACalculations.csv"
        ##Column 1: Verb name
        ##Column 2: Annotator 1
        ##Column 3: Annotator 2
        ##Column 4: Annotator 3
        ##For each verb:
        ##Row 1: Type: Literal or Nonliteral
        ##Row 2: Mismatched argument, if one exists
        writer.writerow(("Verb","Annotator 1","Annotator 2","Annotator 3"))
        for e in verbentities:
            writer.writerow( (e[0].attrib['text'],e[0].attrib['type'],e[1].attrib['type'],e[2].attrib['type']))
            mismatch1 = [x.attrib['fromText'] for x in mismatches1 if x.attrib['toID']== e[0].attrib['id']]
            mismatch2 = [x.attrib['fromText'] for x in mismatches2 if x.attrib['toID'] == e[1].attrib['id']]
            mismatch3 = [x.attrib['fromText'] for x in mismatches3 if x.attrib['toID'] == e[2].attrib['id']]
            writer.writerow( (e[0].attrib['text'], mismatch1, mismatch2, mismatch3 ))

if __name__ == "__main__":
    XMLParse('Annotator1Final.xml','Annotator2Final.xml','Annotator3Final.xml')