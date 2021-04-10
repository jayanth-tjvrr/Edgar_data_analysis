

import pandas as pd
import requests
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from bs4 import BeautifulSoup
import re
import nltk

nltk.download('punkt')
nltk.download("stopwords")

df = pd.read_excel('cik_list.xlsx')

df

y = 'https://www.sec.gov/Archives/'
links = [y+x for x in df['SECFNAME']]

links

reports = []
for url in links:
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, "html.parser")
    reports.append(soup.get_text())

print(f'Total {len(reports)} reports saved')

len(links)

sections = ["Management's Discussion and Analysis",
            "Quantitative and Qualitative Disclosures about Market Risk\n",
            "Risk Factors\n"]
caps = [x.upper() for x in sections]

caps.extend(sections)

caps

with open('StopWords_Generic.txt','r') as f:
    stop_words = f.read()

stop_words = stop_words.split('\n')
print(f'Total number of Stop Words are {len(stop_words)}')

master_dic = pd.read_excel('LoughranMcDonald_MasterDictionary_2018.xlsx')
master_dic.head()

positive_dictionary = [x for x in master_dic[master_dic['Positive'] != 0]['Word']]

negative_dictionary = [x for x in master_dic[master_dic['Negative'] != 0]['Word']]

print(f"Total positve words in dictionary are {len(positive_dictionary)}")
print(f"Total negative words in dictionary are {len(negative_dictionary)}")

uncertainity = pd.read_excel('uncertainty_dictionary.xlsx')
uncertainity_words = list(uncertainity['Word'])

constraining = pd.read_excel('constraining_dictionary.xlsx')
constraining_words = list(constraining['Word'])

def remove_stopwords(words, stop_words):
    return [x for x in words if x not in stop_words]
    
def countfunc(store, words):
    score = 0
    for x in words:
        if(x in store):
            score = score+1
    return score

def sentiment(score):
    if(score < -0.5):
        return 'Most Negative'
    elif(score >= -0.5 and score < 0):
        return 'Negative'
    elif(score == 0):
        return 'Neutral'
    elif(score > 0 and score < 0.5):
        return 'Positive'
    else:
        return 'Very Positive'
    

def polarity(positive_score, negative_score):
    return (positive_score - negative_score)/((positive_score + negative_score)+ 0.000001)
     

def subjectivity(positive_score, negative_score, num_words):
    return (positive_score+negative_score)/(num_words+ 0.000001)

def syllable_morethan2(word):
    if(len(word) > 2 and (word[-2:] == 'es' or word[-2:] == 'ed')):
        return False
    
    count =0
    vowels = ['a','e','i','o','u']
    for i in word:
        if(i.lower() in vowels):
            count = count +1
        
    if(count > 2):
        return True
    else:
        return False
    
def fog_index_cal(average_sentence_length, percentage_complexwords):
    return 0.4*(average_sentence_length + percentage_complexwords)

col = ['mda','qqdmr','rf']
var = ['positive_score',
      'negative_score',
      'polarity_score',
      'average_sentence_length',
      'percentage_of_complex_words',
      'fog_index',
      'complex_word_count',
      'word_count',
      'uncertainity_score',
      'constraining_score',
      'positive_word_proportion',
      'negative_word_proportion',
      'uncertainity_word_proportion',
      'constraining_word_proportion']


for c in col:
    for v in var[:-1]:
        df[c+'_'+v] = 0.0

df['constraining_words_whole_report'] = 0.0

df

s_map = {0:'mda',1:'qqdmr',2:'rf'}

for i in range(len(links)):
  z = reports[i]
  z = re.sub('Reports on Form 8-K','FINANCIAL STATEMENT SCHEDULES AND REPORTS',z)
  y = re.search('TABLE OF CONTENTS',z)
  h = re.search('FINANCIAL STATEMENT SCHEDULES AND REPORTS',z)
  if y and h:
    start,end = y.span()
    start1,end1 = h.span()
    content = z[start:end1]
    z = z.replace(content," ")
    for j in range(3):
      x = re.search('ITEM\s+[\d]\(*[A-Za-z]*\)*.*\s+\-*\s*'+caps[j], z)
      if x:
        start,end = x.span()
        g = z[start:].split('ITEM')[1]
        words = word_tokenize(g)
        num_words = len(words)
        positive_score = countfunc(positive_dictionary, words)
        negative_score = countfunc(negative_dictionary, words)
        polarity_score = polarity(positive_score, negative_score)
        subjectivity_score = subjectivity(positive_score, negative_score, num_words)
        sentences = sent_tokenize(content)
        num_sentences = len(sentences)
        average_sentence_length = num_words/num_sentences
        num_complexword =0
        uncertainity_score = 0
        constraining_score = 0
                
        for word in words:
            if(syllable_morethan2(word)):
                num_complexword = num_complexword+1
                        
            if(word in uncertainity_words):
                uncertainity_score = uncertainity_score+1
                        
            if(word in constraining_words):
                constraining_score = constraining_score+1
        percentage_complexwords = num_complexword/num_words
        fog_index = fog_index_cal(average_sentence_length, percentage_complexwords)
        positive_word_proportion = positive_score/num_words
        negative_word_proportion = negative_score/num_words
        uncertainity_word_proportion = uncertainity_score/num_words
        constraining_word_proportion = constraining_score/num_words
        df.at[i,s_map[j]+'_positive_score'] = positive_score
        df.at[i,s_map[j]+'_negative_score'] = negative_score
        df.at[i,s_map[j]+'_polarity_score'] = polarity_score
        df.at[i,s_map[j]+'_average_sentence_length'] = average_sentence_length
        df.at[i,s_map[j]+'_percentage_of_complex_words'] = percentage_complexwords
        df.at[i,s_map[j]+'_fog_index'] = fog_index
        df.at[i,s_map[j]+'_complex_word_count'] = num_complexword
        df.at[i,s_map[j]+'_word_count'] = num_words
        df.at[i,s_map[j]+'_uncertainity_score'] = uncertainity_score
        df.at[i,s_map[j]+'_constraining_score'] = constraining_score
        df.at[i,s_map[j]+'_positive_word_proportion'] = positive_word_proportion
        df.at[i,s_map[j]+'_negative_word_proportion'] = negative_word_proportion
        df.at[i,s_map[j]+'_uncertainity_word_proportion'] = uncertainity_word_proportion
        df.at[i,s_map[j]+'_constraining_word_proportion'] = constraining_word_proportion

    constraining_words_whole_report = 0
    tokenized_report_words = word_tokenize(reports[i])
    report_words = remove_stopwords(tokenized_report_words, stop_words)
    for word in report_words:
        if word in constraining_words:
            constraining_words_whole_report = 1+ constraining_words_whole_report
    df.at[i,'constraining_words_whole_report'] = constraining_words_whole_report

df.to_excel('output.xlsx')

