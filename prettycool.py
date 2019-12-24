#!/usr/bin/python3 
import requests
from bs4 import BeautifulSoup
import getopt
import socket
#import shodan
import sys
import json
import threading
import time
import os 
import subprocess
# Local Stuff 
from tools import db_controler
from tools import report_maker
from tools import awsSearch
from tools import spyse
from tools import dnsbuffer
from tools import wayback

global censys 
global shodan
global sectrial
global scanned
global domain
global CENSYS_DEAD
global done 
global wayback_scanned
wayback_scanned=[]
done = False
CENSYS_DEAD=False
scanned=[]
allTargets=[]
URLSPYSE='https://api.spyse.com/v1'
http_status_codes = {'400':'Maximum value for parameter exceeded / invalid or missing required parameters.',
                    '402':'Request limit exceeded',
                    '403':'Missing or invalid required parameter api_token.',
                    '500': 'Internal server error. We are aware of the error and are already working on fixing it. Sorry for inconvenience.'}


def genURL(url,port):
  if port == 80:
    burl='http://'+url
  elif port == 443:
    burl='https://'+url
  else:
    burl='http://'+url+':'+str(port)
    return burl

def check_banner(hostName,banner,port,ipAddress):
  if hostName in wayback_scanned:
    return False
  else:
    app_payload={}
    wayback_scanned.append(hostName)
    http_protocols=['http']
    waf_signature=['cloudflare']
    cdn_signature=['cloudFront']
    iaas_signature=['amazon']  
    if 'http' in banner.lower():
      print(banner)
      print("WAY BACK MACHINE")
      url=genURL(hostName, port)
      urls=wayback.gowbm(url)
      if urls:
        aux=0
        app_payload['url']=url
        app_payload['port']=port
        app_payload['hostName']=hostName
        app_payload['ipAddress']=ipAddress
        db_controler.appAdd(app_payload)
        for s_url in urls:                
          aux+=1
          app_payload['url']=s_url
          db_controler.appAddContent(app_payload)
        print("[+][WAYBACK] Done for Target %s, got %s urls" % (url,aux))

def checkDB():
  pid=os.system('ps -C mysqld &>/dev/null')
  if pid == 256:
    print("[!!] Database is not running")
    return False
  elif pid == 0: 
    print("[!!] Database is running, ready to kill some bytes!")  
    return True

def healthCheck():
  #Notes from fucked dev: Tenho vergonha dessa merda q eu escrevi
  #Censys api info
  # Todo: Check if api are reacheable trying to connect. 
  # And fuc, this code sucks bro, clean this shit 
  # Add database checker
  if os.geteuid() != 0: 
    print("[-] Error: You need to run this program with root, morty")
    exit(1)
  #if not checkDB():
  loadKeys()
  global censys_UID
  global censys_SECRET
#  URLS={'censys':
#          {'url_to_do_y':'url',
#            'url_to_do_x':'url'},
#          'shodan':{}
#          }
  API_URL = "https://censys.io/api/v1"
  page=requests.get(API_URL+"/account", auth=(censys_UID,censys_SECRET))
  left=int(page.json()['quota']['allowance'])-int(page.json()['quota']['used'])
  if left > 50:
    print("[!!] Censys API has only {} requests left".format(str(left)))
  elif left > 20:
    print("[!!] Censys API has only {} requests left".format(str(left)))
  elif left > 10:
    print("[!!] Censys API has only {} requests left".format(str(left)))
  elif left <= 0:
    global CENSYS_DEAD
    CENSYS_DEAD = True
    # Pick up another key right guys! 
    print("[!!] Censys API has no credits to use")
  else:
    print("[!!] Censys API is ready to rock with {} requests left".format(left))
    
  #Shodan api info 
  global shodan_key
  page=requests.get('https://api.shodan.io/api-info?key='+shodan_key)
  left=int(page.json()['unlocked_left'])
  if left < 50:
    print("[!!] Shodan API has only {} requests left".format(str(left)))
  elif left < 20:
    print("[!!] Shodan API has only {} requests left".format(str(left)))
  elif left < 10:
    print("[!!] Shodan API has only {} requests left".format(str(left)))
  else:
    print("[!!] Shodan API is ready to rock with {} requests left".format(left))
 #Security Trails
  global securitytrails_KEY
  headers={'apikey': securitytrails_KEY}
  page = requests.get('https://api.securitytrails.com/v1/account/usage',headers=headers)
  if 'message' in page.json().keys():
    error=page.json()['message']
    print("[!!] SecurityTrails API issue: {}".format(error))
    return False
  else:
    left=page.json()['allowed_monthly_usage'] - page.json()['current_monthly_usage']
    print("[!!] SecurityTrails API is ready to rock with {} requests left".format(left))

