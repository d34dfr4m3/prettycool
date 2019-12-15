#!/usr/bin/python3
# https://account.spyse.com/apidocs
import requests
import json
URL='https://api.spyse.com/v1'
http_status_codes = {'400':'Maximum value for parameter exceeded / invalid or missing required parameters.',
                    '402':'Request limit exceeded',
                    '403':'Missing or invalid required parameter api_token.',
                    '500': 'Internal server error. We are aware of the error and are already working on fixing it. Sorry for inconvenience.'} 

def spyse_subdomains(domain):
  data = requests.get(URL+'/subdomains-aggregate?domain={}'.format(domain))
  if data.status_code in http_status_codes.keys(): 
    print('[!!] Error - {}'.format(http_status_codes))
  for cidr in data.json()['cidr']:
    for host_iter in range(len(data.json()['cidr'][cidr]['results'])):
      for hostname in range(len(data.json()['cidr'][cidr]['results'][host_iter]['data']['domains'])):
        print(data.json()['cidr'][cidr]['results'][host_iter]['data']['domains'][hostname])
   

def spyse_ip(ip):
  data = requests.get(URL+'/ip-port-lookup?q={}&page={}'.format(ip,'1'))
  if data.status_code in http_status_codes.keys():
    print('[!!] Error - {}'.format(http_status_codes))
  elif len(data.json()) == 0:
    print("[!] Nothing found for target: {}".format(ip))
  for ips in range(len(data.json())):
    ipAddress=data.json()[ips]['ip']['ip']
    print("[+] IP: {}".format(ipAddress))
    for ports in range(len(data.json()[ips]['iplList'])):
      port=data.json()[ips]['iplList'][ports]['port']
      banner=data.json()[ips]['iplList'][ports]['banner']
      protocol=data.json()[ips]['iplList'][ports]['protocol']['name']
      print("\t[-] Port: {} Protocol: {} Banner: {}".format(port,protocol,banner.replace('\n','\n\t')))

def spyse_related_domain(domain):
  domain_results=[]
  data = requests.get(URL+'/domains-on-ip?domain={}&page={}'.format(domain,'1'))
  if data.status_code in http_status_codes.keys():
    print('[!!] Error - {}'.format(http_status_codes))
  for domains in range(len(data.json()['records'][0])):
    related_domain = data.json()['records'][domains]['domain']
    print("[!] Target domain has relation with {}".format(related_domain))
    domain_results.append(related_domain)
  return domain_results

#import sys
#target=sys.argv[1]
#spyse_subdomains(target)     
#spyse_related_domain(target) 
#spyse_ip(target)
