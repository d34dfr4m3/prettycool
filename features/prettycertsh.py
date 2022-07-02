#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup

class my_crtsh:
  def __init__(self,target_domain):
    self.target_domain = target_domain
    self.url = "https://crt.sh/?q=%.{}".format(self.target_domain)
    self.health_url = "https://crt.sh/"
    self.name = "CRTSH" 

  def health_check(self):
    print("[-] HEALTH CHECK - %s" %(self.name))
    try_reach = requests.get(self.health_url)
    if try_reach.status_code == 200: 
      print("[!] %s IS REACHABLE - Status code: %s" %(self.name,try_reach.status_code))
      return True
    else:
      print("[!] %s IS NOT REACHABLE - Status code: %s" %(self.name,try_reach.status_code))

  def discovery(self): 
    print("[+][STARTING CRTSH] Target: %s " %(self.target_domain))
    data = requests.get(self.url)
    page = BeautifulSoup(data.text,'html.parser')
    badChars=['*',' ','crt.sh','%','Identity','LIKE',"'"] 
    target_list=[]
    for domain in page.find_all('td'):
      domaintxt = str(domain).replace('<br/>',',')
      if self.target_domain in domaintxt:
        hostname=domaintxt.split('>')[1].split("<")[0]
        if ',' in hostname: 
          for host in hostname.split(','):
            if not "*" in host and host not in target_list:
              target_list.append(host)
              print("[+][%s] HOSTNAME: %s" %(self.name,host))

        
if __name__ == "__main__":
  import sys
  crt = my_crtsh(sys.argv[1])
  crt.health_check()
  crt.discovery()