def shodan(target,hostname):
  global shodan_key
  host_update={}
  try:
    data = requests.get('https://api.shodan.io/shodan/host/'+target+'?key='+shodan_key)
    payload=data.json()
  except Exception as err:
    print("\t[SHODAN]ERROR: Miss or error: {}".format(err))
  if not len(payload) > 0:
    return False
  last_update=payload['last_update'] if 'last_update' in payload else False
  if not 'data' in payload:
    return False
  payload_data=payload['data']
  for i in range(len(payload_data)):
    port=payload_data[i]['port'] if 'port' in payload_data[i] else False
    product=payload_data[i]['product'] if 'product' in payload_data[i] else False
    banner=payload_data[i]['data'] if 'data' in payload_data[i] else False
    ops=payload_data[i]['os'] if 'os' in payload_data[i] else False
    isp=payload_data[i]['isp'] if 'isp' in payload_data[i] else False
    org=payload_data[i]['org'] if 'org' in payload_data[i] else False
    asn=payload_data[i]['asn'] if 'asn' in payload_data[i] else False
    version=payload_data[i]['version'] if 'version' in payload_data[i] else False
    link=payload_data[i]['link'] if 'link' in payload_data[i] else False
    if '_shodan' in payload_data[i]:
      payload_shodan=payload_data[i]['_shodan']
      module=payload_shodan['module'] if 'module' in payload_shodan else False 
    if 'location' in payload_data[i]:
      payload_location=payload_data[i]['location']
      country_code=payload_location['country_code'] if 'country_code' in payload_location else False
      longitude=payload_location['longitude'] if 'longitude' in payload_location else False
      latitude=payload_location['latitude'] if 'latitude' in payload_location else False
      
    print('[*][SHODAN] Last Update for %s : %s' % (hostname,last_update))
    #print("\t[+][SHODAN] OS: {} ISP: {} Org: {} ASN: {} link: {}".format(ops,isp,org,asn,link))
    #print("\t[+][SHODAN] Country: {} Longitude: {} Latitude: {}".format(country_code,longitude,latitude))
    #HOST UPDATE HERE DBCONTROLER
    host_update['hostName']=hostname
    host_update['country_code']=country_code
    host_update['latitude']=latitude
    host_update['longitude']=longitude
    host_update['os']=ops
    host_update['isp']=isp
    host_update['asn']=asn
    host_update['link']=link
    host_update['shodan_last_update']=last_update
    db_controler.hostUpdate(host_update)
    port_service=str(product)+' '+str(version)
    port_module=str(port)+'/'+str(module)

    if 'http' in payload_data[i]:
      payload_http=payload_data[i]['http']
      securitytxt=payload_http['securitytxt'] if 'securitytxt' in payload_http else False
      title=payload_http['title'] if 'title' in payload_http else False
      sitemap_hash=payload_http['sitemap_hash'] if 'sitemap_hash' in payload_http else False
      robots=payload_http['robots'] if 'robots' in payload_http else False
      html=payload_http['html'] if 'html' in payload_http else False
      location_url=payload_http['location'] if 'location' in payload_http else False
      server=payload_http['server'] if 'server' in payload_http else False
      host_http=payload_http['host'] if 'host' in payload_http else False
      if port == 80: 
          url_path='http://{}{}'.format(host_http,location_url)
      elif port == 443:
          url_path='https://{}{}'.format(host_http,location_url)
      else:
          url_path='http://{}:{}{}'.format(host_http,port,location_url)

      print("\t\t[+][SHODAN] - WebApp found Title:{} URL: {}:{}{} Service:{}".format(title,host_http,port,location_url,server))
    #  print("\t\t\t[-] Securitytxt:  {} Sitemap: {}".format(securitytxt,sitemap_hash))
    #  print("\t\t\t[-] Robots:  {}".format(robots))
    #  print("\t\t\t{}".format(html))
    #Insert into tb_application
      app_payload={}
      app_payload['port']=port
      app_payload['applicationName']=title
      app_payload['hostName']=hostname
      app_payload['url']=url_path
      app_payload['ipAddress']=target
      app_payload['service']=server
      db_controler.appAdd(app_payload)
      #Insert into tb_applicationContent
      app_payload['sitemap_hash']=sitemap_hash
      if robots: 
        app_payload['url']=url_path+'robots.txt'
        #if app_payload['url'].split('/')[-1].split('.')dd[-1]:
        #fileExtension=app_payload['url'].split('.')[-1]
        #app_payload['fileExtension']=fileExtension
        app_payload['page_content']=robots
        l1=banner.splitlines(1)[0]
        status_code=l1.split(' ')[1]
        app_payload['status_code']=status_code
        db_controler.appAddContent(app_payload)
      if html:
        app_payload['url']=url_path
        app_payload['page_content']=html
        l1=banner.splitlines(1)[0]
        status_code=l1.split(' ')[1]
        app_payload['status_code']=status_code
        db_controler.appAddContent(app_payload)

    #print("\t[+][SHODAN] OS: {} ISP: {} Org: {} ASN: {} link: {}".format(port_module,port_service,ops,isp,org,asn,link))
    #print('\t[+][SHODAN] Open Port: {} Product: {}  \n\t\t Banner: {}'.format(port,product,banner))
    db_controler.portAdd(target,port,hostname,module,banner,port_service)
    check_banner(hostname,banner,port,ipAddress)

