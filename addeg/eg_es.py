#!/usr/bin/env python
# coding: utf-8

# # **Make spanish examples(json)**
# make `spanish` examples to `eg/es .json`

# ### **Packages**

# In[1]:


import os
import json
import time
import translatepy
from multiprocessing.dummy import Pool as ThreadPool
from tqdm import tqdm


# ### **Functions**

# In[2]:


#return the same word if it can't translate
def en_es(word):
    translator = translatepy.Translator()
    gtrans=translator.translate(word,'es','en')
    palabra=gtrans.result
    translator.clean_cache()
    return palabra

#trasnlate list and return [['en','es'],['en','es'],...]
def en_es_list(eg):
    if eg is None:
        return None
    else:
        return [[x,en_es(x)] for x in eg]


# ### **Get word from json file name `eg/en`**

# In[3]:


words=[]
files = os.listdir('eg/en')
#files = os.listdir('eg/en')[:10]

for f in files:
    if f.endswith('.json'):
        #print(f.replace('.json',''))
        words.append(f.replace('.json',''))


# ##### **Create and delete `eg/es` folder**

# In[4]:


#!rm -rf eg/es
#!mkdir eg/es


# ### **Multiprocessing add english examples**

# In[5]:


#worker
def make_eg_es(word):
    with open(f'eg/en/{word}.json') as json_file:
        data = json.load(json_file)
    
    examples = data['examples']
    examples = en_es_list(examples)
    
    data.update({'examples':examples})
    
    with open(f'eg/es/{word}.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)
    
    pbar.update(1)

#multiprocessing
pbar = tqdm(total=len(words))
pool = ThreadPool(100)
pool.starmap(make_eg_es, zip(words)) 
pool.close() 
pool.join()

