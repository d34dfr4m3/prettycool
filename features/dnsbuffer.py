#!/usr/bin/python3
import requests
import json

class dnsbuffer:
  def __init__(self,target_domain,db):
    self.target_domain = target_domain
    self.url = 'https://dns.bufferover.run/dns?q=%s' %(target_domain)
    self.hc_url = 'https://dns.bufferover.run/'

  def health_check(self):
    print("[-] HEALTH CHECK - DNSBUFFER")
    check_reachable = requests.get(self.hc_url)
    if check_reachable.status_code == 200:
      print("[!] DNSBUFFER IS REACHABLE - Status code: %s" %(check_reachable.status_code))
      return True
    else: 
      print("[!] DNSBUFFER IS NOT REACHABLE - Status code: %s" %(check_reachable.status_code))

  def discovery(self):
    print("[+][STARTING DNSBUFFER] Target: %s" %(self.target_domain))
    hosts_results={}
    data=requests.get(self.url)
    if data.status_code == 200:
      datajson=data.json()
      hosts=datajson['FDNS_A']
      if type(hosts) == type(None):
        for error in datajson['Meta']['Errors']:
          print("[DNSBUFFER][ERROR] %s Query: %s" %(error,self.target_domain))
        return False
      for host in range(len(hosts)):
        ip,hostname=hosts[host].split(',')
        check_domain_fqdn='.'+self.target_domain
        if hostname.endswith(check_domain_fqdn):
          #Check if ip is a real IP, if not, resolve.
          print("[+][DNSBUFFER] HOSTNAME: %s ipAddress: %s" %(hostname,ip))
          # Write to database
    #      hosts_results[hostname]=ip The core will resolve. 
#      return hosts_results

if __name__ == "__main__":
  import sys
  dnb = dnsbuffer(sys.argv[1])
  dnb.health_check()
  dnb.discovery() 

#  dnsbuffer_hosts=dnsbuffer.getHosts(tgt)
#  for dnsbuffer_host in dnsbuffer_hosts:
#    ipAddress=dnsbuffer_hosts[dnsbuffer_host]
#    avoidDuplicata(dnsbuffer_host)
#    db_controler.hostAdd(ipAddress,tgt,dnsbuffer_host)

