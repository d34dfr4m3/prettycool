```
   +-----------------------------------------------------------------------------+
   |  [!] Legal disclaimer: Usage of this shit program for attacking targets     |
   |  without prior mutual consent is illegal.                                   |
   |  It is the end user's responsibility to obey all applicable local, state and|
   |  federal laws.                                                              |
   |  Developers assume no liability and are not responsible for any misuse or   |
   |  damage caused by this program                                              |
   +-----------------------------------------------------------------------------+
```
## Passive Recon Tool 
This tool use few API's to grab data from domains.
Passive scan
Active scan
Search for relative data in AWS and Pastebin
someday far way i will write a pretty cool readme, but not today guys


## How it works?
I draw someshit here, it is outdated anyway, i will update after I finish some code stuff
![pipeline](docs/fluxogram.jpeg)

### Python3 Requirement 
- PyMySQL
- shodan
- json
- threading
- os
- time
- requests
- BeautifulSoup
- subprocess
- getopt

### Required Programns
- masscan
- pwgen
- mariadb-server 10.3.20-MariaDB [ Fucking required, >=]


### Instalation: 
```
git clone https://github.com/d34dfr4m3/prettycool.git
cd prettyCool/install
sudo ./install.sh #and pray a while
```

### Configuration(not required because I automate this shit): 
Edit the file tools/report_maker.py and set the password: 

```
def createCon():
  connection = pymysql.connect(host='localhost',
                             user='prettycool',
                             password='',
                             db='db_data',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
  return connection 
```

Edit the file tools/db_controler.py and set the password: 

```
def createCon():
  connection = pymysql.connect(host='localhost',
                             user='prettycool',
                             password='',
                             db='db_data',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
  return connection 
```

### database: 

```
+-----------+--------------+
| cd_status | status_value |
+-----------+--------------+
|         1 | NOT STARTED  |
|         2 | STARTED      |
|         3 | FINISHED     |
|         4 | ERROR        |
|         5 | WAITING      |
|         6 | BURNED       |
|         7 | FINE         |
+-----------+--------------+
7 rows in set (0.001 sec)

```
# Fluxo
1. Input Domain
2. Check the domain in db 
3. Start Host Discovery 
- Shodan 
- Censys (Returns: Ipaddress, Location,ASN, ASN ASN Name, ASN Description, ASN PREFIX, Service Port, Service Name, TCP Certificate)
- CRT.SH (Returns: Hostname)
- CertSpooter (Returns: Hostname)
- VirusTotal (Returns: Hostname)
- SecurityTrails (Returns: Hostname)
- Spyse
-  DNSBuffer (Returns: Hostname, ipaddress)
4. Check Enum from host db 
5. Host Enum 
- Censys
- Shodan
6. Check Service enum in DB
7. Start Service enum 
- WayBackMachine

# Data Sources:
## Discovery (Footprint)
### Proposal: 
- Enum subdmains 