def resolve(target):
  try:
    return socket.gethostbyname(target)
  except Exception as error:
     return False

def certspotter(target):
  print("[+] Searching in Certspotter")
  target_list=[]
  try:
    data = requests.get("https://certspotter.com/api/v0/certs?domain="+target)
    if data.status_code == 429:
      print(data.json()['message'])
      return False
  except Exception as error:
    print("[CERTSPOTTER] ERROR: %s" % (error))
  payload=data.json()
  for domains in range(len(payload)):
    dnsNamesList = payload[domains]['dns_names']
    for i in range(len(dnsNamesList)):
      hostname=dnsNamesList[i]
      if not '*' in hostname:
        if target in hostname and target not in target_list:
          target_list.append(hostname)
          print("[+][CERTSPOTTER] HOSTNAME: %s" %(hostname))
          avoidDuplicata(hostname)

def avoidDuplicata(target):
    # This shit code here will in the future control the data I/O to database. 
  global allTargets
  global domain
  # Check the escope
  if domain in target:
    if target not in allTargets:
      allTargets.append(target)
      return True
    else:
      return False
  
def banner():
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

def censys_api(ipAddress,hostName): 
  global censys_UID
  global censys_SECRET
  global CENSYS_DEAD
  if CENSYS_DEAD:
    return False
  API_URL = "https://censys.io/api/v1"
  web_protocols=['http','https']
  auth = requests.get(API_URL + "/data", auth=(censys_UID,censys_SECRET))
  if auth.status_code != 200:
      print("[+] Auth Error: ", auth.json()['error'])
      CENSYS_DEAD=True
  else:
    params={'query':ipAddress, 'page':10}
    try: 
      page=requests.post(API_URL+"/search/ipv4", json=params,auth=(censys_UID,censys_SECRET))
      num_results = page.json()['metadata']['count']
      if num_results > 0:
        page=requests.get(API_URL+"/view/ipv4/"+ipAddress, auth=(censys_UID,censys_SECRET))
        for protocol in range(len(page.json()['protocols'])):
          port = page.json()['protocols'][protocol].split('/')[0]
          proto = page.json()['protocols'][protocol].split('/')[1]
          if proto in web_protocols:
            if 'title' in page.json()[port][proto]['get'].keys():
              title=page.json()[port][proto]['get']['title']
              protocol=page.json()['protocols'][protocol]
              print("\t[+] Protocol: {}  Title: {} ".format(page.json()['protocols'][proto], title))
            else:
              print("\t[+] Protocol: {}".format(page.json()['protocols'][protocol]))
      db_controler.portAdd(ipAddress,port,hostName,protocol)
    except Exception as error: 
      print("[!} Error Censys:", str(error))

