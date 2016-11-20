# Sharbatc
# Ines
# Corentin

# For testing, as mentioned publicly in Microsoft Azure's testpage.
# Simple program that demonstrates how to invoke Azure ML Text Analytics API: key phrases, language and sentiment detection.
import urllib
from urllib.request import urlopen, Request
import sys
import base64
import json

# Azure portal URL.
base_url = 'https://westus.api.cognitive.microsoft.com/'
# Your account key goes here.
account_key = '9cd819218d0849d0a9d43a7ce555f2f5'

headers = {'Content-Type':'application/json', 'Ocp-Apim-Subscription-Key':account_key, 'Accept':'application/json'}
            
file_path = 'data.txt'
f = open(file_path, 'r')
input_texts = f.read()

input_texts = input_texts.encode() # why Python3, why? ;_;

# input_texts = urllib.parse.urlencode(input_texts) # why Python3, why? ;_;

num_detect_langs = 1;

# Detect key phrases.
batch_keyphrase_url = base_url + 'text/analytics/v2.0/keyPhrases'
req = Request(batch_keyphrase_url, input_texts, headers) 
response = urlopen(req).read().decode(); # why Python3, why? ;_;
obj = json.loads(response)
for keyphrase_analysis in obj['documents']:
    print('Key phrases ' + str(keyphrase_analysis['id']) + ': ' + ', '.join(map(str,keyphrase_analysis['keyPhrases'])))

# Detect language.
language_detection_url = base_url + 'text/analytics/v2.0/languages' + ('?numberOfLanguagesToDetect=' + num_detect_langs if num_detect_langs > 1 else '')
req = Request(language_detection_url, input_texts, headers)
response = urlopen(req).read().decode('utf-8') # why Python3, why? ;_;
obj = json.loads(response)
for language in obj['documents']:
    print('Languages: ' + str(language['id']) + ': ' + ','.join([lang['name'] for lang in language['detectedLanguages']]))

# Detect sentiment.
batch_sentiment_url = base_url + 'text/analytics/v2.0/sentiment'
req = Request(batch_sentiment_url, input_texts, headers) 
response = urlopen(req).read().decode('utf-8') # why Python3, why? ;_;
obj = json.loads(response)
for sentiment_analysis in obj['documents']:
    print('Sentiment ' + str(sentiment_analysis['id']) + ' score: ' + str(sentiment_analysis['score']))
    