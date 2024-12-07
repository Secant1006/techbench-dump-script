#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import time
import json
import uuid
import requests

print('TechBench Dump Script', '2024/12/7', 'https://techbench.betaworld.cn/', '', sep='\n')

# Open JSON database
db_filename = 'dump.json'
db_loaded = False
data = {}
data['genTime'] = ''
data['productNumber'] = ''
data['products'] = {}
if os.path.exists(db_filename):
    with open(db_filename, 'r', encoding='utf-8') as file:
        try:
            data = json.load(file)
        except:
            db_loaded = False
        else:
            db_loaded = True

# Read arguments and determine starting point
start = 0
end = -1 # -1 if undetermined for now, will automatically detect later
if len(sys.argv) == 1:
    try:
        start = int(list(data['products'].keys())[-1]) + 1
    except:
        start = 0
elif len(sys.argv) == 3:
    try:
        start = int(sys.argv[1])
        end = int(sys.argv[2])
    except:
        print('Error: Invalid argument.')
        sys.exit(1)
    if start > end:
        print ('Error: Invalid argument.')
        sys.exit(1)
else:
    print('Error: Invalid argument.')
    sys.exit(1)
print('[INFO] Start dumping from ID: %d' % start)

# Dump
requests.packages.urllib3.disable_warnings()
cur = start - 1
count = 0
limit = 5
while True:
    if (end == -1 and count >= limit) or (end != -1 and cur >= end):
        print('[INFO] End dumping at ID: %d' % cur)
        break
    cur += 1

    # Send request
    sessionID = str(uuid.uuid4())
    try:
        response = requests.get(f'https://www.microsoft.com/software-download-connector/api/getskuinformationbyproductedition?profile=606624d44113&ProductEditionId={cur}&SKU=undefined&friendlyFileName=undefined&Locale=en-US&sessionID={sessionID}', headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'}, verify=False)
    except:
        print('[ERROR] Error sending request for ID:', cur)
        count += 1
        continue
    
    # Parsing response
    try:
        productInfo = json.loads(response.text)
    except:
        print('[ERROR] Error parsing response for ID:', cur)
        count += 1
        continue
    
    # Get product name
    try:
        name = productInfo['Skus'][0]['ProductDisplayName']
    except:
        print('[ERROR] No valid product info for ID:', cur)
        count += 1
        continue
    else:
        print(f'[INFO] ID: {cur}, name: {name}')
        data['products'][str(cur)] = name
        count = 0

# Sort
data['products'] = dict(sorted(data['products'].items(), key=lambda item: int(item[0])))

# Write output
try:
    with open(db_filename, 'w+', encoding='utf-8') as file:
        data['genTime'] = str(int(time.time()))
        data['productNumber'] = str(len(data['products']))
        json.dump(data, file)
except:
    print('[ERROR] Error writing output.')
else:
    print('[INFO] Finished writing output.')