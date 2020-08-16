#!/usr/bin/python3
# Python modules 
import sys


# Control Modules / Report modules
from features import db_controler
from features import report_maker
from features import coreaux


# Auxiliary modules
from features import net_misc 

# Host Discovery 
from features import virustotal
from features import certspotter
from features import dnsbuffer 
from features import securitytrails 
from features import prettycertsh
from features import dnsbuffer 


# Service Enum 
#from features import prettyshodan
#from features import spyse 
#from features import masscan 
#from features import prettycensys
# from features import dnsdumpster -> Not ready

# Intel 
from features import awsSearch # or awsSearch_v2 or grayHatWarfare ?
from features import prettypastebin

# Fingerprint/Service Enum
from features import wayback 



def intel():
  #Pastebin Search
  pasteFounded=pastebin(tgt)

### Recon Passivo Footprint
def discovery(db,target_domain):
# New code
  vt = virustotal.hosts(db,target_domain)
  if vt.health_check():
    vt.enum()

#  ctp = certspotter.my_certspotter(target_domain,db)
#  if ctp.health_check():
#    ctp.discovery()
  
#  dnb = dnsbuffer.dnsbuffer(target_domain,db)
#  if dnb.health_check():
#    dnb.discovery()

#  st=securitytrails.securitytrails(key,target_domain,db)
#  if st.health_check():
#    st.discovery()


#  dnb = dnsbuffer(sys.argv[1])
#  if dnb.health_check():
    

#  vt=hosts(target_domain)
#  vt.health_check()
#  vt.enum()

# Old Code
#  try:
#    spyse_subdomains(tgt)
#  except Exception as Error:
#    print("[-] Spyse Error: " + str(Error))

#  securitytrails(tgt)
#  virustotal(tgt)
#  crtsh(tgt)
#  certspotter(tgt)
  ## dnsbuffer retorna com endereços IPv4, melhor ao inves de usar listas, consumir direto do banco
#  dnsbuffer_hosts=dnsbuffer.getHosts(tgt)
#  for dnsbuffer_host in dnsbuffer_hosts:
#    ipAddress=dnsbuffer_hosts[dnsbuffer_host]
#    avoidDuplicata(dnsbuffer_host)
#    db_controler.hostAdd(ipAddress,tgt,dnsbuffer_host)

# Add a new domain in the database with status not running, then check for domains with this status and run


coreutils = coreaux.core_utils()
coreutils.banner()
coreutils.health_check()
coreutils.loadKeys()


domain_name = sys.argv[1]
db = db_controler.db_contrl()
db.load_cred()
db.domainAdd(domain_name)
rpt = report_maker.report(db)
domainList = rpt.listDomains()
if domain_name in domainList:
  discovery(db,domain_name)
else:
  print("[*] Target domain not found")


