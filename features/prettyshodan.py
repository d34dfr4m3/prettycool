#!/usr/bin/python3
import requests
import json
## buscar por hosts atraves da url "https://api.shodan.io/shodan/host/search?key=&query=hostname:HERE 
## Busca por IP dps 
class myshodan:
  def __init__(self,target,api_key):
    self.api_key = api_key
    self.target_host = target
    #self.url_api_host = 'https://api.shodan.io/shodan/host/%s/key=%s' %(self.target_host,self.api_key)
    self.url_api_host = 'https://api.shodan.io/shodan/host/search?key=%s&query=hostname:%s' %(self.api_key,self.target_host)
    self.url_api_discovery = "https://api.shodan.io/dns/domain/%s?key=%s" %(self.target_host,self.api_key) # Not a host, its is a domain
    self.url_api_scan = 'https://api.shodan.io/shodan/scan?key=%s' %(self.api_key)
    self.url_api_info = 'https://api.shodan.io/api-info?key=%s' %(self.api_key)
    self.url_api_honeypot = "https://api.shodan.io/labs/honeyscore/%s?key=%s" %(self.target_host,self.api_key)
    #self.health = health status boolean, true ok false dead, if false, the core do not use this shit  

  def health_check(self):
    page = requests.get(self.url_api_info)
    creds = int(page.json()['unlocked_left'])
    if creds == 0:
      print("[!!] Shodan API is dead!")
      return False
    elif creds < 25:
      print("[!!] Shodan API has only %s requests left" %(creds)) 
      return True
    else:
      print("[!!] Shodan API is ready to rock with %s requests left" %(creds)) 
      return True

  def host_enum(self):
      host_update={}
      try:
        data = requests.get(self.url_api_host)
        payload=data.json()
#        print(payload['matches'])
#        print(len(payload['matches']))
      except Exception as err:
        print("\t[SHODAN]ERROR: Miss or error: {}".format(err))
      if not len(payload) > 0:
        return False
      last_update=payload['last_update'] if 'last_update' in payload else False
      if not 'matches' in payload:
        return False
      payload_data=payload['matches']
      for i in range(len(payload_data)):
        port=payload_data[i]['port'] if 'port' in payload_data[i] else False
        target=payload_data[i]['hostnames'] if 'hostnames' in payload_data[i] else False
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
      
        print('[*][SHODAN] Last Update for %s : %s' % (target,last_update))
        print("\t[+][SHODAN] OS: {} ISP: {} Org: {} ASN: {} link: {}".format(ops,isp,org,asn,link))
        print("\t[+][SHODAN] Country: {} Longitude: {} Latitude: {}".format(country_code,longitude,latitude))
    #HOST UPDATE HERE DBCONTROLER
#    host_update['hostName']=hostname
        host_update['country_code']=country_code
        host_update['latitude']=latitude
        host_update['longitude']=longitude
        host_update['os']=ops
        host_update['isp']=isp
        host_update['asn']=asn
        host_update['link']=link
        host_update['shodan_last_update']=last_update
#    db_controler.hostUpdate(host_update)
        port_service=str(product)+' '+str(version)
        port_module=str(port)+'/'+str(module)
      ## Create a new function if http is present
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
          print("\t\t\t[-] Securitytxt:  {} Sitemap: {}".format(securitytxt,sitemap_hash))
          print("\t\t\t[-] Robots:  {}".format(robots))
    #  print("\t\t\t{}".format(html))
    #Insert into tb_application
          app_payload={}
          app_payload['port']=port
          app_payload['applicationName']=title
#      app_payload['hostName']=hostname
          app_payload['url']=url_path
          app_payload['ipAddress']=target
          app_payload['service']=server
#      db_controler.appAdd(app_payload)
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
 #       db_controler.appAddContent(app_payload)
          if html:
            app_payload['url']=url_path
            app_payload['page_content']=html
            l1=banner.splitlines(1)[0]
            status_code=l1.split(' ')[1]
            app_payload['status_code']=status_code
  #      db_controler.appAddContent(app_payload)

        print("\t[+][SHODAN] OS: {} ISP: {} Org: {} ASN: {} link: {}".format(port_module,port_service,ops,isp,org,asn,link))
        print('\t[+][SHODAN] Open Port: {} Product: {}  \n\t\t Banner: {}'.format(port,product,banner))
    #db_controler.portAdd(target,port,hostname,module,banner,port_service)
    #check_banner(hostname,banner,port,ipAddress)

  def host_discovery(self):
    data = requests.get(self.url_api_discovery)
    payload = data.json()
    discovery_total=len(payload["subdomains"]) if "subdomains" in payload else False
    if not discovery_total:
      return False
    print("[+][SHODAN] Found {} Subdomains from Target Domain: {}".format(discovery_total,self.target_host))
    payload_data=payload['data']
    for i in range(len(payload_data)):
      value=payload_data[i]['value'] if 'value' in payload_data[i] else False
      subdomain=payload_data[i]['subdomain'] if 'subdomain' in payload_data[i] else False
      subdomain+="."+self.target_host
      ports=payload_data[i]['ports'] if 'ports' in payload_data[i] else False
      last_seen=payload_data[i]['last_seen'] if 'last_seen' in payload_data[i] else False
      print("\t[+][SHODAN] Subdomain: {} Value: {} Last Seen: {}".format(subdomain,value,last_seen))
      print("\t\t[-] Open Ports: {}".format(ports))

  def run_scan(self):
    url=self.url_api_scan+self.api_key
    self.target_host
    post_payload={'ips':target_host}
    try:
      data=requests.post(url,data=post_payload)
      scan_id=data.json()['id']  # Save in the database
      count=data.json()['count'] # ?
      credits_left=data.json()['credits_left']  # Pass to a health check function
      print("[-] Scan started at ID: {} Count: {} Credits Left: {}".format(scan_id,count,credits_left))
    except Exception as error:
      print("Erorr: {}".format(error))


  def scan_check(scan_id):
    global shodan_key
    url='https://api.shodan.io/shodan/scan/{}?key={}'.format(scan_id,shodan_key)
    try:
      data=requests.get(url)
      scan_id=data.json()['id'] 
      count=data.json()['count'] 
      scan_status=data.json()['status'] 
      created=data.json()['created'] 
      print("[-] Scan ID: {} Created at {} is {} Count: {}".format(scan_id,created,scan_status,count))
    except Exception as error:
      print("Erorr: {}".format(error))

#  def shodan_scan_result(target_file): ## Run shodan host again
#    global shodan_key
#    url='https://api.shodan.io/shodan/scan?key={}'.format(shodan_key)
#    ips_file=open(target_file)
#    pre_ips=''
#    for ip in ips_file:
#      shodan_host(ip.replace('\n',''))

  def check_honeypot(self):
    print("[+][ STARTING SHODAN HONEYPOT CHECKER] Target: %s" %(self.target_host))
    check=requests.get(self.url_api_honeypot)
    if check.status_code == 200: 
      honeyInd=float(check.text)
      if honeyInd == 1:
        print("It is a HoneyPot")
      elif honeyInd >= 0.5:
        print("%50")
      elif honeyInd == 0:
        print('is not a honeypot')
    print("honeyscore: {}".format(honeyInd))

# main
if __name__ == "__main__":
  import sys
#  target_file=sys.argv[1]
  target_domain=sys.argv[1]
  api_key=sys.argv[2]
  shd = myshodan(target_domain,api_key)
  shd.health_check()
  shd.host_enum()
#  shodan_scan_start(target_domain)
#  shodan_scan_check(target_domain)
#  shodan_scan_result(target_domain)
#  shodan_host(target_domain)


