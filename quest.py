import preprocess
import constants
import re
from nltk.tokenize import word_tokenize


def getGapFill(sm,sent,A):
    q=1
    Q=[]
    for i in sm.ner_dict.keys():
        Q.append(sent.replace(str(i),'___________'))
        A.append(i)
    return Q

def getBinaryQuestions(sentence,A):
    s1=sentence
    Q=[]
    sentence=preprocess.remove_punctuation(sentence)
    s=preprocess.inp_to_Lower(sentence)
    l=word_tokenize(s)
    for i in constants.aux_list:
        if(i in l):
            x=s.index(i)
            break
#         if re.search(i,s):
#             x=s.index(i)
#             break
    if(i in l):
        s=i.capitalize()+' '+sentence.replace(i,'')+'?'
        Q.append(s)
        A.append('Yes')
        s=i.capitalize()+' '+sentence.replace(i,'not')+'?'
        Q.append(s)
        A.append('No')
    return Q

def getTrueFalse(s1,A):
    #True-False
    sentence=preprocess.remove_punctuation(s1)
    sentence=preprocess.inp_to_Lower(sentence)
    l=word_tokenize(sentence)
    for i in constants.aux_list:
        if i in l:
            x=sentence.index(i)
            break
    Q=[]
    Q.append(s1)
    A.append('True')
    s=s1.replace(i, i+' not')
    Q.append(s)
    A.append('False')
    return Q

    