#!/usr/bin/python3
#https://buckets.grayhatwarfare.com/apiDoc
import requests
import sys
import json

def searchGo(domainName,keyword,key):
  global buckets
  print("[-] Searching for string: {}".format(keyword))
  header = {'User-Agent': 'curl/7.58.0',
            'Accept':'*/*'} 
  URL="https://buckets.grayhatwarfare.com/api/v1/buckets/0/1000?access_token="+key+'&keywords='+keyword
  data = requests.get(URL,headers=header)
  buckets_count=data.json()['buckets_count']
  if buckets_count == 0:
    print("[*] No buckets found")
    return False
  else:
    for ids in range(len(data.json()['buckets'])):
      bucket_id=data.json()['buckets'][ids]['id']
      bucket_name=data.json()['buckets'][ids]['bucket']
      print('Bucket: {} ID: {}'.format(bucket_name,bucket_id))
      data_bucket = requests.get("https://buckets.grayhatwarfare.com/api/v1/bucket/{}/files/0/100?access_token={}".format(bucket_id,key),headers=header)
      buckets.append(bucket_name)
      if data_bucket.json()['results'] == 0:
        print('\t [-] Content of bucket id {} not found'.format(bucket_id))
      else:
        file_n=len(data_bucket.json()['files'])
        print('\t[-] Number of files: {}'.format(file_n))
#        for file_n in range(len(data_bucket.json()['files'])):
          #filename=data_bucket.json()['files'][file_n]['filename']
          #url=data_bucket.json()['files'][file_n]['url']
          #fullpatch=data_bucket.json()['files'][file_n]['fullPath']
          #print('\t[-] FullPatch: {}'.format(fullpatch))
    return buckets


def genWordlist(prekeyword):
  global wordlist
  badWords=['com','br','net','ru','job']
  chars=['-','_','+','','.']
  #- Search using the domain as keyword
  wordlist.append(prekeyword)
  #- Break the domain and start to try use words from the domain as keyword
  #- First use all words
  if '.' in prekeyword:
    words=prekeyword.split('.')
    for bad in badWords:
      if bad in words:
        words.remove(bad)
      for i in range(len(words)):
        for char in chars:
          prework=char.join(words)
          if prework not in wordlist:
            wordlist.append(prework)
      words.reverse()
      for i in range(len(words)):
        for char in chars:
          prework=char.join(words)
          if prework not in wordlist:
            wordlist.append(prework)
  #- Start to cut and do isolate search
      for word in words:
        if word not in wordlist:
          wordlist.append(word)

def awsSearchFor(domainName,key):
  global buckets
  buckets=[]
  global wordlist
  wordlist=[]
  print("[+] Bucket S3 Routing is starting")
  genWordlist(domainName)
  for keyword in wordlist:
    searchGo(domainName,keyword,key)
  return buckets
