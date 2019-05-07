from nltk.corpus import wordnet as wn
from nltk.corpus import propbank
from nltk.corpus.reader.propbank import PropbankChainTreePointer
from nltk.corpus.reader.propbank import PropbankSplitTreePointer




class VerbMetClass:
    def __init__(self, verb_string, sent_string, pb_inst, label, mismatch):
        self.label = label
        self.mismatch = mismatch
        self.sent_string = sent_string
        self.verb_string = verb_string
        self.tree = pb_inst.tree

        self.arg0 = None
        self.arg1 = None
        self.arg2 = None
        self.rs_arg0 = None
        self.rs_arg1 = None

        if pb_inst.roleset[-1:].isnumeric():
            self.rs = propbank.roleset(pb_inst.roleset)

        for arg in pb_inst.arguments:
            if isinstance(arg[0], PropbankSplitTreePointer):
                arg = arg[0].pieces
            if isinstance(arg[0], PropbankChainTreePointer):
                arg = arg[0].pieces
            if isinstance(arg[0], PropbankSplitTreePointer):
                arg = arg[0].pieces

            string_rep = str(self.tree[arg[0].treepos(self.tree)].productions())
            li = string_rep.strip('[]').split()

            noun_list = []
            for index, elem in enumerate(li):
                if (elem[:2] == 'NN') and (li[index + 1] == '->'):
                    noun_list.append(li[index + 2])
                elif (elem[:3] == 'PRP') and (li[index+1] == '->'):
                    noun_list.append(li[index+2])

            if (arg[1] == 'ARG0') and (len(noun_list) > 1):
                self.arg0 = noun_list[0].strip(',\"')
                #print('arg0', self.arg0)

            elif (arg[1] == 'ARG1') and (len(noun_list) > 1):
                self.arg1 = noun_list[0].strip(',\"')
                #print('arg1', self.arg1)

            elif (arg[1] == 'ARG2') and (len(noun_list) > 1):
                self.arg2 = noun_list[0].strip(',\"')
                #print('arg2', self.arg2)

        for role in self.rs.findall('roles/role'):
            if role.attrib['n'][0] == '0':
                self.rs_arg0 = role.attrib['descr'].split()[0]
            if role.attrib['n'][0]== '1':
                self.rs_arg1 = role.attrib['descr'].split()[0]

    def toString(self):
        print("Verb: " + repr(self.verb_string))
        print("Arg0: " + repr(self.arg0))
        print("Arg1: " + repr(self.arg1))
        print("Label: " + self.label)






