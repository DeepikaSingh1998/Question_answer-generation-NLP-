#import pathlib
import re

subject={'agent','csubj','csubjpass','expl','nsubj','nsubjpass'}
obj={'attr','dobj','oprd'}
aux={'aux','auxpass','neg'}
prepositional_phrase={'pobj','pcomp','prep'}
numeric={'ORDINAL','CARDINAL','MONEY','QUANTITY','PERCENT','TIME','DATE'}
prepositions={'above', 'across', 'against', 'along', 'among', 'around', 'at', 'before', 'behind', 'below', 'beneath', 'beside', 'between', 'by', 'down', 'from', 'in', 'into', 'near', 'of', 'off', 'on', 'to', 'toward', 'under', 'upon', 'with', 'within'}
prep_pos={'NOUN','PROPN','NUM','ADD','DET','ADJ','CONJ','PRON','SYM'}
PRESENT={'VB','VBG','VBP','VBZ'}
PAST={'VBN','VBD'}
past=['was', 'were','had', 'did','could']
aux_list=['am', 'is', 'are', 'was', 'were', 'being', 'been','be','have',
          'has', 'had', 'do', 'does', 'did', 'will', 'would', 'shall', 'should', 'may', 'might', 'must', 'can', 'could']
relative_clause=['who','whose','whom','which','where']

complex_conjunct={'contrast':['although','though','even though','while','whereas'],
                  'reason':['because','since'],
                  'time':['when','as soon as','while','once','until','after','before'],
                  'purpose':['so that'], 
                  'condition':['if', 'unless'], 
                  'manner':['as'],
                  'place':['where'], 
                  'person':['who', 'whose'] ,
                  'thing':['which', 'that'], 
                  'report':['whether','how']}

              
patterns={
    "en":{
        "NP": r"<DET>? <NUM>* (<ADJ> <PUNCT>? <CONJ>?)* (<NOUN>|<PROPN> <PART>?)+",
        #"PP": r'<ADP><DET>?(<NUM>)*(<ADJ><PUNCT>?<CONJ>?)*(<PROPN>)*|(<NOUN><PART>?)+',
        "PP": r'<ADP><DET>?(<NUM>)*(<ADJ><PUNCT>?<CONJ>?)*(<NOUN><PART>?)+',
        "VP": r"<AUX>* <ADV>* <VERB>",
    }
}