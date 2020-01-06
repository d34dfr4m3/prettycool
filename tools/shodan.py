import json
import requests
global url_orq
url_orq='http://127.0.0.1:1337/shodan'

class shodan:
  def __init__(self):
    pass

  def check_honeypot(self,ipAddress):
    shodan_key=''
    url='https://api.shodan.io/labs/honeyscore/{}?key={}'.format(ipAddress,shodan_key)
    check=requests.get(url)
    if check.status_code == 200:
      honeyInd = float(check.text)
      chance = honeyInd * 100
      payload={'honeypot':[]}
      payload['honeypot'].append({'ipAddress':ipAddress,'chance':chance})
      print(f"[!][SHDOAN] Percent of HoneyPot Chance {chance}")
      try:
        orq_data = requests.post(url_orq, data=payload)
      except Exception as error: 
        print("[!][SHODAN] Post data to orquestrator failed: %s" % error)
      code=orq_data.status_code
      if not code == 200:
        print("[*][SHODAN] Post data to orquestrator return codes: %s" % code)

  def hostIp(self, target, hostname):
    shodan_key=''
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
      print("\t[+][SHODAN] OS: {} ISP: {} Org: {} ASN: {} link: {}".format(ops,isp,org,asn,link))
      print("\t[+][SHODAN] Country: {} Longitude: {} Latitude: {}".format(country_code,longitude,latitude))
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
#      db_controler.hostUpdate(host_update)
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

        print("\t\t[+][SHODAN] - WebApp found Title:{} URL: {} Service:{}".format(title,host_http,url_path,server))
#        print("\t\t\t[-] Securitytxt:  {} Sitemap: {}".format(securitytxt,sitemap_hash))
#        print("\t\t\t[-] Robots:  {}".format(robots))
#        print("\t\t\t{}".format(html))
      #Insert into tb_application
        app_payload={}
        app_payload['port']=port
        app_payload['applicationName']=title
        app_payload['hostName']=hostname
        app_payload['url']=url_path
        app_payload['ipAddress']=target
        app_payload['service']=server
       #db_controler.appAdd(app_payload)
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
       #   db_controler.appAddContent(app_payload)
        if html:
          app_payload['url']=url_path
          app_payload['page_content']=html
          l1=banner.splitlines(1)[0]
          status_code=l1.split(' ')[1]
          app_payload['status_code']=status_code
      #    db_controler.appAddContent(app_payload)
      else:
        print("\t[+][SHODAN] Port: {} ".format(port_module))

  def hostNames(self,domain):
    shodan_key=''
    url='https://api.shodan.io/dns/domain/{}?key={}'.format(domain,shodan_key)
    data = requests.get(url)
    payload = { "domain": domain,'hosts': [] } 
    if data.status_code == 200:
      dataJson=data.json()
#    data=open('tools/mock/shodan_dns_domain','r')
#    dataJson=json.load(data)
    if len(dataJson) > 0:
      domain=dataJson['domain']
      dataJsonData=(dataJson['data'])
      for subdomain in range(len(dataJsonData)):
        dataSubdomain=dataJsonData[subdomain]
        if len(dataSubdomain['subdomain']) > 0:
          hostname=dataSubdomain['subdomain'] 
          if dataSubdomain['type'] == 'A':
            ipAddress=dataSubdomain['value']
            last_seen=dataSubdomain['last_seen']
            fqdn='%s.%s' % (hostname,domain)
            hostData={'hostname':fqdn,'ipAddress':ipAddress,'last_seen':last_seen}
            payload['hosts'].append(hostData)
            print("[+][SHODAN] Hostname: %s ipAddress %s Last Seen %s " %(fqdn,ipAddress,last_seen))

        else:
          pass

    if len(payload['hosts']) < 1:
      return False
    else: 
      try:
        url_orq='http://127.0.0.1:1337/shodan'
        orq_data = requests.post(url_orq, data=payload)
      except Exception as error: 
        print("[!][SHODAN] Post data to orquestrator failed: %s" % error)
      code=orq_data.status_code
      if not code == 200:
        print("[!][SHODAN] Post data to orquestrator return codes: %s" % code)
