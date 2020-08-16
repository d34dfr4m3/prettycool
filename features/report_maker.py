#!/usr/bin/python3
import pymysql.cursors
#from features import db_controler
class report:
  def __init__(self,db):
    self.db = db
#    self.db.load_cred()

  def listDomains(self):
    # Query all domains in the database; 
    query = "select domainName,createdAt from tb_domain where cd_status = 1;" 
    result = self.db.execQuery(query)
    db_domains=[]
    if result:
      for domain in range(len(result)):
        domainName=result[domain]['domainName']
        db_domains.append(domainName)
        print("[!] Domain: %s " %(domainName))
      print("[!] Number of domains in database: %s" %(len(result)))  
      return db_domains
#        query="select count(hostName) as total from tb_host where domainName='{}';".format(domainName)
#        getNum = self.db.execQuery(query)
#        if getNum:
#          totalHosts=getNum[0]['total']
  
  def hostOnly(self,hostname):
    # Query a unique hostname in the database; 
    #query ="select tb_host.hostName,tb_host.ipAddress,tb_port.port, tb_port.protocol,tb_port.banner from tb_host inner join tb_port where tb_host.domainName='{}' and tb_port.ipAddress = tb_host.ipAddress order by 1;".format(domain)
    query ="select hostName,ipAddress,isp,link,org,latitude,longitude,last_update,shodan_last_update from tb_host where domainName='{}' and ipAddress != 'False' order by 1;".format(domain)
    result = execQuery(query)
    if result:
      for host in range(len(result)):
        hostName=result[host]['hostName']
        ipAddress=result[host]['ipAddress']
        isp=result[host]['isp']
        link=result[host]['link']
        org=result[host]['org']
        asn=result[host]['asn']
        latitude=result[host]['latitude']
        longitude=result[host]['longitude']
        last_update=result[host]['last_update']
        shodan_last_update=result[host]['shodan_last_update']

        print("[=] Hostname: {} ipAddress: {} ISP: {} Organization: {}".format(hostName,ipAddress,isp,org))
        print("\t\t[=] Link: {} ASN: {} Last Update: {}".format(link,asn,last_update))
        print("\t\t[=] Latitude: {} Longitude: {} Last Shodan update: {}".format(latitude,longitude,shodan_last_update))
        query ="select port,protocol,banner,service from tb_port where hostName='{}' and ipAddress='{}' order by 1;".format(hostName,ipAddress)
        resultPorts = execQuery(query)
        if resultPorts:
          for port in range(len(resultPorts)):
            protocol=resultPorts[port]['protocol']
            rport=resultPorts[port]['port']
            banner=resultPorts[port]['banner']
            service=resultPorts[port]['service']
            if banner.decode() == 'Null':
              print("\t\tPort: {} STATUS OPEN Protocol: {} Service: {} Banner: None ".format(rport,protocol,service))
            else:
              print("\t\tPort: {} STATUS OPEN Protocol: {} Service: {} \n\t\t\t\tBanner: ".format(rport,protocol,service))
              line=''
              for w in banner.decode():
                line+=''.join(w)
                if w == '\n':
                  lineprint='\t\t\t\t\t'+line
                  print(lineprint.replace('\r','').replace('\n',''))
                  line=''

        count+=1
    else:
      print("[+] {} Not found in database".format(domain))
    print("[!] Found {} records in database".format(count))

  def hostOnlyMail(self,target):
    # Query a unique hostname in the database; 
    #query ="select tb_host.hostName,tb_host.ipAddress,tb_port.port, tb_port.protocol,tb_port.banner from tb_host inner join tb_port where tb_host.domainName='{}' and tb_port.ipAddress = tb_host.ipAddress order by 1;".format(domain)
    query ="select hostName,ipAddress,isp,link,org,latitude,longitude,last_update,shodan_last_update from tb_host where domainName='{}' and ipAddress != 'False' and hostName LIKE '%mail%' order by 1;".format(target)
    result = execQuery(query)
    if result:
      for host in range(len(result)):
        hostName=result[host]['hostName']
        ipAddress=result[host]['ipAddress']
  #      isp=result[host]['isp']
  #      link=result[host]['link']
  #      org=result[host]['org']
  #      asn=result[host]['asn']
  #      latitude=result[host]['latitude']
  #      longitude=result[host]['longitude']
  #      last_update=result[host]['last_update']
  #      shodan_last_update=result[host]['shodan_last_update']

        print("[=] Hostname: {} ipAddress: {} ".format(hostName,ipAddress))
