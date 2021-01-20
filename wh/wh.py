from simplenlg.framework import NLGFactory
from simplenlg.lexicon import Lexicon
from simplenlg.realiser.english import Realiser
from simplenlg import phrasespec
from simplenlg import features
from simplenlg.phrasespec import SPhraseSpec
from simplenlg.features import Feature
from simplenlg.features import Tense
from simplenlg.features import InterrogativeType;
from simplenlg.features import Person;
import nltk
import constants
from nltk import word_tokenize, pos_tag
import copy
from extract import subjectMatter

class questionGenerator:
    def __init__(self,sm,sent):#,sub,vb,ob,pp,iob
        self.tense=self.determine_tense_input(sent)
        self.subject_=sm.subject_
        self.sent=sent
        self.object_=sm.object_
        self.verb_=sm.final_verb
        self.pp_=sm.final_prep
        self.iob_=sm.ind_obj
        self.Questions=[]
        self.ner_dict=sm.ner_dict
        self.pos_list=sm.pos_list
        self.dep=sm.dep
        self.tokens=word_tokenize(sent)
#         m=subjectMatter(sent)
#         self.ner_dict=m.get_ner()
#         self.pos_list=m.get_pos()
#         self.dep=m.get_dependency_tree()
        self.lexicon = Lexicon.getDefaultLexicon()
        self.nlgFactory=NLGFactory(self.lexicon)
        self.realiser=Realiser(self.lexicon)
        self.phrase=self.nlgFactory.createClause()


    def determine_tense_input(self,sent):
        text = word_tokenize(sent)
        tagged = pos_tag(text)

        tense = {}
        for word in tagged:
            if word[1]=="MD":
                return "FUTURE"
            elif word[1] in constants.past:
                return "PAST"
            elif word[1] in constants.PAST:
                return "PAST"
            elif word[1] in constants.PRESENT:
                return "PRESENT"

    def get_Question_on_subject(self,subj,phrase):
        if((subj in self.ner_dict and self.ner_dict[subj]=="PERSON") or nltk.pos_tag([subj])[0][1]=='PRP'):
            phrase.setFeature(Feature.INTERROGATIVE_TYPE,InterrogativeType.WHO_SUBJECT)
        else:
            phrase.setFeature(Feature.INTERROGATIVE_TYPE,InterrogativeType.WHAT_SUBJECT)
        return self.realiser.realiseSentence(phrase)

    def get_Questions_on_object(self,obj,phrase):
        if(obj in self.ner_dict.keys()):
            if( self.ner_dict[obj]=="GPE"):
                phrase.setFeature(Feature.INTERROGATIVE_TYPE,InterrogativeType.WHERE)
            elif(self.ner_dict[obj]=="PERSON" or nltk.pos_tag([obj])[0][1]=='PRP'):
                phrase.setFeature(Feature.INTERROGATIVE_TYPE,InterrogativeType.WHO_OBJECT)
        else:
            phrase.setFeature(Feature.INTERROGATIVE_TYPE,InterrogativeType.WHAT_OBJECT)
        return self.realiser.realiseSentence(phrase)
    
    def get_why(self):
        if(len(self.verb_)!=0):
            self.phrase.setVerb(self.verb_[0])
        else:
            return None
        if(len(self.object_)!=0):
            self.phrase.setObject(self.object_)
        else:
            return None