def crtsh(target): 
  print("[+] Searching in crtsh")
  data = requests.get('https://crt.sh/?q=%.'+target)
  page = BeautifulSoup(data.text,'html.parser')
  badChars=['*',' ','crt.sh','%','Identity','LIKE',"'"] 
  target_list=[]
  for domain in page.find_all('td'):
    clean=True
    domaintxt = domain.get_text()
    if target in domaintxt:
      hostname=domaintxt.split('>')[0].split('<')[0]
      if not len(hostname) >=100:
        for badchar in badChars:
          if badchar in hostname:
            clean=False
        if hostname not in target_list and target in hostname and clean:
          target_list.append(hostname)
          print("[+][CRTSH] HOSTNAME: %s" %(hostname))
          avoidDuplicata(hostname)

def spyse_ip(ip,hostName):
  data = requests.get(URLSPYSE+'/ip-port-lookup?q={}&page={}'.format(ip,'1'))
  if data.status_code in http_status_codes.keys():
    print('[!!] Error - {}'.format(http_status_codes))
  elif len(data.json()) == 0:
    return False
  for ips in range(len(data.json())):
    ipAddress=data.json()[ips]['ip']['ip']
    print("[-][SPYSE] Hostname: {} ipAddress: {}".format(hostName,ipAddress))
    for ports in range(len(data.json()[ips]['iplList'])):
      data_json_ports=data.json()[ips]['iplList'][ports]
      if len(data_json_ports) > 0:
        try:
          port=data_json_ports['port'] if 'port' in data_json_ports else 'Null'
          banner=data_json_ports['banner'] if 'banner' in data_json_ports else 'Null'
          banner_base64=data_json_ports['banner_base64'] if 'banner_base64' in data_json_ports else 'Null'
          print("\t[-][SPYSE] Port OPEN {} ".format(port))
          if 'protocol' in data_json_ports:
            if len(data_json_ports['protocol']) > 0:
              data_protocol=data_json_ports['protocol']
              protocol=data_protocol['name'] if 'name' in data_protocol else 'Null'
              protocol_description=data_protocol['description'] if 'description' in data_protocol else 'Null'
              print("\t[-][SPYSE] Protocol: {} Description: {} ".format(protocol,protocol_description))
          if 'service' in data_json_ports:
            if len(data_json_ports['service']) > 0:
              data_service=data_json_ports['service']
              service=data_service['name'] if 'name' in data_service else 'Null'
              service_description=data_service['description'] if 'description' in data_service else 'Null'
              print("\t[-][SPYSE] Service: {} Description: {} ".format( service,service_description))

        #print("\t[-][SPYSE] Port {}  Proto: {} \n\t\tBanner: {} ".format(port,protocol,banner))
          db_controler.portAdd(ipAddress,port,hostName,protocol,banner)
          check_banner(hostName,banner,port,ipAddress)
        except Exception as Error:
          print("Error in Spyse_IP: %s" % (Error))

def pastebin(target):
  pasteList={}
  print("[!] Starting Pastebin Routine: Target {}".format(target))
  data = requests.get("https://psbdmp.ws/api/search/"+target)
  payload = data.json()
  for ids in range(len(payload['data'])):
     check = requests.get('https://pastebin.com/'+payload['data'][ids]['id'])
     if check.status_code == 200:
       page = BeautifulSoup(check.text,'html.parser')
       url='https://pastebin.com/'+str(payload['data'][ids]['id'])
       title=page.title.get_text()
       date=page.findAll('span',limit=11)[10].contents[0]
       print('[!][PSBDMP] Found: {} Date: {} Title: {}'.format(url,date,title))
       try:
         db_controler.pasteAdd(target,url,title,date)
       except Exception as error:
         print("Pastebin error: {}".format(error))
       pasteList[url]={date:title}
  return pasteList

