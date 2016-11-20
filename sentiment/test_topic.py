# Sharbatc
# Ines
# Corentin

# Simple program that demonstrates how to invoke Azure ML Text Analytics API: topic detection.
from urllib.request import urlopen, Request
import urllib
import sys
import base64
import json
import time

# Azure portal URL.
base_url = 'https://westus.api.cognitive.microsoft.com/'
# Your account key goes here.
account_key = '9cd819218d0849d0a9d43a7ce555f2f5'

headers = {'Content-Type':'application/json', 'Ocp-Apim-Subscription-Key':account_key, 'Accept':'application/json'}

# Path to file with JSON inputs.
file_path = 'data.txt'
f = open(file_path, 'r')
input_texts = f.read()

input_texts = input_texts.encode('utf-8') # why Python3, why? ;_;

# Start topic detection and get the URL we need to poll for results.
print('Starting topic detection.')
uri = base_url + 'text/analytics/v2.0/topics' # the Swiss canton
req = Request(uri, input_texts, headers)
response_headers = urlopen(req).info()
uri = response_headers['operation-location']

# Poll the service every few seconds to see if the job has completed.
while True:
	req = Request(uri, None, headers)
	response = urlopen(req)
	result = response.read()
	obj = json.loads(result)

	if (obj['status'].lower() == "succeeded"):
		break

	print('Request processing.')
	time.sleep(10)

print('Topic detection complete. Result:')
print(obj)
    