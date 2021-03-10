#!/usr/bin/env python
# coding: utf-8

# In[8]:


#pip install beautifulsoup4 requests
import requests
from bs4 import BeautifulSoup
import pandas as pd


# In[9]:


url='https://www.oxfordlearnersdictionaries.com/wordlists/oxford3000-5000'
headers={"User-Agent":"Mozilla/5.0"}

page=requests.get(url,headers=headers)
soup=BeautifulSoup(page.content, 'html.parser')
content = soup.find('ul',class_='top-g')


# ## **Word**

# In[10]:


word=[]
for li in content.find_all('li'):
    try:
        word.append(li.find('a').text)
    except:
        word.append(li.find('span').text)


# ## **Word type**

# In[11]:


type_word=[]
for li in content.find_all('li'):
    type_word.append(li.find('span',class_='pos').text)


# ## **Level**

# In[12]:


level=[]
for li in content.find_all('li'):    
    try:
        level.append(li.find('span',class_='belong-to').text)
    except:
        level.append(None)


# ## **Audio**

# In[13]:


uk_mp3=[]
uk_ogg=[]
us_mp3=[]
us_ogg=[]
base_url='https://www.oxfordlearnersdictionaries.com'

for li in content.find_all('li'):
    try:
        uk_mp3.append(base_url + li.find('div',class_='sound audio_play_button icon-audio pron-uk')['data-src-mp3'])
        uk_ogg.append(base_url + li.find('div',class_='sound audio_play_button icon-audio pron-uk')['data-src-ogg'])
        us_mp3.append(base_url + li.find('div',class_='sound audio_play_button icon-audio pron-us')['data-src-mp3'])
        us_ogg.append(base_url + li.find('div',class_='sound audio_play_button icon-audio pron-us')['data-src-ogg'])
    except:
        uk_mp3.append(None)
        uk_ogg.append(None)
        us_mp3.append(None)
        us_ogg.append(None)


# ## **Save as csv**

# In[14]:


fields={'word':word,
        'type_word':type_word,
        'level':level,
        'uk_mp3':uk_mp3,
        'uk_ogg':uk_ogg,
        'us_mp3':us_mp3,
        'us_ogg':us_ogg}

df=pd.DataFrame(fields)
df.to_csv('oxford.csv',index=False)
df.to_json('oxford.json', orient = 'records',indent=4)

