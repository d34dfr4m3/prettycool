#!/usr/bin/python3
class masscan:
  def __init__(self,target_host,target_ip):
    self.target_host = target_host
    self.target_ip  = target_ip

  def run(self):
    hostname = self.target_host
    ipAddress = self.target_ip
    print("[!] Disparando Masscan")
    outputStandart='/tmp/masscan_output_'
    target=ipAddress
    fileName=outputStandart+ipAddress
    FNULL = open(os.devnull, 'w')
    processHandler = subprocess.run(['masscan', ipAddress, '-Pn','--ports' ,'1-65535', '-oJ', fileName, '--banners','--connection-timeout', '3','--wait', '3', '--http-user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36', '--source-port','61000' ], stdout=FNULL,stderr=subprocess.STDOUT)
    FNULL.close()
    if os.stat(fileName).st_size == 0:
      return False
    data = open(fileName,'r')
    payload=json.loads(data.read())
    data.close()
    for host in range(len(payload)):
      print("[+][MASSSCAN] Result for hostname: {} ipAddress: {}".format(hostname,payload[host]['ip']))
      for port in range(len(payload[host]['ports'])):
        host_port=payload[host]['ports'][port]['port']
        if 'service' in payload[host]['ports'][port]:
          service_name=payload[host]['ports'][port]['service']['name']
          service_banner=payload[host]['ports'][port]['service']['banner']
        else:
          service_name='Null'
          service_banner='Null'
        print('\t[+] Open Port: {} Service: {} Banner: \n\t\t{}'.format(host_port,service_name,service_banner))
        try:
          db_controler.portAdd(ipAddress,host_port,hostname,service_name,service_banner)
        except Exception as error:
          print("Error:"+str(error))
    print("[=] Cleaning temp dir")
    processHandler = subprocess.run(['rm', '-f', fileName])
    if [ processHandler.check_returncode() == 0  ]:
      print("[+] Arquivo {} foi removido".format(fileName))
    else:
      print("[*] Falha oa excluir arquivo {}, erro: {}".format(fileName,processHandler.check_returncode()))

if __name__ == "__main__":
  import sys
  scan = masscan(sys.argv[1],sys.argv[2]) # hostname,ipaddress
  scan.run()
