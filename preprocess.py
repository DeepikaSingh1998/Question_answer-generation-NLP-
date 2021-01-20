import nltk
import pandas as pd
#for punctuation removal
import string
#for stopwords
from nltk.corpus import stopwords
#for frequent words
from collections import Counter
#for stemmer
from nltk.stem.porter import PorterStemmer
#for lemmatizer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
#sentence tokenizer
from nltk.tokenize import sent_tokenize

def tokenize_sent(passage):
    sent_list=sent_tokenize(passage)
    return sent_list

def inp_to_Lower(passage):
    passage=passage.lower()
    return passage

#string.punctuation contains: !"#$%&\'()*+,-./:;<=>?@[\\]^_{|}~` (which are punctuation marks)
def remove_punctuation(passage):
    removables=string.punctuation
    passage = passage.translate(str.maketrans('', '', removables))
    return passage

def remove_STOPWORD(passage):
    STOPWORDS=set(stopwords.words('english'))
    passage=" ".join([word for word in str(passage).split() if word not in STOPWORDS])
    return passage

#not required for now, as we are currently dealing with a passage
def remove_frequent(passage):
    cnt_ob=Counter()
    for word in passage.split():
        cnt_ob[word]+=1
    frequent_words=set([w for (w,wc) in cnt_ob.most_common(10)]) #can be changed as per requirement
    passage=" ".join([word for word in str(passage).split() if word not in frequent_words])
    return passage

def stemmer_(passage):
    stemmer=PorterStemmer()
    passage_=" ".join([stemmer.stem(word) for word in passage.split()])
    passage_ #storing it in another variable for now
    return passage_

def lemmatizer_(passage):
    lemmatizer=WordNetLemmatizer()
    wordnet_map={"N":wordnet.NOUN, "V": wordnet.VERB, "J":wordnet.ADJ, "R": wordnet.ADV}
    passage= " ".join([lemmatizer.lemmatize(word) for word in passage.split()])
    return passage