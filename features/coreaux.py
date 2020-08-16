#!/usr/bin/python3
import os
class core_utils:
  def __init__(self):
    self.name = "PRETTYCOOL" 

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
    pid=os.system('ps -C mysqld 1>/dev/null')
    if pid == 0:
      print("[!!] Database is running, ready to kill some bytes!")  
      return True
    elif pid != 0: 
      print("[!!] Database is not running")


  def loadKeys(self): ## Search in the database for keys, if not, search for new keys in the key file
    # Search in the database for keys. 

    # Then, read the key file, if got keys, add to the database. 
    print("[!] Loading keys")
    apiFile = open("keys/api_creds","r")
    for line in apiFile:
      apiName,value = line.split(':')
      if apiName == 'shodan_key':
        shodan_key = value.replace('\n','').strip("'")
        print("[-] Shodan key loaded: %s" %(shodan_key))
      elif apiName == 'censys_UID':
        global censys_UID
        censys_UID=value.replace('\n','').strip("'")
        print("[-] Censys UID loaded: %s " %(censys_UID))
      elif apiName == 'censys_SECRET':
        global censys_SECRET
        censys_SECRET=value.replace('\n','').strip("'")
        print("[-] Censys Secreted loaded: %s" %(censys_SECRET))
      elif apiName == 'securitytrails':
        global securitytrails_KEY
        securitytrails_KEY=value.replace('\n','').strip("'")
        print("[-] SecurityTrails key loaded %s" %(securitytrails_KEY))
      elif apiName == 'greyHat':
        global greyHat
        greyHat=value.replace('\n','').strip("'")
        print("[-] greyHat key loaded: %s " %(greyHat))

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



