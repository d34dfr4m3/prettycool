#!/usr/bin/python3
import requests
class my_certspotter:
  def __init__(self,target_domain,db):
    self.target_domain = target_domain
#    self.url = "https://certspotter.com/api/v1/certs?domain=%s" %(self.target_domain)
    self.url = "https://api.certspotter.com/v1/issuances?domain=%s&expand=dns_names&expand=issuer" %(self.target_domain)
    self.hc_url = "https://certspotter.com/"
    self.visible_name = "CERTSPOTTER" 

  def health_check(self):
    print("[-] HEALTH CHECK - %s" %(self.visible_name))
    check_reachable = requests.get(self.hc_url)
    if check_reachable.status_code == 200:
      print("[!] %s IS REACHABLE - Status code: %s" %(self.visible_name,check_reachable.status_code))
      return True
    else: 
      print("[!] %s IS NOT REACHABLE - Status code: %s" %(self.visible_name,check_reachable.status_code))

  def discovery(self):
    print("[-][STARTING CERTSPOTTER] Target %s" %(self.target_domain))
    target_list=[]
    try:
      data = requests.get(self.url)
      if data.status_code == 429:
        http_error = data.json()['message']
        print("[CERTSPOTTER] HTTP ERROR: %s" % (http_error))
        return False # wtf
    except Exception as error:
      print("[CERTSPOTTER] ERROR: %s" % (error))
    payload=data.json()
    for domains in range(len(payload)):
      dnsNamesList = payload[domains]['dns_names']
      for i in range(len(dnsNamesList)):
        hostname=dnsNamesList[i]
        if not '*' in hostname:
          if self.target_domain in hostname and self.target_domain not in target_list:
            target_list.append(hostname)
            print("[+][CERTSPOTTER] HOSTNAME: %s" %(hostname))
  #          avoidDuplicata(hostname)

if __name__ == "__main__":
  import sys
  ctp = my_certspotter(sys.argv[1])
  ctp.health_check()
  ctp.discovery()
