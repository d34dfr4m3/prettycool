#!/usr/bin/python3
import os
class core_utils:
  def __init__(self):
    self.name = "PRETTYCOOL" 
    self.vt_key = "" 
    self.sectrails_key = "" 
    self.shodan_key = "" 
    self.spyse_auth_token = "" 
    self.censys_uid = "" 
    self.censys_secret = "" 
    self.greyhat_key = "" 
    self.whoisfreaks_key = "" 

  def banner(self):
    print("""
                _   _          ____            _ 
 _ __  _ __ ___| |_| |_ _   _ / ___|___   ___ | |
| '_ \| '__/ _ \ __| __| | | | |   / _ \ / _ \| |
| |_) | | |  __/ |_| |_| |_| | |__| (_) | (_) | |
| .__/|_|  \___|\__|\__|\__, |\____\___/ \___/|_|
|_|                     |___/                    
          
                   - RedTeam/BugBounty Recon Tool! 
       https://github.com/d34dfr4m3/prettycool/
""")

# Health Check do core 
  def health_check(self):
    if os.geteuid() != 0: 
      print("[-] Error: You need to run this program with root, morty")
      exit(1)
    pid=os.system('pidof mariadbd')
    if pid == 0:
      print("[!!] Database is running, ready to kill some bytes!")  
      return True
    elif pid != 0: 
      print("[!!] Database is not running")
      exit(1) 


  def loadKeys(self): ## Search in the database for keys, if not, search for new keys in the key file
    # Search in the database for keys. 

    # Then, read the key file, if got keys, add to the database. 
    print("[!] Loading keys")
    apiFile = open("keys/api_creds","r")
    for line in apiFile:
      apiName,value = line.split(':')
      if apiName == 'shodan_key':
        self.shodan_key = value.replace('\n','').strip("'")
        print("[-] Shodan key loaded: %s" %(self.shodan_key))
      elif apiName == 'censys_UID':
        self.censys_uid = value.replace('\n','').strip("'")
        print("[-] Censys UID loaded: %s " %(self.censys_uid))
      elif apiName == 'censys_SECRET':
        self.censys_secret = value.replace('\n','').strip("'")
        print("[-] Censys Secreted loaded: %s" %(self.censys_secret))
      elif apiName == 'securitytrails':
        self.sectrails_key = value.replace('\n','').strip("'")
        print("[-] SecurityTrails key loaded %s" %(self.sectrails_key))
      elif apiName == 'spyse':
        self.spyse_auth_token = value.replace('\n','').strip("'")
        print("[-] Spyse Auth Token loaded %s" %(self.spyse_auth_token))
      elif apiName == 'greyHat':
        self.greyhat_key = value.replace('\n','').strip("'")
        print("[-] greyHat key loaded: %s " %(self.greyhat_key))
      elif apiName == 'virusTotal':
        self.vt_key=value.replace('\n','').strip("'")
        print("[-] Virus Total key loaded: %s " %(self.vt_key))
      elif apiName == 'whoisfreaks':
        self.whoisfreaks_key=value.replace('\n','').strip("'")
        print("[-] WhoisFreaks key loaded: %s " %(self.whoisfreaks_key))

class domain:
  def __init__(self):
    self.domain_name = "" 
    self.whois = ""
    self.lastUpdate = "" 
    self.createdAt = "" 
    
class host:
  def __init__(self):
    self.ip_address = ""
    self.domain_name = ""
    self.hostname = "" 
    self.geo_location = ""
    self.whois = ""  #ipOwner
    self.latitute = ""
    self.longitude = ""
    self.isp = ""
    self.os = ""
    self.org = ""
    self.asn = ""
    self.link = "" #?
    self.country_code = ""
    self.shodan_last_update = ""
    
class Port:
  def __init__(self):
    self.ip_address = ""
    self.port = ""
    self.protocol = ""
    self.banner = ""
    self.service = "" 
    self.hostname = ""

class Application: 
  def __init__(self):
    self.service = ""
    self.application_name = ""
    self.url = ""



