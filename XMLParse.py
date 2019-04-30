import sys
from bs4 import BeautifulSoup as Soup

def XMLParse(a1,a2,a3):
    annotator1 = open(a1,'r').read()
    annotator2 = open(a2,'r').read()
    annotator3 = open(a3,'r',).read()
    soup1 = Soup(annotator1)
    soup2 = Soup(annotator2)
    soup3 = Soup(annotator3)
    #Grabbing all verbs tagged by each annotator in the last 100 shared lines
    #For a given tag, you can access its attributes like so:
    #tag['id']
    #tag['text']
    #tag['spans']
    #same goes for whatever other attributes the other tags (ARG,MISMATCH) have.
    auxes = ["am","are","is","were","was","been","be","being","has","have","had","do","done"]
    a1tags = soup1.findAll(lambda tag: tag.name=="verb" and int(tag['id'][1:]) > 232 and tag['text'] not in auxes)
    a2tags = soup2.findAll(lambda tag: tag.name == "verb" and int(tag['id'][1:]) > 191 and tag['text'] not in auxes)
    a3tags = soup3.findAll(lambda tag: tag.name == "verb" and int(tag['id'][1:]) > 234 and tag['text'] not in auxes)
    a1mismatches = soup1.findAll(lambda tag: tag.name=="mismatch")


if __name__ == "__main__":
    XMLParse('Annotator1Final.txt.xml','Annotator2Final.txt.xml','Annotator3Final.xml')