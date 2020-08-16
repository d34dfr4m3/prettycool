#!/usr/bin/python3
import requests
import json
class hosts:
  def __init__(self, db, domain):
    self.target_domain = domain
    self.db = db
    self.url = 'https://www.virustotal.com/ui/domains/%s/subdomains?relationships=resolutions' %(self.target_domain)
    self.hc_url = 'https://www.virustotal.com/'
    self.headers={'User-Agent': 'curl/7.68.0',
                  'Accept' : '*/*'}


  def health_check(self):
    print("[-] HEALTH CHECK - VIRUSTOTAL")
    check_reachable = requests.get(self.hc_url,headers=self.headers)
    if check_reachable.status_code == 200:
      print("[!] VIRUSTOTAL IS REACHABLE - Status code: %s" %(check_reachable.status_code))
      return True
    else: 
      print("[!] VIRUSTOTAL IS NOT REACHABLE - Status code: %s" %(check_reachable.status_code))

  def enum(self):
    print("[+][STARTING - VIRUSTOTAL] Target: %s" %(self.target_domain))
    data = requests.get(self.url,headers=self.headers)
    if data.status_code != 200:
      print(data)
      return False
    payload = data.json()
    try:
      for ids in range(len(payload['data'])):
        hostname=payload['data'][ids]['id']
        print("[+][VIRUSTOTAL] HOSTNAME: %s" %(hostname))
        self.db.hostAdd(self.target_domain,hostname)
    except Exception as error:
      print("[!][ERROR VIRUSTOTAL] Error: %s" %(error))

if __name__ == "__main__":
  import sys
  target_domain=sys.argv[1]
  vt=hosts(target_domain)
  vt.health_check()
  vt.enum()
  
