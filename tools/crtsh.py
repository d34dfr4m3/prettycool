import requests
from bs4 import BeautifulSoup

class crtsh:
  def __init__(self):
    pass

  def getHosts(self,domainName): 
    print("[-] Searching in crtsh")
    try:
      data = requests.get('https://crt.sh/?q=%.'+domainName)
    except Exception as error:
      print("[-][CRTSH] Error while requesting source: %s" % error)
      return False
    page = BeautifulSoup(data.text,'html.parser')
    badChars=['*',' ','crt.sh','%','Identity','LIKE',"'"] 
    target_list=[]
    payload={'domainName':domainName,'data':[]}
    for domain in page.find_all('td'):
      clean=True
      domaintxt = domain.get_text()
      if domainName in domaintxt:
        hostname=domaintxt.split('>')[0].split('<')[0]
        if not len(hostname) >=100:
          for badchar in badChars:
            if badchar in hostname:
              clean=False
          if hostname not in target_list and domainName in hostname and clean:
            target_list.append(hostname)
            print("[+][CRTSH] HOSTNAME: %s" %(hostname))
            hostData={'hostname':hostname}
            payload['data'].append(hostData)
            #payload={'domainName':domainName,data=[{'hostname':hostname} }]}

    #Send to orquestrator
        #    avoidDuplicata(hostname)
