from nltk.tokenize import word_tokenize
import constants
import preprocess
import re
from stanfordcorenlp import StanfordCoreNLP

from extract import subjectMatter
from wh import questionGenerator

class simpleSentence:
    def __init__(self,sentence):
        self.sentence=sentence
        self.nlp = StanfordCoreNLP(r'C:\stanford-corenlp-4.1.0')
        self.l=[]
        self.a=[]
        self.q=[]
        for i in constants.complex_conjunct.keys():
            self.l.extend(constants.complex_conjunct[i])
     
    def isnotSimple(self):
        for token in word_tokenize(self.sentence):
            if token in self.l:
                return True
        return False
                
   
    def simplify(self):
        ans=[]
        if self.isnotSimple():
            return self.split_sentence(self.sentence,self.a,self.q)
        return list(self.sentence)
        
    def transform(self,sent):    #brings conjunctions in the middle
        break_point=sent.index(',')
        s=sent[break_point+1:-1]+' '+sent[:break_point]+sent[-1]
        return s
        
    def get_svo(self,sent):
        parsed_data=self.nlp.parse(sent)
        count_=1
        ans=[]
        s=''
        ot=word_tokenize(sent)
        parsed_data=parsed_data[parsed_data.index('VP')+4:]
        for token in word_tokenize(parsed_data):
            if token in ot:
                s+=token+' '
            elif token == ')':
                count_-=1
            if(count_==0):
                break
        if(s in sent):
            ans.append(sent[:sent.index(s)])
            ans.append(s)
            ans.append(sent[(sent.index(s)+len(s)):])
        return ans
    
    def get_why(self,sent):
        a=self.get_svo(sent)
        sm=subjectMatter(sent)
        sm.set_svo(a)
#         sm.extract_svop()
#         print("********",sm.final_verb)
        qg=questionGenerator(sm,sent)
        return qg.get_why()
    
    def get_how(self,sent):
        a=self.get_svo(sent)
        sm=subjectMatter(sent)
        sm.set_svo(a)
        qg=questionGenerator(sm,sent)
        return qg.get_how()
    
    def get_where(self,sent):
        a=self.get_svo(sent)
        sm=subjectMatter(sent)
        sm.set_svo(a)
        qg=questionGenerator(sm,sent)
        return qg.get_where()
        
    def split_sentence(self,sent,A,Q):
        s=preprocess.inp_to_Lower(sent)
        ans=[]
        conjs=[]
        l2=[]
        for i in constants.complex_conjunct.keys():
            if(i=='reason' or i=='purpose' or i=='contrast' or i=='manner' or i=='place'):
                l2.append(i)
        i=0
        for word in word_tokenize(s):
            if word in self.l:
                conjs.append(word)  #conjs is the list of conjunctions in the sentence
        for i in conjs:
            print('\n\n\n',i,'\n',s,'\n\n\n')
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
            if(j=='reason'):
                Q.append(self.get_why(ans[-1]))
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
    
    def close_NLP(self):
        self.nlp.close()
         

