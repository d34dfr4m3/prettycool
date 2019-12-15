#!/usr/bin/python3
import requests
import json


def getHosts(domainName):
  hosts_results={}
  url='https://dns.bufferover.run/dns?q='+domainName
  data=requests.get(url)
  if data.status_code == 200:
    datajson=data.json()
    hosts=datajson['FDNS_A']
    if type(hosts) == type(None):
      for error in datajson['Meta']['Errors']:
        print("[DNSBUFFER][ERROR] %s Query: %s" %(error,domainName))
      return False
    for host in range(len(hosts)):
      ip,hostname=hosts[host].split(',')
      print("[DNSBUFFER] ipAddress: %s Hostname: %s" %(ip,hostname))
      hosts_results[hostname]=ip
    return hosts_results

if __name__ == "__main__":
  import sys
  domainName = sys.argv[1]
  getHosts(domainName)

