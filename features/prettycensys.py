#!/usr/bin/python3
import requests
import json
class mycensys:
  def __init__(self,uid,secret,target):
    self.uid  = uid
    self.target = "" 
    self.secret = secret
    self.api_url_v1 = "https://search.censys.io/api/v1" 
    self.api_url_v2 = "https://search.censys.io/api/v2"
    self.api_host_search = self.api_url_v2 + "/hosts/search?q={}&per_page=50&virtual_hosts=EXCLUDE".format(target)
    self.api_url_health = self.api_url_v1 + "/account" 
    self.api_get_hostname = self.api_url_v2 + "/hosts/{}/names"
    self.host_info = self.api_url_v2 + "/hosts/{}"
    self.web_protocols=['http','https']
  
  def health_check(self):
    page=requests.get(self.api_url_health, auth=(self.uid,self.secret))
    left=int(page.json()['quota']['allowance'])-int(page.json()['quota']['used'])
    if left > 50:
      print("[!!] Censys API has only {} requests left".format(str(left)))
      return True
    elif left > 20:
      print("[!!] Censys API has only {} requests left".format(str(left)))
      return True
    elif left > 10:
      print("[!!] Censys API has only {} requests left".format(str(left)))
      return True
    elif left <= 0:
      # Pick up another key right guys! 
      print("[!!] Censys API has no credits to use")
      return False
    else:
      print("[!!] Censys API is ready to rock with {} requests left".format(left))
      return True

  def discovery(self): 
    data=requests.get(self.api_host_search, auth=(self.uid,self.secret))
#    print(data.json())
    results=data.json()["result"]["hits"]
    for result in results:
      ip=result['ip'] if 'ip' in result else False
      print("Searching hostname for {}".format(ip))
      get_hostname = requests.get(self.api_get_hostname.format(ip),auth=(self.uid,self.secret)) 
      hostnames=get_hostname.json()['result']['names']
      last_updated_at=result['last_updated_at'] if 'last_updated_at' in result else False
      location_country=result["location"]["country"] if "country" in result["location"] else False
      location_city=result["location"]["city"] if "city" in result["location"] else False
      location_coordinates=result["location"]["coordinates"] if "coordinates" in result["location"] else False
      asn=result["autonomous_system"]["asn"] if "asn" in result["autonomous_system"] else False
      asn_description=result["autonomous_system"]["description"] if "description" in result["autonomous_system"] else False
      asn_prefix=result["autonomous_system"]["bgp_prefix"] if "bgp_prefix" in result["autonomous_system"] else False
      asn_name=result["autonomous_system"]["name"] if "name" in result["autonomous_system"] else False
      print("[+][CENSYS] hostName: {} Target Address: {} Location: {}/{}/{} - ASN {} Name: {} ASN Description: {} ASN Prefix: {} Last Update: {}".format(hostnames,ip,location_city,location_country,location_coordinates,asn,asn_name,asn_description,asn_prefix,last_updated_at))
      ## Host Enum 
      self.enum(ip)
      #db_controler.portAdd(ipAddress,port,hostName,protocol)

  def enum(self,ip=None): 
    if ip == None:
      print("[*] - Censys Enum missing IP, exiting")
      return False
    hostinfo = requests.get(self.host_info.format(ip),auth=(self.uid,self.secret))
    if hostinfo.json()['status'] != "OK":
      print("[*] CENSUS ENUM STATUS NOT OK, ABORTING")
      exit(1)
    results=hostinfo.json()['result']
    for service in results["services"]:
      service_port=service['port'] if 'port' in service else False
      service_name=service['service_name'] if 'service_name' in service else False
      service_transport_protocol=service['transport_protocol'] if 'transport_protocol' in service else False
      service_certificate=service['certificate'] if 'certificate' in service else False
      print("\t[+][CENSYS] Port: {} Service Name: {} Protocol: {} Certificate: {}".format(service_port,service_name,service_transport_protocol,service_certificate))
      ### OS 
      if 'operating_system' in service:
        operating_system=service['operating_system']  
        os_product = operating_system['product'] if 'product' in operating_system else False
        os_vendor = operating_system['vendor'] if 'vendor' in operating_system else False
        os_version = operating_system['version'] if 'version' in operating_system else False
        os_edition = operating_system['edition'] if 'edition' in operating_system else False 
        print("\t[+][CENSYS] Product: {} Vendor: {} Version: {} Edition: {}".format(os_product,os_vendor,os_version,os_edition))
      # DNS 
      # WebApps (HTTP/HTTPS)
      if 'http' in service:
        print("HTTP HIT")
        ## Response
        http_response = service['http']['response'] if 'response' in service['http'] else False
        body = http_response['body'] if 'body' in http_response else False 
        protocol = http_response['protocol'] if 'protocol' in http_response else False
        body_size = http_response['body_size'] if 'body_size' in http_response else False
        status_code = http_response['status_code'] if 'status_code' in http_response else False
        status_reason = http_response['status_reason'] if 'status_reason' in http_response else False
        html_tags = http_response['html_tags']  if 'html_tags' in http_response else False
        ### Headers
        headers = http_response['headers'] if 'headers' in http_response else False
        header_content_length = headers['Content_Length'] if 'Content_Length' in headers else False
        header_content_type = headers['Content_Type'] if 'Content_Type' in headers else False
        header_server = headers['Server'] if 'Server' in headers else False
        header_date = headers['Date'] if 'Date' in headers else False
        print("\t[+][CENSYS] Protocol:{} Status Code: {} Content Length {}: Content Type: {} Server: {} Date: {}".format(protocol,status_code,header_content_length,header_content_type,header_server,header_date))
        print("\t\t[+][CENSYS] Html Tags:{} Body Size: {}".format(html_tags,body_size))
        print("\t\t\t{}".format(body))
        #db_controler.portAdd(ipAddress,port,hostName,protocol)

    
if __name__ == "__main__":
  import sys
  api_id=sys.argv[1]
  api_secret=sys.argv[2]
  target=sys.argv[3]
  cnsy=mycensys(api_id,api_secret,target)
  cnsy.health_check()
  cnsy.discovery()
  #cnsy.enum()
