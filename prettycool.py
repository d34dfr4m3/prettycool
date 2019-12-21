#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
import getopt
import socket
import shodan
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
#from tools import wayback

global censys
global shodan
global sectrial
global scanned
global domain
global CENSYS_DEAD
CENSYS_DEAD = False
scanned = []
allTargets = []
URLSPYSE = 'https://api.spyse.com/v1'
http_status_codes = {'400': 'Maximum value for parameter exceeded / invalid or missing required parameters.',
                     '402': 'Request limit exceeded',
                     '403': 'Missing or invalid required parameter api_token.',
                     '500': 'Internal server error. We are aware of the error and are already working on fixing it. Sorry for inconvenience.'}


def checkDB():
    pid = os.system('ps -C mysqld &>/dev/null')
    if pid == 256:
        print("[!!] Database is not running")
        return False
    elif pid == 0:
        print("[!!] Database is running, ready to kill some bytes!")
        return True


def healthCheck():
    # Notes from fucked dev: Tenho vergonha dessa merda q eu escrevi
    # Censys api info
    # Todo: Check if api are reacheable trying to connect.
    # And fuc, this code sucks bro, clean this shit
    # Add database checker
    if os.geteuid() != 0:
        print("[-] Error: You need to run this program with root, morty")
        exit(1)
    # if not checkDB():
    #  exit()
    loadKeys()
    global censys_UID
    global censys_SECRET
#  URLS={'censys':
#          {'url_to_do_y':'url',
#            'url_to_do_x':'url'},
#          'shodan':{}
#          }
    API_URL = "https://censys.io/api/v1"
    page = requests.get(API_URL+"/account", auth=(censys_UID, censys_SECRET))
    left = int(page.json()['quota']['allowance']) - \
        int(page.json()['quota']['used'])
    if left > 50:
        print("[!!] Censys API has only {} requests left".format(str(left)))
    elif left > 20:
        print("[!!] Censys API has only {} requests left".format(str(left)))
    elif left > 10:
        print("[!!] Censys API has only {} requests left".format(str(left)))
    elif left == 0:
        global CENSYS_DEAD
        CENSYS_DEAD = True
        # Pick up another key right guys!
        print("[!!] Censys API has no credits to use")
    else:
        print("[!!] Censys API is ready to rock with {} requests left".format(left))

    # Shodan api info
    global shodan_key
    page = requests.get('https://api.shodan.io/api-info?key='+shodan_key)
    left = int(page.json()['unlocked_left'])
    if left < 50:
        print("[!!] Shodan API has only {} requests left".format(str(left)))
    elif left < 20:
        print("[!!] Shodan API has only {} requests left".format(str(left)))
    elif left < 10:
        print("[!!] Shodan API has only {} requests left".format(str(left)))
    else:
        print("[!!] Shodan API is ready to rock with {} requests left".format(left))
     # Security Trails
    global securitytrails_KEY
    headers = {'apikey': securitytrails_KEY}
    page = requests.get(
        'https://api.securitytrails.com/v1/account/usage', headers=headers)
    left = page.json()['allowed_monthly_usage'] - \
        page.json()['current_monthly_usage']
    if 'message' in page.json().keys():
        error = page.json()['message']
        print("[!!] SecurityTrails API issue: {}".format(error))
        exit(1)
    else:
        print(
            "[!!] SecurityTrails API is ready to rock with {} requests left".format(left))


def shodan(target, hostname):
    global shodan_key
    data = requests.get(
        'https://api.shodan.io/shodan/host/'+target+'?key='+shodan_key)
    payload = data.json()
    try:
        for i in range(len(payload['data'])):
            try:
                port = payload['data'][i]['port']
            except Exception as errPort:
                port = 'Not Found'
            try:
                product = payload['data'][i]['product']
            except Exception as errProduct:
                product = 'Not Found'
            try:
                banner = payload['data'][i]['banner']
            except Exception as error:
                banner = 'Not Found'

            try:
                ops = payload['data'][i]['os']
            except Exception as error:
                ops = 'Not Found'
        print(
            '\t[+] Open Port: {} Product: {} Banner: {} OS: {}'.format(port, product, banner, ops))
        db_controler.portAdd(target, port, hostname)

    except Exception as err:
        print("\t[+] Miss or error: {}".format(err))


