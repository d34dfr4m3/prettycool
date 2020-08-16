#!/usr/bin/python3
class mycensys:
  def __init__(self,uid,secret):
  self.uid  = uid
  self.secret = secret
  self.api_url = "https://censys.io/api/v1" 
  self.api_url_health = self.api_url + "/account" 
  
  def api_auth(self):
    print("Auth function")

  def health_check(self)
    page=requests.get(self.api_url_health, auth=(self.uid,self.secret))
    left=int(page.json()['quota']['allowance'])-int(page.json()['quota']['used'])
    if left > 50:
      print("[!!] Censys API has only {} requests left".format(str(left)))
    elif left > 20:
      print("[!!] Censys API has only {} requests left".format(str(left)))
    elif left > 10:
      print("[!!] Censys API has only {} requests left".format(str(left)))
    elif left <= 0:
      CENSYS_DEAD = True
      # Pick up another key right guys! 
      print("[!!] Censys API has no credits to use")
    else:
      print("[!!] Censys API is ready to rock with {} requests left".format(left))

  def enum(self,ipAddress,hostName): 
    self.uid
    self.secret
    global CENSYS_DEAD
    if CENSYS_DEAD:
      return False
    web_protocols=['http','https']
    auth = requests.get(API_URL + "/data", auth=(self.uid,self.secret))
    if auth.status_code != 200:
        print("[+] Auth Error: ", auth.json()['error'])
        CENSYS_DEAD=True
    else:
      params={'query':ipAddress, 'page':10}
      try: 
        page=requests.post(API_URL+"/search/ipv4", json=params,auth=(censys_UID,censys_SECRET))
        num_results = page.json()['metadata']['count']
        if num_results > 0:
          page=requests.get(API_URL+"/view/ipv4/"+ipAddress, auth=(censys_UID,censys_SECRET))
          for protocol in range(len(page.json()['protocols'])):
            port = page.json()['protocols'][protocol].split('/')[0]
            proto = page.json()['protocols'][protocol].split('/')[1]
            if proto in web_protocols:
              if 'title' in page.json()[port][proto]['get'].keys():
                title=page.json()[port][proto]['get']['title']
                protocol=page.json()['protocols'][protocol]
                print("\t[+] Protocol: {}  Title: {} ".format(page.json()['protocols'][proto], title))
              else:
                print("\t[+] Protocol: {}".format(page.json()['protocols'][protocol]))
#        db_controler.portAdd(ipAddress,port,hostName,protocol)
      except Exception as error: 
        print("[!} Error Censys:", str(error))

    
if __name__ == "__main__":
  import sys
  target=sys.argv[1]
#  hostName=sys.argv[2]
 # spyse_subdomains(target)     
  spyse_related_domain(target) 
 # spyse_ip(target,hostName)
