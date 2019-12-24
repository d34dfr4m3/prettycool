#!/usr/bin/python3
import pymysql.cursors
def createCon():
  connection = pymysql.connect(host='localhost',
                             user='prettycool',
                             password='FRESHINSTALL',
                             db='db_data',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
  return connection 


def commit(query):
  connection = createCon()
  try: 
    with connection.cursor() as cursor:
      cursor.execute(query)
      connection.commit()
  except Exception as error:
    print("[!!] Error in commit: %s" %(error))
  finally:
      connection.close()

def execQuery(query):
  connection = createCon()
  try: 
    with connection.cursor() as cursor:
      cursor.execute(query)
      result=cursor.fetchall()
      if len(result) > 0:
        return result
  except Exception as error:
    print("[!!][ERROR] EXECQUERY: %s" %(error))
  finally:
      connection.close()
      pass

def checkDB(query):
  connection = createCon()
  try:
    with connection.cursor() as cursor:
      cursor.execute(query)
      result=cursor.fetchall()
      if len(result) == 0:
        return True
  except Exception as error:
    print("[!!] Error in checkDB: "+str(error))
    return False
  finally:
    connection.close()

def domainAdd(domain):
  query="select domainName from tb_domain where domainName = '{}';".format(domain)
  if checkDB(query):
    query="INSERT INTO tb_domain(domainName,createdAt) values ('{}', CURRENT_TIMESTAMP);".format(domain)
    commit(query)
    return True
  else:
    return False


#def hostUpdate(ipAddress,domainName,hostName,latitude='Null',longitude='Null',isp='Null',os='Null',asn='Null',link='Null',country_code='Null',shodan_last_update='Null'):
# Update de hosts terá como métrica o número de caracteres em cada campo? Tempo? Ambos? 
# Por hora acredito que é melhor seguir, atualizar se o novo registro for maior que o anterior(char count shit). 

def hostUpdate(update_payload):
  badChars=["'",'"']
  hostName=update_payload['hostName']
  query="SELECT * from tb_host where hostName='{}';".format(hostName)
  results=execQuery(query)
  if results:
    records=results[0]
    for key in records.keys():
      if key in update_payload:
        if len(str(update_payload[key])) > len(str(records[key])):
          clean_value=str(update_payload[key])
          for badchar in badChars:
            aux=clean_value
            clean_value=aux.replace(badchar,'')
            auxk=key
            key=auxk.replace(badchar,'')
          query="update tb_host set {}='{}', last_update=CURRENT_TIMESTAMP where hostName='{}';".format(key,clean_value,hostName) 
          commit(query)
          print("[-] Updating %s" % hostName)

  
def hostAdd(ipAddress,domainName,hostName,latitude='Null',longitude='Null',isp='Null',os='Null',asn='Null',link='Null',country_code='Null',shodan_last_update='Null'):
  query="SELECT hostName from tb_host where hostName='{}';".format(hostName)
  if checkDB(query):
    query="INSERT INTO tb_host(ipAddress,domainName, hostName, latitude, longitude, isp, os,  asn, link, country_code, shodan_last_update, createdAt) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}',CURRENT_TIMESTAMP);".format(ipAddress, domainName, hostName, latitude, longitude, isp, os,  asn, link, country_code, shodan_last_update)
    commit(query)
    return True
  else:
    print("[+] Warning: hostAdd -> Host {} already exist on database".format(hostName))
    return False

def portAdd(ipAddress,port,hostName,protocol='Null',banner='Null',service='Null'):
  query="SELECT port from tb_port where ipAddress='{}' and port='{}';".format(ipAddress,port)
  if checkDB(query):
    clean_banner=banner.replace("'","")
    query="INSERT INTO tb_port(ipAddress,port,hostName,banner,service,createdAt) VALUES ('{}','{}','{}','{}','{}', CURRENT_TIMESTAMP);".format(ipAddress,port,hostName,clean_banner,service)
    commit(query)
  else:
    print("[+] Warning: portAdd -> Host: {} Port: {} already exist on database".format(hostName,port))
    return False

def pasteAdd(domainName,url,title,dumpDate):
  query="SELECT url from tb_pastebin where url='{}';".format(url)
  if checkDB(query):
    query="INSERT INTO tb_pastebin(domainName,url,title,dumpDate, createdAt) VALUES ('{}','{}','{}','{}',CURRENT_TIMESTAMP);".format(domainName, url,title,dumpDate)
    commit(query)

def s3Add(domainName,url):
  query="SELECT url from tb_aws where url='{}';".format(url)
  if checkDB(query):
    query="INSERT INTO tb_aws(domainName,url,createdAt) VALUES ('{}','{}',CURRENT_TIMESTAMP);".format(domainName, url)
    commit(query)

def relatedDomainAdd(mainDomain,domainName):
  query="SELECT domainName from tb_relatedDomains where domainName='{}' and mainDomain='{}';".format(domainName,mainDomain)
  if checkDB(query):
    query="INSERT INTO tb_relatedDomains( mainDomain, domainName,createdAt) VALUES ('{}','{}',CURRENT_TIMESTAMP);".format(mainDomain, domainName)
    commit(query)


def appAddContent(app_payload):
  hostName=app_payload['hostName'] if 'hostName' in app_payload else False
  port=app_payload['port'] if 'port' in app_payload else False
  ipAddress=app_payload['ipAddress'] if 'ipAddress' in app_payload else False
  url=app_payload['url'] if 'url' in app_payload else False
  page_content=app_payload['page_content'] if 'page_content' in app_payload else False
  status_code=app_payload['status_code'] if 'status_code' in app_payload else False
  sitemap_hash=app_payload['sitemap_hash'] if 'sitemap_hash' in app_payload else False

  if not url:
    return False
  query="select url from tb_applicationContent where url='{}';".format(url)
  if checkDB(query):
    query="select app.idApp as id  from tb_application as app inner join tb_port as prt where prt.hostname='{}'  and prt.port={} and prt.ipAddress='{}';".format(hostName,port,ipAddress)
    get_idapp=execQuery(query)
    if get_idapp:
      idApp=get_idapp[0]['id'] if 'id' in get_idapp[0] else False
      if idApp:
        badChars=["'",'"']
        for badchar in badChars:
          aux=url
          url=aux.replace(badchar,'')
          auxk=page_content
          page_content=auxk.replace(badchar,'')
        query="insert into tb_applicationContent(idApp,url,page_content,status_code,sitemap_hash,createdAt) VALUES('{}','{}','{}','{}','{}', CURRENT_TIMESTAMP );".format(idApp,url,page_content,status_code,sitemap_hash)
        commit(query)

def appAdd(app_payload):
  url=app_payload['url'] if 'url' in app_payload else False
  if url:
    query="select url from tb_application where url='{}'".format(url)
    if checkDB(query):
      #Get idPort 
      port=app_payload['port'] if 'port' in app_payload else False
      applicationName=app_payload['applicationName'] if 'applicationName' in app_payload else False
      hostName=app_payload['hostName'] if 'hostName' in app_payload else False
      ipAddress=app_payload['ipAddress'] if 'ipAddress' in app_payload else False
      service=app_payload['service'] if 'service' in app_payload else False
      if port or hostName or ipAddress:
        return False
      query="select idPort as id from tb_port where port={} and hostName='{}' and ipAddress='{}';".format(port,hostName,ipAddress)
      get_idport=execQuery(query)
      print('GET_IDPORT')
      print(get_idport)
      if not get_idport:
        return False
      idPort=get_idport[0]['id'] if 'id' in get_idport[0] else False
      if idPort:
        query="insert into tb_application(idPort,applicationName,url,service,createdAt) VALUES('{}','{}','{}','{}', CURRENT_TIMESTAMP );".format(idPort,applicationName,url,service) 
        commit(query)
        print("ipPort: {} applicationName: {} URL: {} service: {}".format(idPort,applicationName,url,service))


if __name__ == "__main__":
#  hostUpdate(ipAddress,domainName,hostName,latitude='Null',longitude='Null',isp='Null',os='Null',asn='Null',link='Null',country_code='Null',shodan_last_update='Null'):
#  hostUpdate('123.123.123.123','xiaomi.com','www.push.a.xiaomi.com','1234','12345','fudencio','linux','ASNBOLADA','fuked','BR','12:30')
  app_payload={}
  app_payload['port']='80'
  app_payload['url']='http://fodase.com/kk'
  app_payload['hostName']='devblog.pubg.com'
  app_payload['applicationName']='Viva Caralho'
  app_payload['ipAddress']='34.233.207.143'
  app_payload['service']='apache2noia'
  appAdd(app_payload)
