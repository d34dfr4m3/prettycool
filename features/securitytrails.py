#!/usr/bin/python3
import requests
import json
class securitytrails:
  def __init__(self,key,target_host,db):
    self.key = key 
    self.target_host = target_host
    self.headers = headers={'apikey': self.key}
    self.url_health = "https://api.securitytrails.com/v1/account/usage"
    self.url_subdomain = 'https://api.securitytrails.com/v1/domain/%s/subdomains' %(self.target_host)
    
  def health_check(self):
    page = requests.get(self.url_health,headers=self.headers)
    if 'message' in page.json().keys():
      error=page.json()['message']
      print("[!!] SecurityTrails API issue: {}".format(error))
    else:
      left=page.json()['allowed_monthly_usage'] - page.json()['current_monthly_usage']
      print("[!!] SecurityTrails API is ready to rock with {} requests left".format(left))
      return True

  def discovery(self):
    print("[+][STARTING SECURITYTRAILS] Target: %s " %(self.target_host) )
    data = requests.get(self.url_subdomain,headers=self.headers)
    if data.status_code == 429:
        print("[!!] SecurityTrails API is out of credits or some stuff related with capitalism")
        return False ## why u put this shit here ?
    payload=data.json()
    for hosts in range(len(payload['subdomains'])):
      hostname=payload['subdomains'][hosts]+'.'+self.target_host
      print("[+][SECURITYTRAILS] HOSTNAME: %s" %(hostname))
      #avoidDuplicata(hostname)
      #avoidDuplicata(payload['subdomains'][hosts]+'.'+target)
# https://docs.securitytrails.com/reference/ping
# Company Info 
# https://api.securitytrails.com/v1/company/{domain} Premium 
# get https://api.securitytrails.com/v1/company/{domain}/associated-ips
# History
# DNS WHOIS
# Domains
## subdomains
## search
## associated domains


if __name__ == "__main__":
  import sys
  key = sys.argv[1]
  target_domain=sys.argv[2]
  st=securitytrails(key,target_domain)
  st.health_check()
  st.discovery()
