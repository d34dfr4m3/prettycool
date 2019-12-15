#!/usr/bin/python3
import requests

def check_honeypot(ipAddress):
  url='https://api.shodan.io/labs/honeyscore/'
  key='SHODANKEY'
  check=requests.get(url+ipAddress+'?key='+key)
  if check.status_code == 200: 
    honeyInd=float(check.text)
    if honeyInd == 1:
      print("It is a HoneyPot")
    elif honeyInd >= 0.5:
      print("%50")
    elif honeyInd == 0:
      print('is not a honeypot')
    print("honeyscore: {}".format(honeyInd))


import sys
check_honeypot(sys.argv[1])

