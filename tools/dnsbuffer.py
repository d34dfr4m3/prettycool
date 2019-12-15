#!/usr/bin/python3
import requests
import json


def getHosts(domainName):
  hosts_results={}
  url='https://dns.bufferover.run/dns?q='+domainName
  data=requests.get(url).json()
  hosts=data['FDNS_A']
  for host in range(len(hosts)):
    ip,hostname=hosts[host].split(',')
    #print("[DNSBUFFER] ipAddress: %s Hostname: %s" %(ip,hostname))
    hosts_results[hostname]=ip
  return hosts_results
