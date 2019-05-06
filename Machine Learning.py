import numpy as np
from collections import defaultdict
from scipy import linalg
from sklearn.neighbors import KNeighborsClassifier
from nltk.tree import Tree
import csv
import xml.etree.ElementTree as ET
from nltk.corpus import propbank

google_dict = defaultdict()
literal_non_literal_vects = defaultdict()
non_literal_vects = defaultdict()
annotated_data = defaultdict(dict)

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
    pb_instances = propbank.instances()
    with open('VerbMetData - Master - VerbMetData Master.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count != 0:
                if row[2] == 'N':
                    sents[row[1]][int(row[3])] = row[4]
            line_count += 1
    for instance in pb_instances:
        for doc in sents:
            for sent in sents[doc]:
                if instance.fileid == doc and instance.sentnum == sent:
                        sentence_trees[sents[doc][sent]] = instance

def gettags(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    total_text = ''
    sentences = []
    for elem in root:
        lines = elem.text.splitlines()
        for line in lines:
            firstIndex = len(total_text)
            total_text += line + " "
            secondIndex = len(total_text)
            newSentence = SentenceSpan(line, firstIndex, secondIndex)
            sentences.append(newSentence)
    args = [elem for elem in root[1] if elem.tag == 'ARG']
    verbs = [elem for elem in root[1] if elem.tag == 'VERB']
    mismatches = [elem for elem in root[1] if elem.tag == 'MISMATCH']
    for sentence in sentences:
        for verb in verbs:
            start = int(verb.attrib['spans'].split('~')[0])
            end = int(verb.attrib['spans'].split('~')[1])
            if start >= sentence.starting and end <= sentence.ending:
                v = verb.attrib['text']
                type = verb.attrib['type']
                mm = [m.attrib['fromText'] for m in mismatches if
                      'toID' in m.attrib and int(m.attrib['toID'][1:]) == int(verb.attrib['id'][1:])]
                annotated_data[sentence.text][v] = (type, mm)

def read_in_google_vectors():
    google_list = []
    google_index = 0
    with open('GoogleNews-vectors-rcv_vocab.txt') as openfile:
        for line in openfile:
            data = line.split()
            google_dict[data[0]] = google_index
            google_index += 1
            mini_list = []
            for number in data[1:]:
                mini_list.append(float(number))
            google_list.append(mini_list)
    google_vect = np.array(google_list)
    return google_vect

    # Here a for-loop will be used to get the sentences containing each annotated verb, right now
    # it just prints out the starting index of the first verb and the sentence that it is in
def create_sentence_vectors(google_vect):
    for sentence in annotated_data:
        sentence_vector = np.zeros(3)
        word_list = []
        tree = sentence_trees[sentence].tree
        pred_pos = sentence_trees[sentence].predicate.treepos(tree)
        pred = str(tree[pred_pos])
        pred = pred[pred.index(" ") + 1:-1]
        word_list.append(pred)
        number_of_arguments = len(sentence_trees[sentence].arguments)
        if number_of_arguments > 3:
            number_of_arguments = 3
        for argument in sentence_trees[sentence].arguments[:number_of_arguments]:
            if (type(argument[0])) is 'nltk.corpus.reader.propbank.PropbankSplitTreePointer':
                argument[0] = argument[0][0]
            potential_argument = (tree[argument[0].treepos(tree)])
            string_rep = str(potential_argument.productions())
            if 'NN' in string_rep:
                noun_location = string_rep.rfind('NN')
                noun_location = (string_rep[noun_location:])
                noun_location = noun_location[7:]
                noun_location = noun_location[0:noun_location.index("'")]
            elif 'NNP' in string_rep:
                noun_location = string_rep.rfind('NNP')
                noun_location = (string_rep[noun_location:])
                noun_location = noun_location[7:]
                noun_location = noun_location[0:noun_location.index("'")]
            else:
                noun_location = 'asjdknfqjfbqlijbasfaejbkefalbjbhjjhlqelrhjb'
            word_list.append(noun_location)
        verb_vect = (google_vect[google_dict[pred]])
        number = 0
        for word in word_list[1:len(word_list)]:
            if word in google_dict:
                argument_vect = google_vect[google_dict[word]]
                cos = np.dot(verb_vect, argument_vect) / ((linalg.norm(verb_vect)) * linalg.norm(argument_vect))
                sentence_vector[number] = cos
                number += 1
            else:
                sentence_vector[number-1] = -1
                number += 1
        for number in range(len(word_list), 4):
            sentence_vector[number-1] = -1
        print(sentence_vector)


if __name__ == "__main__":

    create_sentences()
    gettags('Annotator1Final.xml')
    gettags('Annotator2Final.xml')
    gettags('Annotator3Final.xml')
    google_vect = read_in_google_vectors()
    create_sentence_vectors(google_vect)