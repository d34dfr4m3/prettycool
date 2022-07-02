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
from features import whoisfreaks
from features import virustotal
from features import certspotter
from features import dnsbuffer 
from features import securitytrails 
from features import prettycertsh
from features import dnsbuffer 


# Service Enum 
from features import prettyshodan
from features import spyse 
#from features import masscan 
from features import prettycensys
# from features import dnsdumpster -> Not ready

# Intel 
from features import s3Search 
from features import prettypastebin

# Fingerprint/Service Enum
from features import wayback 

def intel(target_domain):
  print("STARTING INTEL ROUTINE")
  #Pastebin Search
#  pasteFounded=pastebin(tgt)
  search = prettypastebin.mypastebin(target_domain)
  if search.health_check():
    search.psbdmp()
# GreyHat Warfare
  s3s = s3Search.my_grayhatwarfare(target_domain,coreutils.greyhat_key)
  if s3s.health_check():
    s3s.s3SearchFor()

### Recon Passivo Footprint
def discovery(db,target_domain):
  print("[-] STARTING DISCOVERY ROUTINE")
## Censys
  cnsy=prettycensys.mycensys(coreutils.censys_uid,coreutils.censys_secret,target_domain)
  if cnsy.health_check():
    cnsy.discovery()

## Shodan
  shd = prettyshodan.myshodan(target_domain,coreutils.shodan_key)
  if shd.health_check():
    shd.host_enum() # Host Enum
    shd.host_discovery() # Host discovery 

# New code OK  VirusTotal
  vt = virustotal.hosts(db,target_domain,coreutils.vt_key)
  if vt.health_check():
    vt.enum()

# CertSpotter OK 
  ctp = certspotter.my_certspotter(target_domain,db)
  if ctp.health_check():
    ctp.discovery()
 
# DnsBuffer   OK 
  dnb = dnsbuffer.dnsbuffer(target_domain,db)
  if dnb.health_check():
    dnb.discovery()

# Ready Security Trails
  st=securitytrails.securitytrails(coreutils.sectrails_key,target_domain,db)
  if st.health_check():
    st.discovery()

## Spyse health check??
### spyse.com returns 503 - https://www.reddit.com/r/OSINT/comments/tayfe2/spyse_is_shutting_down_are_there_any_alternatives/ 
#  spy = spyse.spyse(target_domain,coreutils.spyse_auth_token) 
#  if spy.health_check():
#    spy.discovery()

## Crtsh READY  
  crt = prettycertsh.my_crtsh(target_domain)
  if crt.health_check():
    crt.discovery()

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

# Starting DB controler and loading keys/tokens/creds
db = db_controler.db_contrl()
db.load_cred()
# Starting Domain Routine 
coreaux.Domain = sys.argv[1] 
wfks = whoisfreaks.my_whoisfreaks(coreutils.whoisfreaks_key,coreaux.Domain)
if wfks.health_check():
  wfks.get_whois()
# Add domain name to database
db.domainAdd(coreaux.Domain)
rpt = report_maker.report(db) #?? 
domainList = rpt.listDomains()# ?? 
if coreaux.Domain in domainList:
  discovery(db,coreaux.Domain)
  intel(coreaux.Domain)
else:
  print("[*] Target domain not found")