def resolve(target):
    try:
        return socket.gethostbyname(target)
    except Exception as error:
        return False


def certspotter(target):
    print("[+] Searching in Certspotter")
    data = requests.get("https://certspotter.com/api/v0/certs?domain="+target)
    payload = data.json()
    for domains in range(len(payload)):
        dnsNamesList = payload[domains]['dns_names']
        for i in range(len(dnsNamesList)):
            if not '*' in dnsNamesList[i]:
                avoidDuplicata(dnsNamesList[i])


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


def censys_api(ipAddress, hostName):
    global censys_UID
    global censys_SECRET
    API_URL = "https://censys.io/api/v1"
    web_protocols = ['http', 'https']
    auth = requests.get(API_URL + "/data", auth=(censys_UID, censys_SECRET))
    if auth.status_code != 200:
        print("[+] Auth Error: ", auth.json()['error'])
        CENSYS_DEAD = True
    else:
        params = {'query': ipAddress, 'page': 10}
        try:
            page = requests.post(API_URL+"/search/ipv4",
                                 json=params, auth=(censys_UID, censys_SECRET))
            num_results = page.json()['metadata']['count']
            if num_results > 0:
                page = requests.get(API_URL+"/view/ipv4/" +
                                    ipAddress, auth=(censys_UID, censys_SECRET))
                for protocol in range(len(page.json()['protocols'])):
                    port = page.json()['protocols'][protocol].split('/')[0]
                    proto = page.json()['protocols'][protocol].split('/')[1]
                    if proto in web_protocols:
                        if 'title' in page.json()[port][proto]['get'].keys():
                            title = page.json()[port][proto]['get']['title']
                            protocol = page.json()['protocols'][protocol]
                            print(
                                "\t[+] Protocol: {}  Title: {} ".format(page.json()['protocols'][proto], title))
                        else:
                            print(
                                "\t[+] Protocol: {}".format(page.json()['protocols'][protocol]))
            db_controler.portAdd(ipAddress, port, hostName, protocol)
        except Exception as error:
            print("[!} Error Censys:", str(error))


def crtsh(target):
    print("[+] Searching in crtsh")
    data = requests.get('https://crt.sh/?q=%.'+target)
    page = BeautifulSoup(data.text, 'html.parser')
    for domain in page.find_all('td'):
        domaintxt = domain.get_text()
        if target in domaintxt and '*' not in domaintxt and '%' not in domaintxt:
            avoidDuplicata(domaintxt.split('>')[0])


def spyse_ip(ip, hostname):
    data = requests.get(
        URLSPYSE+'/ip-port-lookup?q={}&page={}'.format(ip, '1'))
    if data.status_code in http_status_codes.keys():
        print('[!!] Error - {}'.format(http_status_codes))
    elif len(data.json()) == 0:
        return False
    for ips in range(len(data.json())):
        ipAddress = data.json()[ips]['ip']['ip']
        for ports in range(len(data.json()[ips]['iplList'])):
            try:
                port = data.json()[ips]['iplList'][ports]['port']
                banner = data.json()[ips]['iplList'][ports]['banner']
                protocol = data.json()[
                    ips]['iplList'][ports]['protocol']['name']
                print(
                    "\t[-] Port {}  Proto: {} Banner: {} ".format(port, protocol, banner))
                db_controler.portAdd(
                    ipAddress, port, hostname, protocol, banner)
            except Exception as Error:
                print("Error in Spyse_IP: %s" % (Error))


def pastebin(target):
    pasteList = {}
    print("[!] Starting Pastebin Routine: Target {}".format(target))
    data = requests.get("https://psbdmp.ws/api/search/"+target)
    payload = data.json()
    for ids in range(len(payload['data'])):
        check = requests.get('https://pastebin.com/' +
                             payload['data'][ids]['id'])
        if check.status_code == 200:
            page = BeautifulSoup(check.text, 'html.parser')
            url = 'https://pastebin.com/'+str(payload['data'][ids]['id'])
            title = page.title.get_text()
            date = page.findAll('span', limit=11)[10].contents[0]
            print('[!] Found: {} Date: {} Title: {}'.format(url, date, title))
            try:
                db_controler.pasteAdd(target, url, title, date)
            except Exception as error:
                print("Pastebin error: {}".format(error))
            pasteList[url] = {date: title}
    return pasteList


