#!/usr/bin/python3
import pymysql.cursors
def createCon():
  connection = pymysql.connect(host='localhost',
                             user='prettycool',
                             password='',
                             db='db_data',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
  return connection


def execQuery(query):
  connection = createCon()
  with connection.cursor() as cursor:
    cursor.execute(query)
    result=cursor.fetchall()
    connection.close()
    if len(result) > 0:
      return result

def listDomains():
  # Query all domains in the database; 
  query = "select domainName,createdAt from tb_domain;" 
  result = execQuery(query)
  if result:
    for domain in range(len(result)):
      print(result[domain]['domainName'])
  
def hostOnly(hostname):
  # Query all domains in the database; 
  query = "select hostname,port from tb_port where hostname = '{}'; ".format(hostname)
  result = execQuery(query)
  if result:
    for domain in range(len(result)):
      print(result[domain]['domainName'])

def hostsFromDomain(domain):
  count=0
  print("[+] Hosts from Domain {}:".format(domain))
  query ="select tb_host.hostName,tb_host.ipAddress,tb_port.port, tb_port.protocol,tb_port.banner from tb_host inner join tb_port where tb_host.domainName='{}' and tb_port.ipAddress = tb_host.ipAddress order by 1;".format(domain)
  result = execQuery(query)
  if result:
    for host in range(len(result)):
      ipAddress=result[host]['ipAddress']
      hostName=result[host]['hostName']
      port=result[host]['port']
      banner=result[host]['banner']
      protocol=result[host]['protocol']
      print("\n\tHostname: {} ipAddress: {} Port: {} Protocol: {} Banner: {}".format(hostName,ipAddress,port,protocol,str(banner)))
      count+=1
  else:
    print("[+] {} Not found in database".format(domain))
  print("[!] Found {} records in database".format(count))

def relatedDomains(domain):
  count=0
  print("[+] Related domains from from Domain {}:".format(domain))
  query ="select domainName from tb_relatedDomains where mainDomain ='{}';".format(domain)
  result = execQuery(query)
  if result:
    for domain in range(len(result)):
      rdomain=result[domain]['domainName']
      print("\t[-] Related Domain: {}".format(rdomain))
      count+=1
  else:
    print("[+] {} Not found in database".format(domain))
  print("[!] Found {} related Domains in database".format(count))

def pastebin(domain):
  count=0
  print("[+] Pastebin related with domain {}:".format(domain))
  query ="select url,title,dumpDate from tb_pastebin where domainName='{}';".format(domain)
  result = execQuery(query)
  if result:
    for paste in range(len(result)):
      url=result[paste]['url']
      title=result[paste]['title']
      dumpDate=result[paste]['dumpDate']
      print("\t[-] URL: {} DumpDate: {} Title: {} ".format(url,dumpDate,title))
      count+=1
  else:
    print("[+] {} Not found in database".format(domain))
  print("[!] Found {} links in database".format(count))

def buckets(domain):
  count=0
  print("[+] Buckets from Domain {}:".format(domain))
  query ="select url from tb_aws where domainName='{}';".format(domain)
  result = execQuery(query)
  if result:
    for url in range(len(result)):
      print("\t[-] Bucket: {}".format(result[url]['url']))
      count+=1
  else:
    print("[+] {} Not found in database".format(domain))
  print("[!] Found {} Buckets in database".format(count))

def makeReport(domain):
  pastebin(domain)
  buckets(domain)
  hostsFromDomain(domain)
  relatedDomains(domain)

#import sys
#domain_name = sys.argv[1]
#hostsFromDomain(domain_name)
#buckets(domain_name)
#makeReport(domain_name)
#relatedDomains(domain_name)
#listDomains()
#hostOnly(domain_name)

