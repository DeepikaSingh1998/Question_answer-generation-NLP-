from nltk.tokenize import word_tokenize
import constants
import preprocess
import re
from stanfordcorenlp import StanfordCoreNLP

from extract import sentenceMatter
from wh import questionGenerator

class simpleSentence:
    def __init__(self,sentence):
        self.sentence=sentence
        self.nlp = StanfordCoreNLP(r'C:\stanford-corenlp-4.1.0')
   
        
    def transform(self,sent):    #brings conjunctions in the middle
        break_point=sent.index(',')
        s=sent[break_point+1:-1]+' '+sent[:break_point]+sent[-1]
        return s
        
    def get_why(self,sent):
        sm=sentenceMatter(sent)
        sm.extract_svop()
        qg=questionGenerator(sm,sent)
        return qg.get_why()
    
    def get_how(self,sent):
        sm=sentenceMatter(sent)
        sm.extract_svop()
        qg=questionGenerator(sm,sent)
        return qg.get_how()
    
    def get_where(self,sent):
        sm=sentenceMatter(sent)
        sm.extract_svop()
        qg=questionGenerator(sm,sent)
        return qg.get_where()
        
    def split_sentence(self,sent,A,Q):
        s=preprocess.inp_to_Lower(sent)
        ans=[]
        l=[]
        conjs=[]
        l2=[]
        for i in constants.complex_conjunct.keys():
            if(i=='reason' or i=='purpose' or i=='contrast' or i=='manner' or i=='place'):
                l2.append(i)
            l.extend(constants.complex_conjunct[i])
        i=0
        for word in word_tokenize(s):
            if word in l:
                conjs.append(word)
        for i in conjs:
            j=s.index(i)
            if(j==0):
                sent=self.transform(sent)
            s=preprocess.inp_to_Lower(sent)
            j=s.index(i)
            s=s[j:]
            z = re.compile(re.escape(s), re.IGNORECASE)
            txt=z.sub('', sent)
            ans.append(txt)
#             ans.append(s.replace(s,''))
            s=s.replace(i,'')
            for j in l2:
                if(i in constants.complex_conjunct[j]):
                    break
            print(j)
            if(j=='reason'):
                Q.append(self.get_why(ans))
                A.append(sent)
            elif j=='contrast':
                z = re.compile(re.escape(s), re.IGNORECASE)
                txt=z.sub('', sent)
                ans.append(txt)
            elif j=='purpose':
                Q.append(self.get_why(ans[-1]))
                A.append(sent)
            elif j=='manner':
                Q.append(self.get_how(ans[-1]))
                A.append(sent)
            elif j=='place':
                Q.append(self.get_where(ans[-1]))
                A.append(sent)
        return ans
         

