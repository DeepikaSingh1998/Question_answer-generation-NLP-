from scipy import spatial
import numpy as np
import networkx as nx
from gensim.models import Word2Vec
import pandas as pd
import preprocess
from nltk.tokenize import word_tokenize
from nltk.cluster.util import cosine_distance
import nltk

def sentence_embedding(sentences):
    #Vector representation
    w2v=Word2Vec(sentences,size=1,min_count=1,iter=1000)
    sentence_embeddings=[[w2v[word][0] for word in words] for words in sentences]
    max_len=max([len(tokens) for tokens in sentences])
    sentence_embeddings=[np.pad(embedding,(0,max_len-len(embedding)),'constant') for embedding in sentence_embeddings]
    return sentence_embeddings

def similarity(sentences,sentence_embeddings):
    #cosine similarity
    sim_matrix=np.zeros((len(sentences),len(sentences)))
    for i in range(len(sentence_embeddings)):
        for j in range(len(sentence_embeddings)):
            sim_matrix[i][j]= 1-spatial.distance.cosine(sentence_embeddings[i],sentence_embeddings[j])
    for i in range(len(sim_matrix)):#normalization
        sim_matrix[i]=sim_matrix[i]/sim_matrix[i].sum()
    return sim_matrix

def pageRank(sim_matrix):
    #get the pagerank
    nx_graph = nx.from_numpy_array(sim_matrix)
    scores = nx.pagerank(nx_graph)
    sorted_dict={k:v for k,v in sorted(scores.items(), key=lambda item:item[1])}    
    return sorted_dict