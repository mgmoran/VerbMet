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
annotated_data = defaultdict(lambda: defaultdict())
verbdict = defaultdict(lambda: defaultdict(int))
training_X = []
training_Y = []
testing_X = []
testing_Y = []

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
                arguments = list(
                    set([(arg.attrib['text'], arg.attrib['type']) for arg in args if arg.attrib['text'] in mm]))
                annotated_data[sentence.text][v] = (type, arguments)
    for sentence in annotated_data:
        for v in annotated_data[sentence]:
            if annotated_data[sentence][v][0] == 'Nonliteral':
                for arg in [arg[1] for arg in annotated_data[sentence][v][1]]:
                    verbdict[v][arg] += 1

# Read in the data from the Google vectors .txt file
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

# Create the sentence vectors for each sentence in the training data
def create_sentence_vectors(google_vect):
    train_X_var = 1
    train_Y_var = 1
    for sentence in annotated_data:
        sentence_vector = np.zeros(3)
        word_list = []
        should_be_instance = str(type(sentence_trees[sentence]))
        if should_be_instance == "<class 'nltk.corpus.reader.propbank.PropbankInstance'>":
            tree = sentence_trees[sentence].tree
            tree_type = str(type(sentence_trees[sentence].predicate))
            if tree_type == "<class 'nltk.corpus.reader.propbank.PropbankSplitTreePointer'>" or tree_type == "<class 'nltk.corpus.reader.propbank.PropbankChainTreePointer'>":
                pred_pos = sentence_trees[sentence].predicate.pieces[0].treepos(tree)
            else:
                pred_pos = sentence_trees[sentence].predicate.treepos(tree)
            pred = str(tree[pred_pos])
            pred = pred[pred.index(" ") + 1:-1]
            word_list.append(pred)
            number_of_arguments = len(sentence_trees[sentence].arguments)
            if number_of_arguments > 3:
                number_of_arguments = 3
            for argument in sentence_trees[sentence].arguments[:number_of_arguments]:
                potential = argument[0]
                argument_type = str(type(argument[0]))
                while argument_type == "<class 'nltk.corpus.reader.propbank.PropbankSplitTreePointer'>" or argument_type == "<class 'nltk.corpus.reader.propbank.PropbankChainTreePointer'>":
                    potential = potential.pieces[0]
                    argument_type = str(type(potential))
                potential_argument = (tree[potential.treepos(tree)])
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
            if pred in google_dict:
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
                if train_X_var % 3 != 0:
                    training_X.append(sentence_vector)
                    train_X_var += 1
                else:
                    testing_X.append(sentence_vector)
                    train_X_var += 1
                for tag in annotated_data[sentence]:
                    lit_non_lit = annotated_data[sentence][tag][0]
                    if train_Y_var % 3 != 0:
                        training_Y.append(lit_non_lit)
                        train_Y_var += 1
                    else:
                        testing_Y.append(lit_non_lit)
                        train_Y_var += 1
                    break

# Actually runs the nearest neighbors classifier using K nearest neighbors
def run_nearest_neighbors(k):
    neighbor_classifier = KNeighborsClassifier(n_neighbors=k)
    neighbor_classifier.fit(training_X, training_Y)
    correct = 0
    literal_tp = 0
    literal_fp = 0
    nl_tp = 0
    nl_fp = 0
    index = 0
    for item in testing_X:
        answer = neighbor_classifier.predict([item])
        if answer[0] == testing_Y[index]:
            correct += 1
        if answer[0] == 'Literal' and testing_Y[index] == 'Literal':
            literal_tp += 1
        elif answer[0] == 'Literal':
            literal_fp += 1
        elif answer[0] == 'Nonliteral' and testing_Y[index] == 'Nonliteral':
            nl_tp += 1
        else:
            nl_fp += 1
        index += 1
    print("K-Nearest Neighbors Classifier Statistics:")
    print("Precision of 'Literal' Tag: " + str(literal_tp/(literal_tp+literal_fp)))
    print("Recall of 'Literal' Tag: " + str(literal_tp/(literal_tp+nl_fp)))
    print("'F1 of 'Literal' Tag: " + str(2*(((literal_tp/(literal_tp+literal_fp))*(literal_tp/(literal_tp+nl_fp)))/((literal_tp/(literal_tp+literal_fp))+(literal_tp/(literal_tp+nl_fp))))))
    print("Precision of 'Nonliteral' Tag: " + str(nl_tp / (nl_tp + nl_fp)))
    print("Recall of 'Literal' Tag: " + str(nl_tp / (nl_tp + literal_fp)))
    print("'F1 of 'Literal' Tag: " + str(2 * (
                ((nl_tp / (nl_tp + nl_fp)) * (nl_tp / (nl_tp + literal_fp))) / (
                    (nl_tp / (nl_tp + nl_fp)) + (nl_tp / (nl_tp + literal_fp))))))
    print("Overall Accuracy: " + str(correct/len(testing_X)))


if __name__ == "__main__":

    create_sentences()
    gettags('Annotator1Final.xml')
    gettags('Annotator2Final.xml')
    gettags('Annotator3Final.xml')
    google_vect = read_in_google_vectors()
    create_sentence_vectors(google_vect)
    run_nearest_neighbors(1)