def virustotal(target):
  print("[+] Searching in VirulTotal")
  data = requests.get('https://www.virustotal.com/ui/domains/'+target+'/subdomains?relationships=resolutions')
  payload = data.json()
  for ids in range(len(payload['data'])):
    hostname=payload['data'][ids]['id']
    print("[+][VIRUSTOTAL] HOSTNAME: %s" %(hostname))
    avoidDuplicata(hostname)
    #avoidDuplicata(payload['data'][ids]['id'])

def securitytrails(target):
  print("[+] Searching in SecurityTrails")
  global securitytrails_KEY
  headers={'apikey': securitytrails_KEY}
  data = requests.get("https://api.securitytrails.com/v1/domain/"+target+'/subdomains', headers=headers)
  if data.status_code == 429:
      print("[!!] SecurityTrails API is out of credits or some stuff related with capitalism")
      return False
  payload=data.json()
  for hosts in range(len(payload['subdomains'])):
    hostname=payload['subdomains'][hosts]+'.'+target
    print("[+][SECURITYTRAILS] HOSTNAME: %s" %(hostname))
    avoidDuplicata(hostname)
    #avoidDuplicata(payload['subdomains'][hosts]+'.'+target)

def process(host):
  global domain
  ipAddress = resolve(host)
  db_controler.hostAdd(ipAddress,domain,host)
  if ipAddress: 
    print("[+] Found: {} ipAddress: {}".format(host,ipAddress))
    if hostScanControl(ipAddress):
      spyse_ip(ipAddress,host)
      shodan(ipAddress,host)
    #  runMasscan(host,ipAddress)
      if not CENSYS_DEAD:
        censys_api(ipAddress,host)
    
  else:
    print("[+] Found: {} ipAddress: {}".format(host,"Not Found"))

def loadKeys():
  print("[!] Loading keys")
  apiFile = open("keys/api_creds","r")
  for line in apiFile:
    apiName,value = line.split(':')
    if apiName == 'shodan_key':
      global shodan_key
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

def hostScanControl(target):
  global scanned
  if target not in scanned:
      scanned.append(target)
      return True 
  else:
      return False

def runMasscan(hostname,ipAddress):
  print("[!] Disparando Masscan")
  outputStandart='/tmp/masscan_output_'
  target=ipAddress
  fileName=outputStandart+ipAddress
  FNULL = open(os.devnull, 'w')
  processHandler = subprocess.run(['masscan', ipAddress, '-Pn','--ports' ,'1-65535', '-oJ', fileName, '--banners','--connection-timeout', '3','--wait', '3', '--http-user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36', '--source-port','61000' ], stdout=FNULL,stderr=subprocess.STDOUT)
  FNULL.close()
  if os.stat(fileName).st_size == 0:
    return False
  data = open(fileName,'r')
  payload=json.loads(data.read())
  data.close()
  for host in range(len(payload)):
    print("[+][MASSSCAN] Result for hostname: {} ipAddress: {}".format(hostname,payload[host]['ip']))
    for port in range(len(payload[host]['ports'])):
      host_port=payload[host]['ports'][port]['port']
      if 'service' in payload[host]['ports'][port]:
        service_name=payload[host]['ports'][port]['service']['name']
        service_banner=payload[host]['ports'][port]['service']['banner']
      else:
        service_name='Null'
        service_banner='Null'
      print('\t[+] Open Port: {} Service: {} Banner: \n\t\t{}'.format(host_port,service_name,service_banner))
      try:
        db_controler.portAdd(ipAddress,host_port,hostname,service_name,service_banner)
      except Exception as error:
        print("Error:"+str(error))
  print("[=] Cleaning temp dir")
  processHandler = subprocess.run(['rm', '-f', fileName])
  if [ processHandler.check_returncode() == 0  ]:
    print("[+] Arquivo {} foi removido".format(fileName))
  else:
    print("[*] Falha oa excluir arquivo {}, erro: {}".format(fileName,processHandler.check_returncode()))

