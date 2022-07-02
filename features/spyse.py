#!/usr/bin/python3
# https://account.spyse.com/apidocs
import requests
import json
class spyse:
  def __init__(self,target_domain, auth_token):
    self.url = 'https://api.spyse.com/v3/data'
    self.auth_token = auth_token 
    self.head = { 'Authorization': 'Bearer ' + self.auth_token,
                'accept': 'application/json'}
    self.http_status_codes = { 400:'Maximum value for parameter exceeded / invalid or missing required parameters.',
                             402:'Request limit exceeded',
                             403:'Missing or invalid required parameter api_token.',
                             500: 'Internal server error. We are aware of the error and are already working on fixing it. Sorry for inconvenience.'} 
    self.target_domain = target_domain 
    self.url_subdomain = self.url + '/domain/subdomain/count?domain=%s' %(self.target_domain)
    self.url_sub_limit = self.url + '/domain/subdomain?limit=%s&domain=%s' %('100',self.target_domain) 

  def health_check(self):
    check = requests.get("https://spyse.com/")
    if check.status_code == 200:
      print("SPYSE OK")
      return True
    else:
      print("SPYSE is dead")
      return False

  def discovery(self):
 #necessário fazer um count antes e iterar de 100 em 100 devido restrições da API. 
    num_data = requests.get(self.url_subdomain,headers=self.head)
    num_sub=int(num_data.json()['data']['total_count'])
    if num_sub <= 100:
      data = requests.get(self.url_sub_limit,headers=self.head)
      if data.status_code in self.http_status_codes.keys(): 
        print('[!!] Error - {}'.format(self.http_status_codes))
        exit()
      payload_data=data.json()['data']['items']
      for item in range(len(payload_data)):
        host_fqdn=payload_data[item]['name']
        print("[+][SPYSE] HOSTNAME: %s" % host_fqdn)
    else:
      for offset in (0,num_sub,100):
        data = requests.get(self.url_subdomain + '&offset=%s&limit=%s' %(offset,100),headers=self.head)
        if data.status_code in http_status_codes.keys(): 
          print('[!!] Error - {}'.format(http_status_codes))
          exit()
        payload_data=data.json()['data']['items']
        for item in range(len(payload_data)):
          host_fqdn=payload_data[item]['name']
          print("[+][SPYSE] HOSTNAME: %s" % host_fqdn)
   
## Spyse IP 
#  def enum(self,ip,hostName):
#
#def spyse_ip(ip,hostName):
#  spyse.spyse_ip(ip,hostName) 
#  db_controler.portAdd(ipAddress,port,hostName,protocol,banner)
#  check_banner(hostName,banner,port,ipAddress)
#  print("Error in Spyse_IP: %s" % (Error))
    #Tb trabalha com offset
    data = requests.get(self.url+'/ip/port?limit=100&&ip={}'.format(ip),headers=self.head)
    if data.status_code in http_status_codes.keys():
      print('[!!] Error - {}'.format(http_status_codes))
    elif len(data.json()) == 0:
      print("[!] Nothing found for target: {}".format(ip))
    payload_data=data.json()['data']['items']
    ipAddress=ip
    total_count=data.json()['data']['total_count'] 
    print("[-][SPYSE] Hostname: {} ipAddress: {} Total Ports: {}".format(hostName,ipAddress,total_count))
    for portc in range(len(payload_data)):
      pdata=payload_data[portc]
      port=pdata['port'] if 'port' in pdata else 'Null'
      banner=pdata['banner'] if 'banner' in pdata else 'Null'
      service=pdata['service'] if 'service' in pdata else 'Null'
      os=pdata['operation_system']  if 'operation_system' in payload_data else 'Null'
      product=pdata['product']  if 'product' in pdata else 'Null'
      version=pdata['version']  if 'version' in pdata else 'Null'  
      if len(pdata['banner_ssl']) > 0:
        banner=pdata['banner_ssl'] if 'banner_ssl' in pdata else 'Null'

      print("\t[+] Port: {} Protocol: {} Banner: {} \n\n\t OS: {} Product: {} {}".format(port,service,banner.replace('\n','\n\t'),os,product,version))

    #extract=payload_data[port]['extract'] 
    #http_headers==extract['http_headers'] 

#              print("\t[-][SPYSE] Protocol: {} Description: {} ".format(protocol,protocol_description))
#          if 'service' in data_json_ports:
#            if len(data_json_ports['service']) > 0:
#              data_service=data_json_ports['service']
#              service=data_service['name'] if 'name' in data_service else 'Null'
#              service_description=data_service['description'] if 'description' in data_service else 'Null'
#              print("\t[-][SPYSE] Service: {} Description: {} ".format( service,service_description))

          #db_controler.portAdd(ipAddress,port,hostName,protocol,banner)
          #check_banner(hostName,banner,port,ipAddress)
#        except Exception as Error:
#          print("Error in Spyse_IP: %s" % (Error))


  def related_domain(self):
    domain_results=[]
    data = requests.get(URL+'/domain/on_same_ip?limit={}&domain={}'.format('30',self.target_domain),headers=self.head)
    if data.status_code in http_status_codes.keys():
      print('[!!] Error -{}  {}'.format(data.status_code,http_status_codes[data.status_code]))
    else:
      payload_data=data.json()['data']['items']
      for item in range(len(payload_data)):
        related_domain= payload_data[item]['name']
        print("[!] Target domain has relation with {}".format(related_domain))
        domain_results.append(related_domain)
#      return domain_results

if __name__ == "__main__":
  import sys
  target=sys.argv[1]
  auth_token = sys.argv[2] 
  spy = spyse(target,auth_token) 
  spy.discovery()
#  hostName=sys.argv[2]
 # spyse_subdomains(target)     
  #spyse_related_domain(target) 
 # spyse_ip(target,hostName)
