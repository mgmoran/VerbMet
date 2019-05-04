import sys
import lxml.html
from lxml import etree
import nltk
import csv
from nltk import agreement
from nltk.metrics.agreement import AnnotationTask
from nltk.metrics import interval_distance, binary_distance, masi_distance

def AnnotationStats(a1,a2,a3):
        literal = 0
        nonliteral = 0
        exceptions = ["am", "are", "is", "were", "was", "been", "be", "being", "has", "have", "had", "do", "done", "compared", "aware","used","said", "overlap", "noted","think", "Performing","go","seems","uses","says","raising","appear","received","boost","reciting","reprove","responded","leave"]
        ### Annotator 1
        annotator1 = etree.parse(a1)
        ### all tags
        tags1 = list(annotator1.iter())
        verbs1 = [e for e in tags1 if e.tag=='VERB']
        for verb in verbs1:
            if verb.attrib['type']=='Literal':
                literal+=1
            else:
                nonliteral +=1
        args1 = [e for e in tags1 if e.tag=='ARG']
        mm1 = [e for e in tags1 if e.tag=='MISMATCH']
        with open('Annotator1.csv', 'w') as f:
            writer = csv.writer(f, delimiter=",")
            writer.writerow(("Verb","Type","Mismatched Args"))
            for e in verbs1:
                writer.writerow((e.attrib['text'],e.attrib['type'],[x.attrib['fromText'] for x in mm1 if int(x.attrib['toID'][1:])==int(e.attrib['id'][1:])]))
        f.close()
        ### shared tags
        shared1 = {e: (e.attrib['spans'].split('~'), e.attrib['text']) for e in tags1 if e.tag=='VERB' and int(e.attrib['id'][1:]) > 233 and e.attrib['text'] not in exceptions}
        shared1 = sorted(shared1, key= lambda x: shared1[x][0][0])
        verbids1 = [e.attrib['id'] for e in shared1]
        mismatches1 = [e for e in annotator1.iter() if e.tag=='MISMATCH']
        mismatches1 = [e for e in mismatches1 if e.attrib['toID'] in verbids1]

        ### Annotator 2
        annotator2 = etree.parse(a2)
        ### all tags
        tags2 = list(annotator2.iter())
        verbs2 = [tag for tag in tags2 if tag.tag == 'VERB']
        for verb in verbs2:
            if verb.attrib['type'] == 'Literal':
                literal += 1
            else:
                nonliteral += 1
        args2 = [tag for tag in tags2 if tag.tag == 'ARG']
        mm2 = [tag for tag in tags2 if tag.tag == 'MISMATCH']
        with open('Annotator2.csv', 'w') as f:
            writer = csv.writer(f, delimiter=",")
            writer.writerow(("Verb", "Type", "Mismatched Args"))
            for e in verbs2:
                writer.writerow((e.attrib['text'], e.attrib['type'], [x.attrib['fromText'] for x in mm2 if
                                                                      'toID' in x.attrib and int(x.attrib['toID'][1:]) == int(
                                                                          e.attrib['id'][1:])]))
        f.close()
        ### shared tags
        shared2 = {e: (e.attrib['spans'].split('~'), e.attrib['text']) for e in tags2 if e.tag == 'VERB' and int(e.attrib['id'][1:]) > 192 and e.attrib['text'] not in exceptions}
        shared2 = sorted(shared2, key=lambda x: shared2[x][0][0])
        verbids2 = [e.attrib['id'] for e in shared2]
        mismatches2 = [e for e in annotator2.iter() if e.tag == 'MISMATCH'  and 'toID' in e.attrib]

        ### Annotator 3
        annotator3 = etree.parse(a3)
        ### all tags
        tags3 = list(annotator3.iter())
        verbs3 = [tag for tag in tags3 if tag.tag == 'VERB']
        for verb in verbs3:
            if verb.attrib['type'] == 'Literal':
                literal += 1
            else:
                nonliteral += 1
        args3 = [tag for tag in tags3 if tag.tag == 'ARG']
        mm3 = [tag for tag in tags3 if tag.tag == 'MISMATCH']
        with open('Annotator3.csv', 'w') as f:
            writer = csv.writer(f, delimiter=",")
            writer.writerow(("Verb", "Type", "Mismatched Args"))
            for e in verbs3:
                writer.writerow((e.attrib['text'], e.attrib['type'], [x.attrib['fromText'] for x in mm3 if
                                                                      int(x.attrib['toID'][1:]) == int(
                                                                          e.attrib['id'][1:])]))
        f.close()
        shared3 = {e: (e.attrib['spans'].split('~'), e.attrib['text']) for e in tags3 if e.tag == 'VERB' and int(e.attrib['id'][1:]) > 235 and e.attrib['text'] not in exceptions}
        shared3 = sorted(shared3, key=lambda x: shared3[x][0][0])
        verbids3 = [e.attrib['id'] for e in shared3]
        mismatches3 = [e for e in annotator3.iter() if e.tag == 'MISMATCH']
        mismatches3 = [e for e in mismatches3 if e.attrib['toID']  in verbids3]


        ## Inter-Annotator Agreement
        verbentities = zip(shared1, shared2, shared3)
        tupls = []
        index = 0
        with open('IAACalculations.csv', 'w') as f:
            writer = csv.writer(f, delimiter=",")
            writer.writerow(("Verb","Annotator 1","Annotator 2","Annotator 3"))
            for e in verbentities:
                verb = e[0].attrib['text']
                type1 = e[0].attrib['type']
                type2 = e[1].attrib['type']
                type3 = e[2].attrib['type']
                tupls.extend( [ ('a1', frozenset([verb]),frozenset([type1])),  ('a2', frozenset([verb]),frozenset([type2])), ('a3', frozenset([verb]),frozenset([type3]))])
                writer.writerow( (e[0].attrib['text'],e[0].attrib['type'],e[1].attrib['type'],e[2].attrib['type'] ) )
                if type1=='Nonliteral' and type2=='Nonliteral'and type3=='Nonliteral':
                    mismatch1 = [x.attrib['fromText'] for x in mismatches1 if x.attrib['toID']== e[0].attrib['id']]
                    mismatch2 = [x.attrib['fromText'] for x in mismatches2 if x.attrib['toID'] == e[1].attrib['id']]
                    mismatch3 = [x.attrib['fromText'] for x in mismatches3 if x.attrib['toID'] == e[2].attrib['id']]
                    tupls.extend([('a1', frozenset([index]),frozenset(mismatch1)),('a2', frozenset([index]),frozenset(mismatch2)),('a3', frozenset([index]), frozenset(mismatch3))])
                    index +=1
                    writer.writerow( (e[0].attrib['text'], mismatch1, mismatch2, mismatch3))
        f.close()
        ### Calculating IAA
        t = agreement.AnnotationTask(data=tupls,distance=masi_distance)
        print("\nAnnotation Statistics")
        print("Literal tags: %d" %(literal))
        print("Nonliteral tags: %d\n" % (nonliteral))
        print("Agreement")
        print("Observed Agreement: %.2f" %(t.avg_Ao()))
        print("Alpha: %.2f" % (t.alpha()))
        print("S measure: %.2f" %(t.S()))
        print("Pi: %.2f" %(t.pi()))


if __name__ == "__main__":
    AnnotationStats('Annotator1Final.xml','Annotator2Final.xml','Annotator3Final.xml')