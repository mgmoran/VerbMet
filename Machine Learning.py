import numpy as np
from collections import defaultdict
import scipy.linalg as scipy_linalg
from nltk.corpus import treebank
from nltk.tree import Tree
import csv
import xml.etree.ElementTree as ET

# A dictionary of dictionaries where the first key is the document name, the second key is the sentence index, and
# the value is the sentence itself
# E.g. {'wallstreetjournalblahblah': 0: 'This is sentence 0 in the document'}
sents = defaultdict(lambda : defaultdict())

# A dictionary mapping each sentence as a string to its parse tree
# E.g. {'This is a sentence': (S ( NP This is ) ( VP its parse tree ) ) }
sentence_trees = defaultdict(lambda : Tree)

# Class defining SentenceSpan objects that have fields for the sentence in a document,
# the starting index of the sentence in the document, and the ending index of the sentence in the document
class SentenceSpan():
    def __init__(self, text, starting, ending):
        self.text = text
        self.starting = starting
        self.ending = ending

# Creates and initialized the sents dictionary of dictionaries as well as the sentence_trees dictionary
# Right now only uses the sentences that were not shared by annotators, can be edited depending on how we want
# to create our test sets
def create_sentences():
    with open('VerbMetData - Master - VerbMetData Master.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count != 0:
                if row[2] == 'N':
                    sents[row[1]][int(row[3])] = row[4]
            line_count += 1
    for doc in sents:
        for sent in sents[doc]:
            sentence_trees[sents[doc][sent]] = treebank.parsed_sents(doc)[sent]


if __name__ == "__main__":
    create_sentences()

    # Here is where each annotators XML file can be parsed, right now this is just Annotator 2's
    tree = ET.parse('Annotator2Final.xml')
    root = tree.getroot()
    total_text = ''
    # Create a list of SentenceSpan objects for the annotator
    sentences = []
    for elem in root:
        lines = elem.text.splitlines()
        for line in lines:
            firstIndex = len(total_text)
            total_text += line
            secondIndex = len(total_text)
            newSentence = SentenceSpan(line, firstIndex, secondIndex)
            sentences.append(newSentence)

    # Here a for-loop will be used to get the sentences containing each annotated verb, right now
    # it just prints out the starting index of the first verb and the sentence that it is in
    number = int(root[1][0].attrib['spans'][0:root[1][0].attrib['spans'].index('~')])
    print(number)
    for sentence in sentences:
        if sentence.starting <= number and sentence.ending >= number:
            print(sentence.text)

