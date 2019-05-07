import nltk
import verbmetclass
from verbmetclass import VerbMetClass
from nltk.corpus import propbank
from nltk.corpus import wordnet as wn
from xml.etree import ElementTree
from collections import defaultdict
import xml.etree.ElementTree as ET
import csv
from nltk.tree import Tree

annotations = defaultdict(dict)
sentence_span = defaultdict(dict)
sents = defaultdict(lambda : defaultdict())
sentence_trees = defaultdict(lambda : Tree)
verbdict = defaultdict(list)
typedict = defaultdict(list)
labeled_data = []


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
            sentences.append((line, firstIndex, secondIndex))  # text, starting index, ending index
    args = [elem for elem in root[1] if elem.tag == 'ARG']
    verbs = [elem for elem in root[1] if elem.tag == 'VERB']
    mismatches = [elem for elem in root[1] if elem.tag == 'MISMATCH']
    for sentence in sentences:
        for verb in verbs:
            start = int(verb.attrib['spans'].split('~')[0])
            end = int(verb.attrib['spans'].split('~')[1])
            if start >= sentence[1] and end <= sentence[2]:
                v = verb.attrib['text']
                type = verb.attrib['type']
                mm = [m.attrib['fromText'] for m in mismatches if
                      'toID' in m.attrib and int(m.attrib['toID'][1:]) == int(verb.attrib['id'][1:])]
                arguments = list(
                    set([(arg.attrib['text'], arg.attrib['type']) for arg in args if arg.attrib['text'] in mm]))
                annotations[sentence[0]] = (v,type, arguments)
    for sentence in annotations:
        if annotations[sentence][1] == 'Nonliteral':
            for arg in annotations[sentence][2]:
                    verbdict[annotations[sentence][0]].append(arg[1])

def create_verbmet_objects():
    verbmet_objects = []
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
                    if instance.roleset[-1:].isnumeric():
                        # unpacking instance starts here -------------------
                        text = sents[doc][sent]
                        if annotations[text]:
                            verb_string = annotations[text][0]
                            label = annotations[text][1]
                            mismatch = annotations[text][2]
                            v_object = VerbMetClass(verb_string, text, instance, label, mismatch)
                            verbmet_objects.append(v_object)
    return verbmet_objects

def create_feature_sets(v_objects):
    feature_sets = [(feature_dict(v_object), v_object.label) for v_object in v_objects]
    splitpoint = int(len(feature_sets)*.7)
    print("Total instances: ", len(feature_sets))
    print("Training instances: ", splitpoint)
    print("Test instances: ", len(feature_sets) - splitpoint)
    train_set, test_set = feature_sets[:splitpoint], feature_sets[splitpoint:]
    return train_set, test_set

def has_Proper_subject(v_object):
    if v_object.arg0 is not None:
        return v_object.arg0[0].isupper()
    else:
        return False

def feature_dict(v_object):
    featureset = {}
    featureset['proper_subject'] = has_Proper_subject(v_object)
    featureset['has_arg2'] = (v_object.arg2 is not None)
    most_likely_mismatch = 'Subject'
    try:
        most_likely_mismatch = verbdict[v_object.verb_string][0]
    except IndexError:
        most_likely_mismatch=='Subject'
    if most_likely_mismatch == 'Subject':
        featureset['has_arg0'] = (v_object.arg0 is not None)
        featureset['roleset_arg0'] = v_object.rs_arg0
    if most_likely_mismatch =='Object':
        featureset['has_arg1'] = (v_object.arg1 is not None)
        featureset['roleset_arg1'] = v_object.rs_arg1
    return featureset

def train_classifier(training_set):
    classifier = nltk.NaiveBayesClassifier.train(training_set)
    return classifier

def evaluate_classifier(classifier, test_set):
    trueliteral = len([verb for verb in test_set if verb[1]=='Literal'])
    truenonliteral = len([verb for verb in test_set if verb[1]=='Nonliteral'])
    falseliteral = 0
    falsenonliteral = 0
    for verb in test_set:
        verbobject = v_objects[test_set.index(verb)]
        answer = classify_verb(verbobject,classifier)
        if answer == 'Nonliteral':
            if answer==verb[1]:
                truenonliteral +=1
            else:
                falsenonliteral +=1
        else:
            if answer==verb[1]:
                trueliteral +=1
            else:
                falseliteral +=1
    lprecision = (trueliteral/ (trueliteral + falseliteral))
    nprecision = (truenonliteral/ (truenonliteral + falsenonliteral))
    lrecall = trueliteral / (trueliteral + falsenonliteral)
    nrecall = (truenonliteral / (truenonliteral + falseliteral))
    lf1 = (2 * lprecision * lrecall)/ (lprecision + lrecall)
    nf1 = (2 * nprecision * nrecall)/(nprecision + nrecall)
    print("\t\t\tPrecision\t\tRecall\t\tF1")
    print("Literal\t\t%.2f\t\t%.2f\t\t %.2f" %(lprecision,lrecall,lf1))
    print("Nonliteral\t%.2f\t\t%.2f\t\t %.2f" % (nprecision, nrecall, nf1))
    print()
    print("Accuracy: %.2f" %(nltk.classify.accuracy(classifier, test_set)))


def classify_verb(v_object, classifier):
    feat_set = feature_dict(v_object)
    return classifier.classify(feat_set)



if __name__ == '__main__':
    gettags('Annotator1Final.xml')
    gettags('Annotator2Final.xml')
    gettags('Annotator3Final.xml')
    for verb in verbdict:
        verbdict[verb] = sorted([arg for arg in verbdict[verb]], key=lambda arg:verbdict[verb].count(arg))
    v_objects = create_verbmet_objects()
    training_set, test_set = create_feature_sets(v_objects)
    classifier = train_classifier(training_set)
    evaluate_classifier(classifier, test_set)
    #classifier.show_most_informative_features()