#        print("\t\t[=] Link: {} ASN: {} Last Update: {}".format(link,asn,last_update))
  #      print("\t\t[=] Latitude: {} Longitude: {} Last Shodan update: {}".format(latitude,longitude,shodan_last_update))
        query ="select port,protocol,banner,service from tb_port where hostName='{}' and ipAddress='{}' order by 1;".format(hostName,ipAddress)
        resultPorts = execQuery(query)
        if resultPorts:
          for port in range(len(resultPorts)):
            protocol=resultPorts[port]['protocol']
            rport=resultPorts[port]['port']
            banner=resultPorts[port]['banner']
            service=resultPorts[port]['service']
            if banner.decode() == 'Null':
              print("\t\tPort: {} STATUS OPEN Protocol: {} Service: {} Banner: None ".format(rport,protocol,service))
            else:
              print("\t\tPort: {} STATUS OPEN Protocol: {} Service: {} \n\t\t\t\tBanner: ".format(rport,protocol,service))
              line=''
              for w in banner.decode():
                line+=''.join(w)
                if w == '\n':
                  lineprint='\t\t\t\t\t'+line
                  print(lineprint.replace('\r','').replace('\n',''))
                  line=''

   #     count+=1
    else:
      print("[+] {} Not found in database".format(domain))
  #  print("[!] Found {} records in database".format(count))

  def hostOnly(self,hostname):
    # Query a unique hostname in the database; 
    #query ="select tb_host.hostName,tb_host.ipAddress,tb_port.port, tb_port.protocol,tb_port.banner from tb_host inner join tb_port where tb_host.domainName='{}' and tb_port.ipAddress = tb_host.ipAddress order by 1;".format(domain)
    query ="select hostName,ipAddress,isp,link,org,latitude,longitude,last_update,shodan_last_update from tb_host where domainName='{}' and ipAddress != 'False' order by 1;".format(domain)
    result = execQuery(query)
    if result:
      for host in range(len(result)):
        hostName=result[host]['hostName']
        ipAddress=result[host]['ipAddress']
        isp=result[host]['isp']
        link=result[host]['link']
        org=result[host]['org']
        asn=result[host]['asn']
        latitude=result[host]['latitude']
        longitude=result[host]['longitude']
        last_update=result[host]['last_update']
        shodan_last_update=result[host]['shodan_last_update']

        print("[=] Hostname: {} ipAddress: {} ISP: {} Organization: {}".format(hostName,ipAddress,isp,org))
        print("\t\t[=] Link: {} ASN: {} Last Update: {}".format(link,asn,last_update))
        print("\t\t[=] Latitude: {} Longitude: {} Last Shodan update: {}".format(latitude,longitude,shodan_last_update))
        query ="select port,protocol,banner,service from tb_port where hostName='{}' and ipAddress='{}' order by 1;".format(hostName,ipAddress)
        resultPorts = execQuery(query)
        if resultPorts:
          for port in range(len(resultPorts)):
            protocol=resultPorts[port]['protocol']
            rport=resultPorts[port]['port']
            banner=resultPorts[port]['banner']
            service=resultPorts[port]['service']
            if banner.decode() == 'Null':
              print("\t\tPort: {} STATUS OPEN Protocol: {} Service: {} Banner: None ".format(rport,protocol,service))
            else:
              print("\t\tPort: {} STATUS OPEN Protocol: {} Service: {} \n\t\t\t\tBanner: ".format(rport,protocol,service))
              line=''
              for w in banner.decode():
                line+=''.join(w)
                if w == '\n':
                  lineprint='\t\t\t\t\t'+line
                  print(lineprint.replace('\r','').replace('\n',''))
                  line=''

        count+=1
    else:
      print("[+] {} Not found in database".format(domain))
    print("[!] Found {} records in database".format(count))

  #query = "select ipAddress, port, banner, protocol from tb_port where hostName = '{}'; ".format(hostname)
  #result = execQuery(query)
  #if result:
  #  print("[!] Hostname: %s" % hostname)
  #  ipAddress=result[0]['ipAddress']
  #  for records in range(len(result)):
  #    port=result[records]['port']
  #    protocol=result[records]['protocol']
  #    banner=result[records]['banner']
  #    print("\t\tPort: %s Protocol: %s \n\t\t\t\tBanner: %s" %(port,protocol,banner))
  #else:
