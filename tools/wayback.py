#!/usr/bin/python3
import requests
import sys
import json
import threading
import time

def gowbm(webapp):
  if not webapp:
    return False
  print("[!][WAYBACKMACHINE] Starting Routine for : %s"%(webapp))
  global valid_urls
  valid_urls=[]
  header={"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0",
        "Referer":'http://duckduckgo.com'
        }
  url="http://web.archive.org/web/timemap/json?url={}/&fl=timestamp:4,original&matchType=prefix&filter=statuscode:200&collapse=urlkey&collapse=timestamp:4".format(webapp)
  try:
    payload=requests.get(url,headers=header)
    data=json.loads(payload.text)
  except Exception as error:
    print("[!][WAYBACKMACHINE] Error: %s"%(error))
  if data:
    del data[0]
    urlList=[]
    for url in range(len(data)):
      if data[url][1] not in urlList:
        urlList.append(data[url][1])

    print("[+][WAYBACKMACHINE] WebApp: {} Found: {} urls.".format(webapp,len(urlList)))
    for lurl in range(len(urlList)):
      path=(urlList[lurl])
      threading.Thread(target=check,args=[path]).start()
      time.sleep(0.5)
    return valid_urls

def check(path):
  global valid_urls
  statusCode=['200','201','202','302','301']
  try:
    check = requests.get(path)
    if check.status_code in statusCode:
      print('[-] URL: {} Returns:{}'.format(path,check.status_code))
      valid_urls.append(path)
    else: 
      pass
      print('[-] URL: {} Returns:{}'.format(path,check.status_code))
  except Exception as error:
    print("[!][WAYBACKMACHINE] Error: %s"%(error))
    pass
    #return False

if __name__ == "__main__":
  import sys
  webapp=sys.argv[1]
  gowbm(webapp)

