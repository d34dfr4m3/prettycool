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
#### Data Sources:
- Shodan: Used to get services at hosts. (https://api.shodan.io)
- Censys: Used to get services at hosts. (https://censys.io)
- Crt.sh: Used to enumerate hosts from domain and subdomains. (https://crt.sh)
- Certspooter: Used to enumerate hosts from domain and subdomains (https://certspotter.com)
- VirusTottal: Used to enumerate hosts from domain and subdomains. (https://www.virustotal.com)
- SecurityTrails: Used to enumerate hosts from domain and subdomains. (https://api.securitytrails.com)
- Spyse Used to get hosts from domain and ports from hosts (https://api.spyse.com/)
- psbdmp.ws: Search cross a indexes pastebin urls into a open database or someshit like that (https://psbdmp.ws)
- dnsbuffer
- GreyHatWarfare: Search for buckets s3 (https://buckets.grayhatwarfare.com/)
- waybackmachine [bugged]

#### Tools for active recon
- masscan

## ToDO
- Check healty with database when start
- Read the db credentials from file
- SHODAN Implementar busca por hosts de dominio("subdominios") no shodan /dns/domain/{domain}  https://api.shodan.io/dns/domain/{domain}?key={YOUR_API_KEY}
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
- Integrar com https://dnsdumpster.com -> Problemas com token CSRF  403 of insanity motherfckr
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
- crtsh  https://pypi.org/project/certificate-search/
- pastebin https://pypi.org/project/Pastebin/


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