#             o=''
#             i=self.tokens.index(self.verb_)
#             for j in range (i,len(self.tokens),1):
#                 o+=j+' '
#             self.phrase.setObject(self.object_)
        self.phrase.setIndirectObject(self.iob_)
        #     phrase.addModifier(modi)
        #     phrase.setDeterminer(arti)
        if(self.tense=="FUTURE"):
            self.phrase.setFeature(Feature.TENSE, Tense.FUTURE)
        elif(self.tense=="PAST"):
            self.phrase.setFeature(Feature.TENSE, Tense.PAST)
        else:
            self.phrase.setFeature(Feature.TENSE, Tense.PRESENT)
        if(len(self.subject_)!=0):
            self.phrase.setSubject(self.subject_)
        
        self.phrase.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.WHY)
        return self.realiser.realiseSentence(self.phrase)
    
    def get_how(self):
        if(len(self.verb_)!=0):
            self.phrase.setVerb(self.verb_[0])
        if(len(self.object_)!=0):
            self.phrase.setObject(self.object_)
        self.phrase.setIndirectObject(self.iob_)
        #     phrase.addModifier(modi)
        #     phrase.setDeterminer(arti)
        if(self.tense=="FUTURE"):
            self.phrase.setFeature(Feature.TENSE, Tense.FUTURE)
        elif(self.tense=="PAST"):
            self.phrase.setFeature(Feature.TENSE, Tense.PAST)
        else:
            self.phrase.setFeature(Feature.TENSE, Tense.PRESENT)
        if(len(self.subject_)!=0):
            self.phrase.setSubject(self.subject_)
        
        self.phrase.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.HOW)
        return self.realiser.realiseSentence(self.phrase)

    def get_where(self):
        if(len(self.verb_)!=0):
            self.phrase.setVerb(self.verb_[0])
        if(len(self.object_)!=0):
            self.phrase.setObject(self.object_)
        self.phrase.setIndirectObject(self.iob_)
        #     phrase.addModifier(modi)
        #     phrase.setDeterminer(arti)
        if(self.tense=="FUTURE"):
            self.phrase.setFeature(Feature.TENSE, Tense.FUTURE)
        elif(self.tense=="PAST"):
            self.phrase.setFeature(Feature.TENSE, Tense.PAST)
        else:
            self.phrase.setFeature(Feature.TENSE, Tense.PRESENT)
        if(len(self.subject_)!=0):
            self.phrase.setSubject(self.subject_)
        
        self.phrase.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.WHERE)
        return self.realiser.realiseSentence(self.phrase)

    def get_All_Questions(self,Answers):
        if(len(self.verb_)!=0):
            self.phrase.setVerb(self.verb_[0])
        if(len(self.object_)!=0):
            self.phrase.setObject(self.object_)
        self.phrase.setIndirectObject(self.iob_)
        #     phrase.addModifier(modi)
        #     phrase.setDeterminer(arti)
        if(self.tense=="FUTURE"):
            self.phrase.setFeature(Feature.TENSE, Tense.FUTURE)
        elif(self.tense=="PAST"):
            self.phrase.setFeature(Feature.TENSE, Tense.PAST)
        else:
            self.phrase.setFeature(Feature.TENSE, Tense.PRESENT)
        if(len(self.subject_)!=0):
        #     if(final_subject[0] in ner_dict):
        #         if(ner_dict[final_subject[0]]=="ORG"):
        #             phrase.setSubject("Which organisation")
        #             p1=copy.deepcopy(phrase)
        #         elif(ner_dict[final_subject[0]]=="GPE"):
        #             phrase.setSubject("Which place")
        #             p1=copy.deepcopy(phrase)
        #         else:
            self.phrase.setSubject(self.subject_)
            p2=copy.deepcopy(self.phrase)
            if(len(self.pp_)!=0):
                self.phrase.addComplement(str(' '.join (x for x in self.pp_)))
            p1=copy.deepcopy(self.phrase)
            #Questions.append(get_Binary_Questions(phrase)) #output not satisfactory
            #print(self.realiser.realiseSentence(self.phrase))
            self.Questions.append (self.get_Question_on_subject(self.subject_[0],self.phrase))
        else:
            return None
        self.Questions.append(self.get_Questions_on_object(self.object_,p1))
        p=self.pp_
        for final_prep in p:
            prep=' '.join(x for x in p)
            prep=prep.replace(final_prep,'')
            if(len(final_prep)!=0):
                x=list(final_prep.split())
                preposition=x[0]
                remaining_phrase=' '.join(i for i in x[1:])
                #p1.addComplement(prep)
                p2.setFeature(Feature.INTERROGATIVE_TYPE,InterrogativeType.WHERE)
                interrogative=self.realiser.realiseSentence(p2)
                if(remaining_phrase in self.ner_dict.keys() and self.ner_dict[remaining_phrase]=="PERSON"):
                    interrogative=interrogative.replace("Where","Who")
                elif(remaining_phrase in self.ner_dict.keys() and self.ner_dict[remaining_phrase]=="DATE"):
                    interrogative=interrogative.replace("Where","When")
                elif(remaining_phrase in self.ner_dict.keys() and self.ner_dict[remaining_phrase]=="LOC"):
                    pass
                elif(remaining_phrase in self.ner_dict.keys() and self.ner_dict[remaining_phrase]=="ORG"):
                    interrogative=interrogative.replace("Where",str(preposition+" ").capitalize()+"which organisation")
                else:
                    interrogative=interrogative.replace("Where",str(preposition+" ").capitalize()+"what")
                interrogative=interrogative.replace("?",str(" "+prep+"?"))
                self.Questions.append(interrogative)
        for i in self.Questions:
            Answers.append(self.sent)
        return self.Questions