def spyse_subdomains(domain):
  print("[+] Searching in Spyse")
  data = requests.get(URLSPYSE+'/subdomains-aggregate?domain={}'.format(domain))
  if data.status_code in http_status_codes.keys(): 
    print('[!!] Error - {}'.format(http_status_codes))
  for cidr in data.json()['cidr']:
    for host_iter in range(len(data.json()['cidr'][cidr]['results'])):
      for hostname in range(len(data.json()['cidr'][cidr]['results'][host_iter]['data']['domains'])):
        host_fqdn = data.json()['cidr'][cidr]['results'][host_iter]['data']['domains'][hostname]
        print("[+][SPYSE] HOSTNAME: %s" % host_fqdn)
        avoidDuplicata(host_fqdn)
   


def countThreads():
  numT = threading.active_count()
  last_numT=0
  # thrad count issue
  while numT > 2 :
    numT = threading.active_count()
    if last_numT != numT:
      print("[*] {} threads left, please wait...".format(numT-2))
    last_numT=numT
  #  time.sleep(3)
  done = True

### Profiles
def passive_recon():
   # Pastebin Search
  pasteFounded=pastebin(tgt)
  ### Recon Passivo Footprint
  spyse_subdomains(tgt)
  securitytrails(tgt)
  virustotal(tgt)
  crtsh(tgt)
  certspotter(tgt)
  ## dnsbuffer retorna com endereços IPv4, melhor ao inves de usar listas, consumir direto do banco
  dnsbuffer_hosts=dnsbuffer.getHosts(tgt)
  for dnsbuffer_host in dnsbuffer_hosts:
    ipAddress=dnsbuffer_hosts[dnsbuffer_host]
    avoidDuplicata(dnsbuffer_host)
    db_controler.hostAdd(ipAddress,tgt,dnsbuffer_host)

def active_recon():
  global AGRESSIVE
  AGRESSIVE = True

### MAIN #### 
banner()
healthCheck()
targets=[]
domain=sys.argv[1] 
if not db_controler.domainAdd(domain):
  print("[!] The domain %s is already done bro" %(domain))

print("[*] Starting Routine for target %s" %(domain))
targets.append(domain)

## Find Related Domains:
for relDomain in spyse.spyse_related_domain(domain):
#  targets.append(relDomain)
  try:
    db_controler.relatedDomainAdd(domain,relDomain)
  except Exception as error:
    print("Error: %s" % (error))

for tgt in targets:
  db_controler.domainAdd(tgt)
  # Aws Search
  buckets = awsSearch.awsSearchFor(tgt,greyHat) #remove
  for bucket in buckets: # remove
    try:   # remove
      db_controler.s3Add(tgt,bucket) # Remove comment 
    except Exception as error:     # Remove Comment 
      print("Error: %s" % (error)) # Remove comment 

   # Pastebin Search
  pasteFounded=pastebin(tgt) # Remove comment 

  ### Recon Passivo Footprint
  crtsh(tgt)
  virustotal(tgt)
  spyse_subdomains(tgt)
  securitytrails(tgt)
  certspotter(tgt)
  dnsbuffer_hosts=dnsbuffer.getHosts(tgt)
  for dnsbuffer_host in dnsbuffer_hosts:
    ipAddress=dnsbuffer_hosts[dnsbuffer_host]
    avoidDuplicata(dnsbuffer_host)
    db_controler.hostAdd(ipAddress,tgt,dnsbuffer_host)

  sorted(set(allTargets))
  print("[*] Found {} hosts for {}".format(str(len(allTargets)),tgt))
   ## Recon Passivo Fingerprint
  print("[+] Resolving hostnames")
  API_COUNT=False
  for host in allTargets:
    threading.Thread(target=process,args=[host]).start()
    time.sleep(0.6)

  for thread in threading.enumerate():
    if not thread.getName() == 'MainThread':
      thread.join()
  t_num=len(threading.enumerate())-2
  while t_num >= 1:
    t_num_old=t_num
    if t_num_old != t_num:
      print('[*] Number of threads: ', threading.active_count())
      print('WAY BACK MODAFOCAAAAAAAAAA')
    t_num=len(threading.enumerate())-2

  print("[!] Creating Report for domain: {}".format(tgt))
  report_maker.hostsFromDomain(tgt)
  # Cleaning
  scanned=[]
  allTargets=[]