### Sources 
- Shodan: Used to get services at hosts. (https://api.shodan.io)
-- DONE  /dns/domain/{domain} (1 credit by request) + Enum ports
-- DONE /shodan/host/search (Search by domain name) + Enum ports and services
- Censys: Used to get services at hosts. (https://censys.io)
-- DONE /v2/hosts/search Returns previews of hosts matching a specified search query - Enum + ports and Services
-- /v2/hosts/{ip} Returns host information for the specified IP address
-- /v2/hosts/{ip}/names Returns host names for the specified IP address
--- https://search.censys.io/api#/hosts/searchHosts
- DONE Crt.sh: Used to enumerate hosts from domain and subdomains. (https://crt.sh)
- DONE Certspooter: Used to enumerate hosts from domain and subdomains (https://certspotter.com)
- VirusTottal: Used to enumerate hosts from domain and subdomains. (https://www.virustotal.com)
- SecurityTrails: Used to enumerate hosts from domain and subdomains. (https://api.securitytrails.com)
- Spyse Used to get hosts from domain and ports from hosts (https://api.spyse.com/)
- DONE dnsbuffer
# Discovery
#### Censys (Features ok)
- Docs https://search.censys.io/search/language?resource=hosts
- Api Docs https://search.censys.io/api

API Endpoints
- (Discovery/ENUM) - /v2/hosts/search - Accepts queries for host or service attributes provided in the Censys Search Language and returns a list of matching hosts with some summary fields.
Returns previews of hosts matching a specified search query - Enum + ports and Services
- (DISCOVERY) - /v2/hosts/{ip}/names -  Returns host names for the specified IP address
- (ENUM)/v2/hosts/{ip} - Returns host information for the specified IP address
Returns info related to services available like: Banners, content etc 

- Censys: Used to get services at hosts. (https://censys.io)
-- DONE /v2/hosts/search Returns previews of hosts matching a specified search query - Enum + ports and Services
-- DONE  /v2/hosts/{ip} Returns host information for the specified IP address
-- DONE /v2/hosts/{ip}/names Returns host names for the specified IP address
--- https://search.censys.io/api#/hosts/searchHosts

#### Shodan (Check Features)
- Shodan: Used to get services at hosts. (https://api.shodan.io)
-- DONE  /dns/domain/{domain} (1 credit by request) + Enum ports
-- DONE /shodan/host/search (Search by domain name) + Enum ports and services

#### VirusTotal (Features ok)
- Docs
- API Docs: https://developers.virustotal.com/reference/overview

```
Public API constraints and restrictions

The Public API is limited to 500 requests per day and a rate of 4 requests per minute.
The Public API must not be used in commercial products or services.
The Public API must not be used in business workflows that do not contribute new files.
You are not allowed to register multiple accounts to overcome the aforementioned limitations.
```
Endpoints
- X (DISCOVERY) historical_ssl_certificates (https://developers.virustotal.com/reference/domain-historical_ssl_certificates)
- X (DISCOVERY) historical_whois - https://developers.virustotal.com/reference/domain-historical_whois
All whois records that have been associated with the domain at some moment in time.
- X (INTEL) referrer_files - https://developers.virustotal.com/reference/domain-referrer_files
The referrer_files relationship returns a list of files containing the given domain on its strings. 
- X (INTEL) resolutions - https://developers.virustotal.com/reference/domain-resolutions
The resolutions relationship returns a list of past and current IP resolutions for a given domain or subdomain. 
- X (INTEL) siblings (https://developers.virustotal.com/reference/siblings)
The siblings relationship returns a list of subdomains at the same level as the given subdomain for a domain, along with their information. 
- DONE (DISCOVERY) subdomains - (https://developers.virustotal.com/reference/subdomains)
The subdomains relationship returns a list of all domain's subdomains. This relationships only returns direct subdomains, it's not recursive (it won't return a subdomain's subdomains).
- HOLD (ENUM)(PREMIUM) urls - https://developers.virustotal.com/reference/domain-urls
The urls relationship returns a list of the domain's URLs. This relationship is only available for Premium API users.
- (ENUM) historical_whois - /ip_addresses/ip_addresses/historical_whois https://developers.virustotal.com/reference/ip-historical_whois
Thehistorical_whois relationship returns a list of whois records that have been associated with the IP address at some moment in time. 
- (ENUM) historical_ssl_certificates - /ip_addresses/{ip_addresses}/historical_ssl_certificates - https://developers.virustotal.com/reference/ip-historical_ssl_certificates
The historical_ssl_certificates relationship returns a list of SSL certificates that have been associated with the IP address at some moment in time.
- (ENUM) historical_whois - /ip_addresses/{ip_addresses}/historical_whois - https://developers.virustotal.com/reference/ip-historical_whois
Thehistorical_whois relationship returns a list of whois records that have been associated with the IP address at some moment in time.
- Map favico and search for hash in vtotal

 
#### CertSpotter (Features ok)
- Docs https://sslmate.com/certspotter/
Certspooter: Used to enumerate hosts from domain and subdomains (https://certspotter.com)
- Crawling

#### DNSBuffer (Features ok)
- Docs:
- (DISVOERY) https://dns.bufferover.run/dns?q=


#### SecurityTrails (Check Features)
- Docs https://docs.securitytrails.com/docs 
- Docs API  https://docs.securitytrails.com/reference/ping
- SecurityTrails: Used to enumerate hosts from domain and subdomains. (https://api.securitytrails.com)

- (INTEL) https://api.securitytrails.com/v1/company/{domain} -  https://docs.securitytrails.com/reference/company-details 
Returns details for a company domain.
Custom subscription required
- (INTEL) https://api.securitytrails.com/v1/company/{domain}/associated-ips - https://docs.securitytrails.com/reference/company-associated-ips 
Returns associated IPs for a company domain. The result is not paginated nor limited. The data is based on whois data with the names matched to the domains.
Custom subscription required

- (ENUM)  https://api.securitytrails.com/v1/domain/{hostname} - https://docs.securitytrails.com/reference/domain-details
Returns the current data about the given hostname. In addition to the current data, you also get the current statistics associated with a particular record. For example, for a records you'll get how many other hostnames have the same IP. 

- OK (DISCOVERY) - https://api.securitytrails.com/v1/domain/{hostname}/subdomains -  https://docs.securitytrails.com/reference/domain-subdomains
Returns child and sibling subdomains for a given hostname. Limited to 2000 results for the Free plan and to 10000 for all paid subscriptions.

- (DISCOVERY/INTEL) - https://api.securitytrails.com/v1/domain/{hostname}/whois - https://docs.securitytrails.com/reference/domain-whois
Returns the current WHOIS data about a given hostname with the stats merged together

- (INTEL) - SEARCH - https://api.securitytrails.com/v1/domains/list - https://docs.securitytrails.com/reference/domain-search 
```
Sample Use Cases
    Search for all hostnames that point to your IP address
    Search for phishing domains containing a certain terms
```
- (INTEL) Associated Domains - https://api.securitytrails.com/v1/domain/{hostname}/associated - 
DOCS https://docs.securitytrails.com/reference/domain-associated-domains
Find all domains that are related to a hostname you input. Limited to 10000 results. 

- (INTEL) HISTORY DNS  - https://api.securitytrails.com/v1/history/{hostname}/dns/{type} 
DOCS https://docs.securitytrails.com/reference/history-dns 
Lists out specific historical information about the given hostname parameter. In addition of fetching the historical data for a particular type, the count statistic is returned as well, which represents the number of that particular resource against current data. (a records will have an ip_count field which will represent the number of records that has the same IP as that particular record) The results are sorted first_seen descending. The number of results is not limited. 

- (INTEL) History WHOIS - https://api.securitytrails.com/v1/history/{hostname}/whois 
Docs https://docs.securitytrails.com/reference/history-whois 
Returns historical WHOIS information about the given domain. The number of results is not limited. 

- (ENUM/INTEL) Ips Neighbors - https://api.securitytrails.com/v1/ips/nearby/{ipaddress} - 
DOCS https://docs.securitytrails.com/reference/ips-neighbors
Returns the neighbors in any given IP level range and essentially allows you to explore closeby IP addresses. It will divide the range into 16 groups. Example: a /28 would be divided into 16 /32 blocks or a /24 would be divided into 16 /28 blocks



#### Spyse (DOWN)
- Spyse Used to get hosts from domain and ports from hosts (https://api.spyse.com/)
- Related Domains and intel 

#### CRTSH 
- Crawling 
- (DISCOVERY) OK https://crt.sh/?q=TARGET_DOMAIN


## Intel
### Proposal: 
- Enum related Domains
- Enum users and e-mails
- Enum leaked passwords 
- Check Exposure on S3 buckets
- Intel from pastebin and related dump/leak platforms

### Sources
- spyse related domains
- awsSearch.py
- prettypastebin.py
- psbdmp.ws: Search cross a indexes pastebin urls into a open database or someshit like that (https://psbdmp.ws)
- GreyHatWarfare: Search for buckets s3 (https://buckets.grayhatwarfare.com/) - s3Search.py
- http://pwndb2am4tzkvold.onion/ (DOWN)
- https://pastebin.com
- https://www.pastemonitor.com/
- https://psbdmp.ws/
- https://scribd.com  # Leak de documentos
- https://overleaf.com # Leak de documentos
- https://dehashed.com


## Enum (Fingerprint)
### Proposal:
- Enum services, ports and vulnerabiliteis
- Enum Web Services, urls and content 
- Shodan monopolizou

### Sources
- Shodan (Enum hosts)
- Censys
- Spyse
- Security Trails
- Way Back Machine - waybackv2.py 

#### Tools for active recon
- masscan

# ToDO
- Internar o health check em todas as funcoes dentro das features ao inves de chamar na core_brain
- Insercao dos dados no db 
- Remodelar base de dados
-- Whois
-- Host
-- AppContent
- Aquatone ,tirar print de webapps
- https://docs.securitytrails.com/reference/domain-associated-domains 
- Redefinir fluxo (discovery, enum etc)
- Reescrever features de discovery
- Integrar com banco de dados
- Reescrever features de enum
- Integrar com banco de dados
- Check healty with database when start
- Read the db credentials from file
- SANITIZAR TODOS OS INPUTS PRO BANCO DE DADOS, alguns valores estãop quebrando
- Abusar de features do shodan.
- Abusar de features do censys rtfm
- Criar uma tabela para os arquivos do bucket da AWS
- Problema no censys refrente à identificar portas ativas no servidor de proxy reverso da aplicação caso esteja em um serviço tipo AWS. 
- Refatorar o código. 
- Analisar estrutura dos dados e armazenamento.
- Verificar doc do Shodan e trabalhar melhor os dados.
- Criar uma pool de keys de API caso uma queime.
- integrar zoomeye para descoberta de hosts e serviços.
- Adotar multithread e alterar o fluxo de execução do programa visando melhorar o desempenho. [ Adotar processos]
- Refatorar -> Reescrever chamadas de API, centralizar em um lugar só e criar métodos pra cada API ao invez de ficar trocando URL. 
- Substituir OS por subprocess.
- Database deploy, verificação de dados se existem no banco de dados antes de pesquisar Dominios, IPS, implementar um timestamp dos dados, a partir de X tempoo o valor do banco expira e precisa ser scaneado novamente. 
- [HOLD] Integrar com https://dnsdumpster.com -> Problemas com token CSRF  403 of insanity motherfckr
- randomizar useragent
- Colocar função global de http status code -> Existem diferenças de status code para algumas API's, não são http like
- Pesquisar no grayhatwarfare por nomes em arquivos.
- REPORT -> Separar hosts com IP e apenas enumerar hosts sem IP
- Resultado do masscan não está sendo inserido no fucking banco de dados porra caralho.[ n lembro se arrumei ] 
- Integrar com Amass(?)
- Github Search [ in progress ]
- Adotar https://ipinfo.io/ 
- Adotar print das páginas ScreenShot https://github.com/maaaaz/webscreenshot
- Configurar daemon para rotinas periodicas. 
- Possibilidade de definir escopo restritivo
- colocar um fucking menu e opções nessa caralha, por exemplo, se quiser só dumpar os dados do banco de um determinado host, ou só recon passivo(redteam profile) ou recon ativo(bugbounty profile) 
- Analise de banners coletados visando identificar se está em Cloud, interno, waf, cdn. 
- Extrair versão de serviços de buscar por vulnerabilidades publicas. 
- Identificar possíveis pontos de autenticação para ataques de password spray 
- Crawler de aplicações web(começar a partir da url raiz e usar as infos do wayback como apoio, armazenar no banco) e identificar o número de parâmetros de cada página para agilizar os testes. 
- Identificar qual a aplicação web, caso for um CMS, disparar um scanner ou não, especifico para o cms identificado.
- Automatizar o reconhecimento dos buckets, verificar se possui READ/Write. 
- Funções de atualização de dados no banco quando um novo scan acontecer para algum objeto que já está mapeado no banco
- pastebin https://pypi.org/project/Pastebin/
- Integracao com splunk (free)
- Censys - Migrate to API v2 
- http://kcon.knownsec.com/2021/#/
- https://www.seebug.org/
- viz.greynoise.io
- zoomeye.org
- fofa.so
- onyphe.io
- app.binaryedge.io
- hunter.io
- ghostproject.fr
- wigle.net
- haveibeenpwned.com 
- url2 = "https://api.hackertarget.com/hostsearch/?q=" dzdz = "http://api.hackertarget.com/nmap/?q="
- buildwith 



#### Report
- Listar dominios no banco
- Listar hosts de um dominio especifico
- Listar hosts e respectivas portas/serviços/banners
- Selecionar informações de um host 
- Listar URLS do pastebin de um dominio especifico
- Listar urls de s3(aws) de um dominio especifico
- Listar aplicações web de um dominio especifico
- Listar informações(banner, urls/paths) de uma aplicação em especifico.
- Listar por hosts de um dominio que possuem determinada porta.



##### WayBackMachine 
- https://github.com/tomnomnom/waybackurls 

### Maybe put in the project
- honeypot checker from shodan
- OTX? Não faz sentido mas seria maneiro ter uma analise de comprometimento do alvo caso existir algum report em bases otx. 

##### Footprint DNS IP / Network
- Virtual host scanner https://github.com/jobertabma/virtual-host-discovery
- Asnlookup https://github.com/yassineaboukir/asnlookup
- SpoofCheck https://github.com/BishopFox/spoofcheck
- Just-metadata https://github.com/FortyNorthSecurity/Just-Metadata

##### Web Recon 
- JSParser https://github.com/nahamsec/JSParser
- Aquatone https://github.com/michenriksen/aquatone

##### AWS S3 Bucket
- https://github.com/zuBux/badbucket
- Teh S3 Bucketeers https://github.com/tomdev/teh_s3_bucketeers
- Lazys3 https://github.com/nahamsec/lazys3
- AWSBucketDump https://github.com/jordanpotti/AWSBucketDump
- s3-Inspector https://github.com/kromtech/s3-inspector
- Zeus https://github.com/DenizParlak/Zeus

```shellscript
#!/bin/bash
TARGET=$1
echo "[-] s3://$TARGET/"
aws --no-sign-request s3 cp data s3://$TARGET/
for S3_PATH in `aws --no-sign-request s3 ls s3://$TARGET`
do 
  if [[ ! $S3_PATH == "PRE" ]]
  then
    if [ $(echo $S3_PATH | grep '/' | wc -l) -eq 1 ];then
      echo "[-] s3://$TARGET/$S3_PATH"
      aws --no-sign-request s3 cp data s3://$TARGET/$S3_PATH
     fi
  fi
done

```

##### OSINT 
- Datasploit https://github.com/DataSploit/datasploit
- pwnedOrNot https://github.com/thewhiteh4t/pwnedOrNot
- pwndb https://github.com/davidtavarez/pwndb/
- LinkedInt https://github.com/vysecurity/LinkedInt
- CrossLinked https://github.com/m8r0wn/CrossLinked

##### Github
- unfurl https://github.com/probot/unfurl
- truffleHog https://github.com/dxa4481/truffleHog
- https://github.com/techgaun/github-dorks
- [DOCS] https://github.com/search



### Usefull:
- Bucket S3 S3-Inspector https://securityonline.info/s3-inspector-check-aws-s3-bucket-permissions/
- refazer o fluxogram
- https://github.com/infosecn1nja/Red-Teaming-Toolkit#reconnaissance
- https://pentester.land/conference-notes/2018/07/25/bug-bounty-talks-2017-automation-for-bug-hunters.html
- https://developer.shodan.io/api
- https://censys.io/api
- https://securitytrails.com/corp/api
- https://github.com/screetsec/sudomy
- https://www.zoomeye.org/doc
- User Database permissions: https://www.digitalocean.com/community/tutorials/how-to-create-a-new-user-and-grant-permissions-in-mysql
- https://dev.mysql.com/doc/refman/5.7/en/mysql-secure-installation.html
- https://www.w3schools.com/sql/sql_foreignkey.asp
- https://github.com/robertdavidgraham/masscan

# BugFix 
- virus total ok bypass UI fucked, changed to api endpoint 
- security trails ok plug and playyy
- certspotter ok  upgrade to v1 
- dnsbuffer.py ok - missing db integration
- spyse.py (In progress) - Missing db integration
-- Discovery OK 
-- Related Domains 
- Shodan
-- Parser quebrado, precisa reestruturar OK 
-- hostnames e target ok
-- database integration
- Censys
- crtsh (prettycertsh.py)  OK 
- dns dumper (anti CSRF issue, no api available, dead), need to bypass the anti csrf and then parse the results using web scrap
- coreaux.py
- db_controler.py
