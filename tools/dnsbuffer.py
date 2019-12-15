#!/usr/bin/python3
import requests
import json


def getHosts(domainName):
  url='https://dns.bufferover.run/dns?q='+domainName
  data=requests.get(url).json()
  hosts=data['FDNS_A']
  for host in range(len(hosts)):
    ip,hostname=hosts[host].split(',')
    print("IP: %s Hostname: %s" %(ip,hostname))



import sys
getHosts(sys.argv[1])



