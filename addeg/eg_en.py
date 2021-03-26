#!/usr/bin/env python
# coding: utf-8

# # **Make english examples(json)**
# make `english` examples to `eg/en .json`

# ### **Packages**

# In[1]:


import json
import time
import translatepy
import pandas as pd
import oxford_api
from oxford_api import Word
from pandarallel import pandarallel
from multiprocessing.dummy import Pool as ThreadPool


# ### **Functions**

# In[2]:


#return the same word if it can't translate
def en_es(word):
    translator = translatepy.Translator()
    gtrans=translator.translate(word,'es','en')
    palabra=gtrans.result
    translator.clean_cache()
    return palabra

def en_es_list(eg):
    if eg is None:
        return None
    else:
        return [[x,en_es(x)] for x in eg]
    
#translator.example
'''
1. return a list of objects <class 'translatepy.translators.bing.Example'>
    - Note: it doent return list of strings. You need to convert to str() to use them.
2. return empty list [] if it doesnt have examples, but sometimes return None
'''
def expl_transpy(word):
    translator = translatepy.Translator()
    ex=translator.example(word,'es','en')
    if ex is None:
        ex = []
    ex = [str(x) for x in ex[:4]]
    translator.clean_cache()
    return ex

def get_examples(word):
    try:
        Word.get(word)
    except:
        expl = expl_transpy(word)[:4]
        if len(expl)==0:
            expl = None
        return expl
    else:
        expl=Word.examples()[:4]
        if len(expl)<4:
            expl = expl + expl_transpy(word)[:4]
            expl = expl[:4]
        if len(expl)==0:
            expl = None
        return expl


# ### **Read file merge.json**

# In[3]:


df=pd.read_json('../merge.json')
#df=df.sample(n=50)


# ##### **Create and delete `eg/en` folder**

# In[4]:


#!rm -rf eg/en
#!mkdir eg/en


# ### **Multiprocessing add english examples**

# In[5]:


#worker
def make_eg(word):
    data={}
    data['word']=word
    examples=get_examples(word)
    data['examples']=examples
    with open(f'eg/en/{word}.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)
        
pandarallel.initialize(nb_workers=100, progress_bar=True)
ti=time.time()
df['word'].parallel_apply(make_eg)
tf=time.time()
print(f'ok! in {tf-ti} seconds')

