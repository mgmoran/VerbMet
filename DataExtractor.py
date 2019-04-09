##This is an ugly first pass just to get all the information we need for our annotators...
##We can organize the data better later, maybe with lots of tuples, associating sentences with
##documents, with their instances, etc...but you can use this for now to see all the sentences
## organized by document that have a PropBank annotated verb in them. (often more than one 
##verb (instance) per sentence)

##Stats: 
#9000 "instances" (individual verbs annotated with their arguments)
#186 total documents represented among all the instances
#3469 total sentences


import nltk
from nltk.corpus import treebank,propbank
from collections import defaultdict

# Grabbing the first 9000 propbank instances (these 9000 instances map to 186 documents total)
instances = propbank.instances()[:9000]
#Getting a set of documents represented by these 9000 instances
docs = set(list([instance.fileid for instance in instances]))
#Filling a dictionary of WSJ documents (keys) mapped to all the propbank instances contained in each doc (values)
instancedict = {}
for doc in docs:
    instancedict[doc] = [instance for instance in instances if instance.fileid==doc]

#Create a dictionary of each sentence in the document corresponding to an instance, for each doc
#docs are keys, values are lists of sentences. Sentences are tokenized.
docdict = defaultdict(list)
for doc in instancedict:
    sentlist = set([instance.sentnum for instance in instancedict[doc]])
    docdict[doc] = [treebank.sents(doc)[sentid] for sentid in sentlist]
