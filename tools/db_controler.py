#!/usr/bin/python
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

def hostAdd(ipAddress,domainName,hostName):
  query="SELECT hostName from tb_host where hostName='{}';".format(hostName)
  if checkDB(query):
    query="INSERT INTO tb_host(ipAddress,domainName, hostName, createdAt) VALUES ('{}','{}','{}',CURRENT_TIMESTAMP);".format(ipAddress,domainName,hostName)
    commit(query)
    return True
  else:
    print("[+] Warning: hostAdd -> Host {} already exist on database".format(hostName))
    return False

def portAdd(ipAddress,port,hostName,protocol='Null',banner='Null'):
  query="SELECT port from tb_port where ipAddress='{}' and port='{}';".format(ipAddress,port)
  if checkDB(query):
    query="INSERT INTO tb_port(ipAddress,port,hostName,banner,createdAt) VALUES ('{}','{}','{}','{}',CURRENT_TIMESTAMP);".format(ipAddress,port,hostName,banner)
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
