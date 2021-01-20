import spacy
import itertools
import re
from spacy import attrs
from spacy.language import Language
from spacy.symbols import NOUN, PROPN, VERB
from spacy.tokens import Doc, Span, Token
import constants
nlp=spacy.load('en_core_web_sm')

class subjectMatter:
    def __init__(self,sentence):
        #lists containing sentence matter
        self.final_subject=[]
        self.final_verb=[]
        self.final_object=[]
        self.final_prep=[]
        self.subject_=''
        self.object_=''
        self.ind_obj=''
        self.sentence=nlp(sentence)
        self.pos_list=[]
        for token in self.sentence:
            self.pos_list.append(token.pos_)
            
        self.dep={}
        for chunk in self.sentence.noun_chunks:
            self.dep[chunk.root.dep_]=chunk.text
            
        self.ner_dict={}
        for entity in self.sentence.ents:
            self.ner_dict[entity.text]=entity.label_
        
        no_of_prep=self.pos_list.count('ADP')
        self.ignore_=[False for i in range(no_of_prep)]
    
    def set_svo(self,a):
        self.subject_=a[0]
        self.object_=a[2]
        self.final_verb.append(a[1])
        
        
    def get_pos(self):
        return self.pos_list
    
    def get_dependency_tree(self):
        return self.dep
    
    def get_ner(self):
        return self.ner_dict
    
    def get_verb(self):
        return [i for i in self.sentence if i.pos_ == 'VERB' and i.dep_ not in constants.aux]
    
    def get_conjunctions(self,token_):
        return [i for i in token_.rights if i.dep_ == 'conj']
    
    def get_subject(self,verb):
        subjs=[tok for tok in verb.lefts if tok.dep_ in constants.subject]
        #get additional conjunct subjects
        subjs.extend(tok for subj in subjs for tok in self.get_conjunctions(subj))
        return subjs
    
    def get_object(self,verb):
        objs=[tok for tok in verb.rights if tok.dep_ in constants.obj]
        #get open clausal complements(xcomp)
        objs.extend(tok for tok in verb.rights if tok.dep_ == 'xcomp')
        objs.extend(tok for obj in objs for tok in self.get_conjunctions(obj))
        return objs
    
    def get_compound_noun_span(self,noun):
        min_i=noun.i-sum(1 for _ in itertools.takewhile(lambda x:x.dep_=='compound',reversed(list(noun.lefts))))
        return (min_i,noun.i)
    
    def get_span_for_verb_auxiliaries(self,verb):
        min_i = verb.i - sum(
            1
            for _ in itertools.takewhile(
                lambda x: x.dep_ in constants.aux, reversed(list(verb.lefts))
            )
        )
        max_i = verb.i + sum(
            1
            for _ in itertools.takewhile(
                lambda x: x.dep_ in constants.aux, verb.rights
            )
        )
        return (min_i, max_i)
    
    def get_prepositional_phrase(self):
        p=[]
        s=''
        add_=False
        j=-1
        k=0
        for i in self.pos_list:
            j+=1
            if i=='PUNCT':
                p.append(s.rstrip())
                k+=1
                break
            if(add_ and i in constants.prep_pos):
                s+=self.sentence[j].text+' '
            if(add_ and i=='ADP'):
                p.append(s.rstrip())
                k+=1
                s=self.sentence[j].text+' '
            if(add_ and i=='VERB'):
                p.append(s.rstrip())
                s=''
                add_=False
                self.ignore_[k]=True
                k+=1
            if(not add_ and i=='ADP'):
                s+=self.sentence[j].text+' '
                add_=True
        if(s!=''):
            p.append(s.rstrip())
        p=list(set(p))  #AEZAKMI
        return p

    def combinations(self,l):
        s=''
        for i in range(0,len(l)-1,1):
            if(s.find(l[i])==-1):
                s+=l[i]+', '
        if(s.find(l[i+1])==-1):
            s+='and '+l[i+1]
        return s 
    
    def get_full(self,subjs,ch):
        if(ch=="S"):
            for j in range(len(subjs)):
                if(subjs[j] in self.dep.keys()):
                    continue
                for i in self.dep.keys():
                    if(i in constants.subject and self.dep[i].find(subjs[j])>-1):
                        subjs[j]=self.dep[i]
        elif(ch=="O"):
            for j in range(len(subjs)):
                for i in self.dep.keys():
                    if(i in constants.obj and self.dep[i].find(subjs[j])>-1):
                        subjs[j]=self.dep[i]
        return subjs

    def extract_svop(self):
        verbs=self.get_verb()
        self.ind_obj=''
        if 'dative' in self.dep:
            self.ind_obj=self.dep['dative']
        for verb in verbs:
            subjs=self.get_subject(verb)
            if not subjs:
                continue
            objs=self.get_object(verb)
            if not objs:
                continue
            
            start_i=self.sentence[0].i
            verb_span=self.get_span_for_verb_auxiliaries(verb)
            verb=self.sentence[verb_span[0]-start_i:verb_span[1]-start_i+1]
            count_=-1
            for subj in subjs:
                subj=self.sentence[
                    self.get_compound_noun_span(subj)[0]
                    - start_i: subj.i
                    - start_i
                    + 1
                ]
                count_+=1
                iob=''
                c_obj=-1
                for obj in objs:
                    if obj.pos == 'NOUN':
                        span=self.get_compound_noun_span(obj)[0]
                    elif obj.pos == 'VERB':
                        span=self.get_span_for_verb_auxiliaries(obj)
                    else:
                        span=(obj.i,obj.i)
                    obj=self.sentence[span[0]-start_i:span[1]-start_i+1]
                    self.final_subject.append(subj.text)
                    self.final_verb.append(verb.text)
                    self.final_object.append(obj.text)
        self.final_prep=self.get_prepositional_phrase()
        self.final_subject=self.get_full(self.final_subject,"S")
        if(len(self.final_subject)>1):
            self.subject_=self.combinations(self.final_subject)
        else:   
            self.subject_=' '.join(x for x in self.final_subject)
        self.final_object=self.get_full(self.final_object,"O")
        if(len(self.final_object)>1):
            self.object_=self.combinations(self.final_object)
        else:
            self.object_=' '.join(x for x in self.final_object)
        for i in range(len(self.ignore_)):
            if(self.ignore_[i]==True):
                self.subject_+=' '+str(self.final_prep[i])
        for i in range(len(self.ignore_)):
            if(self.ignore_[i]==True):
                del self.final_prep[i]
        
                    
        
            