#!/usr/bin/python3
import requests
import json

class my_whoisfreaks:
  def __init__(self,key,target_domain):
    self.target_domain = target_domain
    self.key = key
    self.url = "https://api.whoisfreaks.com/v1.0/whois?apiKey={}&whois=historical&domainName={}".format(self.key,self.target_domain)

  def health_check(self):
    print("[-] HEALTH CHECK - WHOIS FREAKS NOT IMPLEMENTED")
#    check_reachable = requests.get(self.url)
#    if check_reachable.status_code == 200:
#      print("[!] WHOISFREAKS IS REACHABLE - Status code: %s" %(check_reachable.status_code))
#    else: 
#      print("[!] WHOISFREAKS IS NOT REACHABLE - Status code: %s" %(check_reachable.status_code))

  def get_whois(self):
    print("[+][STARTING WHOISFREAKS] Target: %s" %(self.target_domain))
    data=requests.get(self.url)
    if data.status_code == 200:
      print("[!] WHOISFREAKS IS REACHABLE - Status code: %s" %(data.status_code))
    else:
      print("[!] WHOISFREAKS IS NOT REACHABLE - Status code: %s" %(data.status_code))
      return False
    whoisdata=data.json()['whois_domains_historical'][0]
#    print(whoisdata)
    domain_name = whoisdata['domain_name'] if 'domain_name' in whoisdata else False
    create_time = whoisdata['create_date'] if 'create_date' in whoisdata else False
    expiry_time = whoisdata['expiry_date'] if 'expiry_date' in whoisdata else False
    print("[+] WhoisFreaks - Domain Name: {} Create Time: {} Expiricy Time: {}".format(domain_name,create_time,expiry_time))
    if 'registrant_contact' in whoisdata:
      registrant_contact = whoisdata['registrant_contact'] 
      registrant_name = registrant_contact['name'] if 'name' in registrant_contact else False
      registrant_country = registrant_contact['country_name'] if 'country_name' in registrant_contact else False
      registrant_email = registrant_contact['email_address'] if 'email_address' in registrant_contact else False
      print("[+] WhoisFreaks - Registrant Contact -> Name: {} Country: {} Email: {}".format(registrant_name,registrant_country,registrant_email))
    else:
      print("WHOISFREAKS - No registrant_contact Available")
    if 'administrative_contact' in whoisdata:
      administrative_contact = whoisdata['administrative_contact'] 
      administrative_name = administrative_contact['name'] if 'name' in administrative_contact else False
      administrative_country = administrative_contact['country_name'] if 'country_name' in administrative_contact else False
      administrative_email = administrative_contact['email_address'] if 'email_address' in administrative_contact else False
      print("[+] WhoisFreaks - Administrative Contact -> Name: {} Country: {} Email: {}".format(administrative_name,administrative_country,administrative_email))
    else:
      print("WHOISFREAKS - No administrative_contact Available") 
    if 'technical_contact' in whoisdata:
      technical_contact = whoisdata['technical_contact'] 
      technical_name = technical_contact['name'] if 'name' in technical_contact else False
      technical_country = technical_contact['country_name'] if 'country_name' in technical_contact else False
      technical_email = technical_contact['email_address'] if 'email_address' in technical_contact else False
      print("[+] WhoisFreaks - Technical Contact -> Name: {} Country: {} Email: {}".format(technical_name,technical_country,technical_email))
    else:
      print("WHOISFREAKS - No technical_contact Available") 
    if 'billing_contact' in whoisdata:
      billing_contact = whoisdata['billing_contact'] 
      billing_name = billing_contact['name'] if 'name' in billing_contact else False
      billing_country = billing_contact['country_name'] if 'country_name' in billing_contact else False
      billing_email = billing_contact['email_address'] if 'email_address' in billing_contact else False
      print("[+] WhoisFreaks - Billing Contact -> Name: {} Country: {} Email: {}".format(billing_name,billing_country,billing_email))
    else:
      print("WHOISFREAKS - No billing_contact Available") 
    for name_server in whoisdata['name_servers']:
      print("[+] Name Server:{}".format(name_server))


if __name__ == "__main__":
  import sys
  key = sys.argv[1]
  target_domain = sys.argv[2]
  wfks = whoisfreaks(key,target_domain)
  wfks.health_check()
  wfks.get_whois() 
