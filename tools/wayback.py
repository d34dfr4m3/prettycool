#!/usr/bin/python3
import requests
import sys
import json
import threading
import time

def check_logFile(LOGFILE):
  print("do something here to check if the logfile already exist")

def check(path,output):
  statusCode=['200','302']
  try:
    check = requests.get(path)
    if check.status_code in statusCode:
      print('[-] URL: {} Returns:{}'.format(path,check.status_code))
      output.write(path+'\n')
      return True
    else: 
      print('[-] URL: {} Returns:{}'.format(path,check.status_code))
  except Exception as error:
    print("[+] Check Function error: {}".format(error))
    return False
    
header={"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0",
        "Referer":'http://duckduckgo.com'
        }

#domain=sys.argv[1]
LOGFILE=domain+'_wbm'
#check_logFile(LOGFILE)
url="http://web.archive.org/web/timemap/json?url={}/&fl=timestamp:4,original&matchType=prefix&filter=statuscode:200&collapse=urlkey&collapse=timestamp:4".format(domain)
payload=requests.get(url,headers=header)
data=json.loads(payload.text)
output=open(LOGFILE,'a')
del data[0]
urlList=[]
for url in range(len(data)):
  if data[url][1] not in urlList:
    urlList.append(data[url][1])

print("[-] Found {} urls.".format(len(urlList)))
for url in range(len(urlList)):
  path=(urlList[url])
  threading.Thread(target=check,args=[path,output]).start()
  time.sleep(0.5)
output.close()

