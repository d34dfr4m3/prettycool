#!/usr/bin/python3
#https://buckets.grayhatwarfare.com/docs/api/v1
import requests
import sys
import json

class my_grayhatwarfare:
  def __init__(self,domain,key):
    self.key = key 
    self.target_domain = domain
    self.header = {'User-Agent': 'firefuck',
                    'Accept':'*/*'} 
    self.url = "https://buckets.grayhatwarfare.com/api/v1/buckets/0/1000?access_token={}&keywords={}"
    self.url_check = "https://buckets.grayhatwarfare.com/api/account?access_token=" 

  def health_check(self):
    check = requests.get(self.url_check+self.key)
    if check.status_code == 200:
      print("GreyHatWarfare ok")
      print(check.json())
      return True
    else:
      return False

  def searchGo(self,keyword):
    global buckets
    print("[-] Searching for string: {}".format(keyword))
    URL="https://buckets.grayhatwarfare.com/api/v1/buckets/0/1000?access_token="+self.key+'&keywords='+keyword
    try:
      data = requests.get(URL,headers=self.header)
      buckets_count=data.json()['buckets_count']
    except Exception as error:
      print("ERROR:{}".format(error))
      pass
    if buckets_count == 0:
      print("[*] No buckets found")
      return False
    else:
      for ids in range(len(data.json()['buckets'])):
        bucket_id=data.json()['buckets'][ids]['id']
        bucket_name=data.json()['buckets'][ids]['bucket']
        print('Bucket: {} ID: {}'.format(bucket_name,bucket_id))
        data_bucket = requests.get("https://buckets.grayhatwarfare.com/api/v1/bucket/{}/files/0/100?access_token={}".format(bucket_id,self.key),headers=self.header)
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


  def genWordlist(self):
    global wordlist
    badWords=['com','br','net','ru','job','gov']
    chars=['-','_','+','','.']
    #- Search using the domain as keyword
    wordlist.append(self.target_domain)
    #- Break the domain and start to try use words from the domain as keyword
    #- First use all words
    if '.' in self.target_domain:
      words=self.target_domain.split('.')
      for bad in badWords:
        if bad in words:
          words.remove(bad)
        for i in range(len(words)):
          for char in chars:
            prework=char.join(words)
            if prework not in wordlist:
              if len(prework) >= 3: 
                wordlist.append(prework)
        words.reverse()
        for i in range(len(words)):
          for char in chars:
            prework=char.join(words)
            if prework not in wordlist:
              if len(prework) >= 3: 
                wordlist.append(prework)
    #- Start to cut and do isolate search
        for word in words:
          if word not in wordlist:
              if len(word) >= 3: 
                wordlist.append(word)
            #CLear again the fucking list 
      for bad in badWords:
        if bad in wordlist:
          wordlist.remove(bad)

  def s3SearchFor(self):
    global buckets
    buckets=[]
    global wordlist
    wordlist=[]
    print("[+] Bucket S3 Routing is starting")
    self.genWordlist()
    for keyword in wordlist:
      self.searchGo(keyword)
    return buckets


if __name__ == "__main__":
  import sys
  target=sys.argv[1]
  key=sys.argv[2]
  s3s = my_grayhatwarfare(target,key)
  s3s.s3SearchFor()
