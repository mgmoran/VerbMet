##Extracts annotatable sentences that correspond to Instance objects in Propbank.
##Eventually we might want to organize this data better, perhaps into tuples associating
##sentences with their doc name, instance number, etc.


##Stats: 
#9000 "instances" (individual verbs annotated with their arguments)
#186 total documents represented among all the instances
#3469 total sentences


import nltk
from nltk.corpus import treebank,propbank
from collections import defaultdict

# Grabbing the first 9000 propbank instances (these 9000 instances map to 186 documents total)
instances = propbank.instances()[:9000]
#Extracting the set of documents represented by these 9000 instances
docs = set(list([instance.fileid for instance in instances]))
#A dictionary that maps WSJ documents (keys) to all propbank instances contained in each doc (values)
instancedict = defaultdict(list)
for doc in docs:
    instancedict[doc] = [instance for instance in instances if instance.fileid == doc]

#A dictionary of WSJ docs mapped to every sentence in that doc associated to a PB instance.
#Each sentence is then mapped to a list of its PB instances.
sentdict = defaultdict(lambda: defaultdict(list))
for doc in instancedict:
        sentlist = set([instance.sentnum for instance in instancedict[doc]])
        for num in sentlist:
            sentdict[doc][num] = [instance for instance in instancedict[doc] if instance.sentnum==num]

#For simplicity's sake, I filter out all sentences that have more than one
#PB instance.
#Creates a dictionary of WSJ doc names mapped to viable sentences for annotation in that doc.
#Sentences are tokenized.
docdict = defaultdict(list)
for doc in sentdict:
    sentlist = set([instance.sentnum for instance in instancedict[doc]])
    docdict[doc] = [treebank.sents(doc)[sentid] for sentid in sentdict[doc] if len(sentdict[doc][sentid])==1]