def virustotal(target):
    print("[+] Searching in VirulTotal")
    data = requests.get('https://www.virustotal.com/ui/domains/' +
                        target+'/subdomains?relationships=resolutions')
    payload = data.json()
    for ids in range(len(payload['data'])):
        avoidDuplicata(payload['data'][ids]['id'])


def securitytrails(target):
    print("[+] Searching in SecurityTrails")
    global securitytrails_KEY
    headers = {'apikey': securitytrails_KEY}
    data = requests.get("https://api.securitytrails.com/v1/domain/" +
                        target+'/subdomains', headers=headers)
    if data.status_code == 429:
        print(
            "[!!] SecurityTrails API is out of credits or some stuff related with capitalism")
        exit()
    payload = data.json()
    for hosts in range(len(payload['subdomains'])):
        avoidDuplicata(payload['subdomains'][hosts]+'.'+target)


def process(host):
    global domain
    ipAddress = resolve(host)
    db_controler.hostAdd(ipAddress, domain, host)
    if ipAddress:
        print("[+] Found: {} ipAddress: {}".format(host, ipAddress))
        if hostScanControl(ipAddress):
            shodan(ipAddress, host)
            spyse_ip(ipAddress, host)
            if not CENSYS_DEAD:
                censys_api(ipAddress, host)

            runMasscan(host, ipAddress)

    else:
        print("[+] Found: {} ipAddress: {}".format(host, "Not Found"))


def loadKeys():
    print("[!] Loading keys")
    apiFile = open("keys/api_creds", "r")
    for line in apiFile:
        apiName, value = line.split(':')
        if apiName == 'shodan_key':
            global shodan_key
            shodan_key = value.replace('\n', '').strip("'")
            print("[-] Shodan key loaded: %s" % (shodan_key))
        elif apiName == 'censys_UID':
            global censys_UID
            censys_UID = value.replace('\n', '').strip("'")
            print("[-] Censys UID loaded: %s " % (censys_UID))
        elif apiName == 'censys_SECRET':
            global censys_SECRET
            censys_SECRET = value.replace('\n', '').strip("'")
            print("[-] Censys Secreted loaded: %s" % (censys_SECRET))
        elif apiName == 'securitytrails':
            global securitytrails_KEY
            securitytrails_KEY = value.replace('\n', '').strip("'")
            print("[-] SecurityTrails key loaded %s" % (securitytrails_KEY))
        elif apiName == 'greyHat':
            global greyHat
            greyHat = value.replace('\n', '').strip("'")
            print("[-] greyHat key loaded: %s " % (greyHat))


def hostScanControl(target):
    global scanned
    if target not in scanned:
        scanned.append(target)
        return True
    else:
        return False


def runMasscan(hostname, ipAddress):
    print("[!] Disparando Masscan")
    outputStandart = '/tmp/masscan_output_'
    target = ipAddress
    fileName = outputStandart+ipAddress
    FNULL = open(os.devnull, 'w')
    processHandler = subprocess.run(['masscan', ipAddress, '-Pn', '--ports',
                                     '1-65535', '-oJ', fileName], stdout=FNULL, stderr=subprocess.STDOUT)
    FNULL.close()
    if os.stat(fileName).st_size == 0:
        return False
    data = open(fileName, 'r')
    payload = json.loads(data.read())
    data.close()
    for host in range(len(payload)):
        print("[+] [MASSSCAN] Result for : {} ipAddress: {}".format(hostname,
                                                                    payload[host]['ip']))
        for port in range(len(payload[host]['ports'])):
            port = payload[host]['ports'][port]['port']
            print('\t[+] Open Port: {}'.format(port))
            try:
                db_controler.portAdd(ipAddress, port, hostname)
            except Exception as error:
                print("Error:"+str(error))

    print("[=] Cleaning temp dir")
    processHandler = subprocess.run(['rm', '-f', fileName])
    if [processHandler.check_returncode() == 0]:
        print("[+] Arquivo {} foi removido".format(fileName))
    else:
        print("[*] Falha oa excluir arquivo {}, erro: {}".format(fileName,
                                                                 processHandler.check_returncode()))


