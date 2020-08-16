#!/usr/bin/python3
class mypastebin:
  def __init__(self,target_domain):
    self.target_domain = target_domain 
    self.url_psbdmp = 'https://psbdmp.ws/api/search/%s' %(self.target_domain)
    self.url_psb = "https://pastebin.com/"

  def psbdmp(self):
    pasteList={}
    print("[!][STARTING PSBDMP] Target  %s" %(self.target_domaintarget))
    data = requests.get(self.url_psbdmp)
    payload = data.json()
    for ids in range(len(payload['data'])):
       check = requests.get(self.url_psb+payload['data'][ids]['id'])
       if check.status_code == 200:
         page = BeautifulSoup(check.text,'html.parser')
         url=self.url_psb+str(payload['data'][ids]['id'])
         title=page.title.get_text()
         date=page.findAll('span',limit=11)[10].contents[0]
         print('[!][PSBDMP] Found: {} Date: {} Title: {}'.format(url,date,title))
         try:
            pass
  #         db_controler.pasteAdd(target,url,title,date)
         except Exception as error:
           print("Pastebin error: {}".format(error))
         pasteList[url]={date:title}
    return pasteList

if __name__ == "__main__":
  import sys
  target=sys.argv[1]
  search = mypastebin(sys.argv[1])
  search.psbdmp()