#    print("No records Found")


  def hostsFromDomain(self,domain):
    count=0
    print("[+] Hosts from Domain {}:".format(domain))
    # Total de hosts localizados para o dominio.
    query="select count(hostName) as total from tb_host where domainName='{}';".format(domain)
    result = execQuery(query)
    if result:
      totalHosts=result[0]['total']
    query="select count(hostName) as total from tb_host where ipAddress != 'False' and domainName='{}';".format(domain)
    result = execQuery(query)
    if result:
      totalValidHosts=result[0]['total']
    missing=totalHosts-totalValidHosts
    print("[-] For Domain {}  we have {} hostnames but only {}  has valid IPv4. Hosts missing IPv4: {}".format(domain,totalHosts,totalValidHosts,missing))
  #query ="select tb_host.hostName,tb_host.ipAddress,tb_port.port, tb_port.protocol,tb_port.banner from tb_host inner join tb_port where tb_host.domainName='{}' and tb_port.ipAddress = tb_host.ipAddress order by 1;".format(domain)
  #query="INSERT INTO tb_host(ipAddress,domainName, hostName, latitude, longitude, isp, os, org, asn, link, country_code, shodan_last_update, createdAt) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}',{}',CURRENT_TIMESTAMP);".format(ipAddress,domainName,hostName,latitude,longitude,isp,os,asn,link,country_code,shodan_last_update)
    query ="select hostName,ipAddress,isp,org from tb_host where domainName='{}' and ipAddress != 'False' order by 1;".format(domain)
    result = execQuery(query)
    if result:
      for host in range(len(result)):
        hostName=result[host]['hostName']
        ipAddress=result[host]['ipAddress']
        isp=result[host]['isp']
        org=result[host]['org']
        print("[=] Hostname: {} ipAddress: {} ISP: {} Organization: {}".format(hostName,ipAddress,isp,org))
        query ="select port,protocol,banner from tb_port where hostName = '{}' order by 1;".format(hostName)
        resultPorts = execQuery(query)
        if resultPorts:
          for port in range(len(resultPorts)):
            protocol=resultPorts[port]['protocol']
            rport=resultPorts[port]['port']
            banner=resultPorts[port]['banner']
            if banner.decode() == 'Null':
              print("\t\tPort: {} STATUS OPEN Protocol: {} Banner: None ".format(rport,protocol))
            else:
              print("\t\tPort: {} STATUS OPEN Protocol: {} \n\t\t\t\tBanner: ".format(rport,protocol))
              line=''
              for w in banner.decode():
                line+=''.join(w)
                if w == '\n':
                  lineprint='\t\t\t\t\t'+line
                  print(lineprint.replace('\r','').replace('\n',''))
                  line=''

        count+=1
    else:
      print("[+] {} Not found in database".format(domain))
    print("[!] Found {} records in database".format(count))

  def relatedDomains(self,domain):
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

  def pastebin(self,domain):
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

  def buckets(self,domain):
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

  def makeReport(self,domain):
    pastebin(domain)
    buckets(domain)
    hostsFromDomain(domain)
    relatedDomains(domain)

  def usage(self):
    print("""
    report_maker <opt> <target>
    OPT:
    list-domains: Will list domains in the database
    report: Will make a full report for a specified domain
    buckets: Will list buckets from a specified domain
    related-domains: Will list related domains from a specified domain 
    hosts-from-domain: Will list all hosts from a domain
    host: Will query only the specified host
    usage: this shit
    """)
    exit(1)

if __name__ == "__main__":
  import sys
  rpt = report()
  if len(sys.argv) < 2:
    rpt.usage()
  if len(sys.argv) >=3:
    domain_name = sys.argv[2]
  if len(sys.argv) >=2:
    opt=sys.argv[1]

  if opt == 'list-domains':
    rpt.listDomains()
  elif opt=='report':
    makeReport(domain_name)
  elif opt=='buckets':
    buckets(domain_name)
  elif opt=='related-domains':
    relatedDomains(domain_name)
  elif opt=='hosts-from-domain':
    hostsFromDomain(domain_name)
  elif opt=='host':
    hostOnly(domain_name)
  elif opt=='hosts-from-domain-mail':
    hostOnlyMail(domain_name)
  else:
    print("[!!] Invalid Option")

