import preprocess
from nltk.tokenize import word_tokenize
from nltk.cluster.util import cosine_distance
import numpy as np
from scipy import spatial
import networkx as nx
from gensim.models import Word2Vec
import pandas as pd
import nltk
import sentence_selection as ss
from extract import subjectMatter
from wh import questionGenerator
from simplifier import simpleSentence
import quest


def execute_():
    #input Passage
    passage=input()
    #passage='''Barack Obama is an American politician and attorney who served as the 44th president of the United States from 2009 to 2017. Obama was the first African-American president of the United States. Barack was a member of Democratic Party. '''

    origional=preprocess.tokenize_sent(passage)
    sent_list=origional.copy()
    for i in range(len(sent_list)):
        sent_list[i]=preprocess.inp_to_Lower(sent_list[i])
        sent_list[i]=preprocess.remove_punctuation(sent_list[i])
        sent_list[i]=preprocess.remove_STOPWORD(sent_list[i])

    #sentence selection
    sentences=[]
    for i in sent_list:
        sentences.append(word_tokenize(i))#break sentence into list of words
    sorted_dict=ss.pageRank(ss.similarity(sentences,ss.sentence_embedding(sentences)))
    sorted_indices=list(sorted_dict)#sort the list of sentences
    ranked_sentences=[]
    for i in sorted_indices:
        ranked_sentences.append(origional[i])

    Answers=[]
    Questions=[]
    q=1
    
    #Fill Up Questions will be stored here
    type1=[]
    ans1=[]
    
    #Binary Questions Will be stored here
    type2=[]
    ans2=[]
    
    #True-False Questions will be stored here
    type3=[]
    ans3=[]
    
    #Wh and How type Questions will be stored here
    type4=[]
    ans4=[]
    #get Questions
#     for important_sentence in ranked_sentences:
#         sm=subjectMatter(important_sentence)
#         x=[]
#         y=[]
#         x=quest.getGapFill(sm,important_sentence,y)
#         ans1.extend(y)
#         type1.extend(x)#gap fill list
#         Questions.extend(x)
#         Answers.extend(y)
#         y=[]
#         x=quest.getBinaryQuestions(important_sentence,y)
#         ans2.extend(y)
#         type2.extend(x)#Binary list
#         Questions.extend(x)
#         Answers.extend(y)
#         y=[]
#         x=quest.getTrueFalse(important_sentence,y)
#         ans3.extend(y)
#         type3.extend(x)#True-False
#         Questions.extend(x)
#         Answers.extend(y)
#         y=[]
#         sm.extract_svop()
#         qg=questionGenerator(sm,important_sentence)
#         x=qg.get_All_Questions(y)
#         if(x!=None):
#             type4.extend(x)
#             ans4.extend(y)
#             Questions.extend(x)#WH
#             Answers.extend(y)
#     for i in range(len(Questions)):
#         print('Q '+str(q)+'. '+Questions[i])
#         print('Ans: '+Answers[i]+"\n")
#         q+=1
        
    for sent in ranked_sentences:
        simp=simpleSentence(sent)
        simple_sentences=simp.simplify()
        type4.extend(simp.q)
        ans4.extend(simp.a)
        if(simp.q!=None):
            Questions.extend(simp.q)#WH
            Answers.extend(simp.a)
        simp.close_NLP()
    for i in range(len(Questions)):
        print('Q '+str(q)+'. '+Questions[i])
        print('Ans: '+Answers[i]+"\n")
        q+=1
        
    for i in range(len(Questions)):
        print('Q '+str(q)+'. '+Questions[i])
        print('Ans: '+Answers[i]+"\n")
        q+=1
        
        
