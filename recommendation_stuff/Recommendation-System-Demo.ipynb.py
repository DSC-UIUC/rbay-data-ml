#!/usr/bin/env python
# coding: utf-8

# In[34]:


import pytextrank
import spacy
import numpy
import gzip
import gensim
import logging
import os
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


# In[15]:


text = "Compatibility of systems of linear constraints over the set of natural numbers. Criteria of compatibility of a system of linear Diophantine equations, strict inequations, and nonstrict inequations are considered. Upper bounds for components of a minimal set of solutions and algorithms of construction of minimal generating sets of solutions for all types of systems are given. These criteria and the corresponding algorithms for constructing a minimal supporting set of solutions can be used in solving all the considered types systems and systems of mixed types."


# In[16]:


nlp = spacy.load("en_core_web_sm")
tr = pytextrank.TextRank()
nlp.add_pipe(tr.PipelineComponent, name="textrank", last=True)

doc = nlp(text)

# examine the top-ranked phrases in the document
phrases = []
for p in doc._.phrases:
    #print("{:.4f} {:5d}  {}".format(p.rank, p.count, p.text))
    phrases.append((p.rank, p.count, p.text))
    #print(p.chunks)

phrases = sorted(phrases, reverse=True)
phrases


# In[17]:


keywords = [x[2] for x in phrases]
keywords


# In[18]:


logging.basicConfig(level=logging.DEBUG,
                    filename='test.log', filemode='w')


# In[19]:


f1 = open('arxiv-titles-250k.txt')
pp_titles = f1.readlines()

f2 = open('arxiv-abstracts-250k.txt')
pp_abstracts = f2.readlines()


# In[27]:


post_titles = []
for el in pp_titles:
    for elem in el.split():
        post_titles.append(re.sub(r'\W+', '', elem))

post_abstracts = []
for el in pp_abstracts:
    for elem in el.split():
        post_abstracts.append(re.sub(r'\W+', '', elem))


# In[28]:


post_titles


# In[29]:


post_abstracts


# In[32]:


post_words = post_titles + post_abstracts


# In[35]:


nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
post_words = [el for el in post_words if not el in stop_words]
post_words


# In[ ]:
