#!/usr/bin/python3
import getopt
import sys
import json
#local
from tools.shodan import shodan
from tools.crtsh import crtsh

def usage():
  usage_str="""
usage stuff
shodan 
            shodan ip <ipAddress>: Grab information about ports 
            shodan hostnames <domain>
lorem iplum

  """
  shodan_help()
  censys_help()
  print(usage_str)
  exit(2)
def censys_help():
  censysString="""
            Censys Help Options:
                  hostNames <domain> Get hosts from a domain
                  hostIp <IPv4> Get ports, banners from a IP
               """
  print(censysString)

def crtsh_help():
  crtshString="""
            crtsh Help Options:
                  getHosts <domain>  - Get hosts from a domain
               """
  print(crtshString)

def shodan_help():
  shodanString="""
            Shodan Help Options:
                  hostNames <domain>  - Get hosts from a domain
                  hostIp <IPv4>  - Get ports, banners from a IP
                  check_honeypot <IPv4> - Check the chance a IP could be a HoneyPot
               """
  print(shodanString)

def parserInput(entrydata):
 cleanEntry={}
 requestData=entrydata[0].split(',')
 for host in requestData:
   hostData=(host.split(':'))
   hostname=hostData[0]
   ipAddress=hostData[1]
   cleanEntry[hostname]=ipAddress
 return cleanEntry

if __name__ == '__main__':
  param_list=['shodan', 'censys','crtsh','help']
  try:
    opts,args = getopt.getopt(sys.argv[1:], 'h', param_list)
  except getopt.GetoptError as err:
    print("[!!] GETOPT Error: %s"  % err)
    usage()
  if not len(opts) == 1:
    usage()
  for o,a in opts:
    if o == '--shodan':
      if len(args) > 1:
        shodan_params=['hostnames', 'ip','honeypot']
        if args[0] in shodan_params:
          method=args[0]
          shodanobj=shodan()
          if method == 'hostnames': 
            domain=args[1]
            shodanobj.hostNames(domain)
          elif method == 'ip':
            targets=parserInput(sys.argv[3:])
            for hostname in targets.keys():
              ipAddress=targets[hostname]
#              print('Hostname: %s ipAddress: %s ' %(hostname, ipAddress))
              shodanobj.hostIp(ipAddress, hostname)
          elif method == 'honeypot':   
            ipAddress=sys.argv[3]
            shodanobj.check_honeypot(ipAddress)
    
          else:
            shodan_help()
        else:
          shodan_help()
    elif o == '--censys':
      pass
    elif o =='--crtsh':
      crtsh_params=['getHosts']
      if args[0] in crtsh_params:
        method=args[0]
        crtshObj=crtsh()
        if method == 'getHosts':
          domainName=args[1]
          crtshObj.getHosts(domainName)
      else: 
        crtsh_help()
        exit(1)
    else:
      usage()