def spyse_subdomains(domain):
    print("[+] Searching in Spyse")
    data = requests.get(
        URLSPYSE+'/subdomains-aggregate?domain={}'.format(domain))
    if data.status_code in http_status_codes.keys():
        print('[!!] Error - {}'.format(http_status_codes))
    for cidr in data.json()['cidr']:
        for host_iter in range(len(data.json()['cidr'][cidr]['results'])):
            for hostname in range(len(data.json()['cidr'][cidr]['results'][host_iter]['data']['domains'])):
                host_fqdn = data.json()[
                    'cidr'][cidr]['results'][host_iter]['data']['domains'][hostname]
                avoidDuplicata(host_fqdn)


def countThreads():
    numT = threading.active_count()
    last_numT = 0
    # thrad count issue
    while numT > 2:
        numT = threading.active_count()
        if last_numT != numT:
            print("[*] {} threads left, please wait...".format(numT-2))
        last_numT = numT
        time.sleep(3)

# Profiles


def passive_recon():
   # Pastebin Search
    pasteFounded = pastebin(tgt)
    # Recon Passivo Footprint
    spyse_subdomains(tgt)
    securitytrails(tgt)
    virustotal(tgt)
    crtsh(tgt)
    certspotter(tgt)
    # dnsbuffer retorna com endereços IPv4, melhor ao inves de usar listas, consumir direto do banco
    dnsbuffer_hosts = dnsbuffer.getHosts(tgt)
    for dnsbuffer_host in dnsbuffer_hosts:
        ipAddress = dnsbuffer_hosts[dnsbuffer_host]
        avoidDuplicata(dnsbuffer_host)
        db_controler.hostAdd(ipAddress, tgt, dnsbuffer_host)


def active_recon():
    global AGRESSIVE
    AGRESSIVE = True


### MAIN ####
banner()
healthCheck()
targets = []
domain = sys.argv[1]
if not db_controler.domainAdd(domain):
    print("[!] The domain is already done bro")
targets.append(domain)

# Find Related Domains:
for relDomain in spyse.spyse_related_domain(domain):
    targets.append(relDomain)
    try:
        db_controler.relatedDomainAdd(domain, relDomain)
    except Exception as error:
        print("Error: %s" % (error))

for tgt in targets:
    db_controler.domainAdd(tgt)
    # Aws Search
    buckets = awsSearch.awsSearchFor(tgt, greyHat)
    for bucket in buckets:
        try:
            db_controler.s3Add(tgt, bucket)
        except Exception as error:
            print("Error: %s" % (error))
   # Pastebin Search
    pasteFounded = pastebin(tgt)
    # Recon Passivo Footprint
    spyse_subdomains(tgt)
    securitytrails(tgt)
    virustotal(tgt)
    crtsh(tgt)
    certspotter(tgt)
    # dnsbuffer retorna com endereços IPv4, melhor ao inves de usar listas, consumir direto do banco
    dnsbuffer_hosts = dnsbuffer.getHosts(tgt)
    for dnsbuffer_host in dnsbuffer_hosts:
        ipAddress = dnsbuffer_hosts[dnsbuffer_host]
        avoidDuplicata(dnsbuffer_host)
        db_controler.hostAdd(ipAddress, tgt, dnsbuffer_host)

    sorted(set(allTargets))
    print("[*] Found {} hosts for {}".format(str(len(allTargets)), tgt))
   # Recon Passivo Fingerprint
    print("[+] Resolving hostnames")
    API_COUNT = False
    for host in allTargets:
        # Possível controle por num máximo de threads aqui.
        #print('[*] Number of threads: ', threading.active_count())
        threading.Thread(target=process, args=[host]).start()
        time.sleep(0.7)
        if not API_COUNT:
            threading.Thread(target=countThreads).start()
            API_COUNT = True
    for host in allTargets:
        string = "HOST: {} IP: {}\n".format(host, resolve(host))

    print("[!] Creating Report for domain: {}".format(tgt))
    report_maker.hostsFromDomain(tgt)
    # Cleaning
    scanned = []
    allTargets = []
