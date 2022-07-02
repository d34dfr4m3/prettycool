Funcoes Banco de Dados
## Cria objeto de conexao 
def createCon(self):
## Executa query
Processo de manipulacao do db
## classes criadas em coreaux
Class Host
Class Port 
Class Application 
## Missing 
Class Domain
Class Bucket
Class Pastebin

VIRUSTOTAL OK model 

#avoidDuplicata(hostname)
#avoidDuplicata(payload['subdomains'][hosts]+'.'+target)
#    avoidDuplicata(dnsbuffer_host)
#    db_controler.hostAdd(ipAddress,tgt,dnsbuffer_host)




def execQuery(self,query):
## Verifica conexao 
def checkDB(self,query):
## Controle de Chaves e Secrets de API`s
def key_control(self):

# Dominios 
## Adiciona um novo dominio 
def domainAdd(self,domain): 
## Dominios Relacionados
def relatedDomainAdd(self,mainDomain,domainName):

# Hosts 
    host_update['hostName']=hostname

#    host_update['hostName']=hostname

## Insercao de novo host 
def hostAdd(self,domainName,hostName,ipAddress='Null', latitude='Null',longitude='Null',isp='Null',os='Null',asn='Null',link='Null',country_code='Null',shodan_last_update='Null'):
## Update de host 
def hostUpdate(self,update_payload):

# Portas e Servicos
## Add porta
#db_controler.portAdd(target,port,hostname,module,banner,port_service)

def portAdd(self,ipAddress,port,hostName,protocol='Null',banner='Null',service='Null'):
##  Cadastra aplicacao
def appAdd(self,app_payload):
# Banners e Fingerprint 
## Cria Conteudo de aplicativo (Web?)
def appAddContent(self,app_payload):

# Intel 
## Pastebin add paste
def pasteAdd(self,domainName,url,title,dumpDate):
## Buckets S3 amazon 
def s3Add(self,domainName,url):


MariaDB [db_tool]> show tables;
+-----------------------------+
| Tables_in_db_tool           |
+-----------------------------+
| tb_application              |
| tb_applicationPathsAndFiles |
| tb_domain                   |
| tb_dump                     |
| tb_host                     |
| tb_port                     |
| tb_victim                   |
+-----------------------------+



tb_domain: domainName, whois, createdAt
tb_relatedDomains: mainDomain, domainName, whois, createdAt
tb_host: ipAddress, domainName, hostName, geoLocation, ipOwner, createdAt
tb_port: idPort, ipAddress, hostName, port, protocol, banner, createdAt
tb_application: idPort,ApplicationName(Title?), url, createdAt. # For webApplications(?)
tb_applicationPathsAndFiles: mimeType,uuidFile,extension,hreflFile, isPage, screenshotPath, idApplication -> Alimentar com waybackMachine.
tb_pastebin:id_dump, domainName, URL, title, dateDump(Data de publicação), createdAt
tb_aws: id_aws, domainName, url 
tb_victim: uuidVictim,domainName,email,contact,createdAt,socialMedia


CREATE TABLE  `db_data`.`tb_domain`(
  `domainName` VARCHAR(256) NOT NULL UNIQUE,
  `whois` JSON NULL,
  `createdAt` DATETIME NOT NULL,
  PRIMARY KEY (`domainName`));

CREATE TABLE 'db_data'.'tb_relatedDomains'(
  `mainDomain` VARCHAR(256) NOT NULL UNIQUE,
  `domainName` VARCHAR(256) NOT NULL,
  `whois` JSON NULL,
  `createdAt` DATETIME NOT NULL,
  PRIMARY KEY (`domainName`),
  FOREIGN KEY (mainDomain) REFERENCES tb_domain(domainName) ON DELETE CASCADE
); 


## tb_host
MariaDB [db_data]> desc tb_host;
+--------------------+--------------+------+-----+---------+-------+
| Field              | Type         | Null | Key | Default | Extra |
+--------------------+--------------+------+-----+---------+-------+
| ipAddress          | varchar(40)  | NO   |     | NULL    |       |
| domainName         | varchar(256) | NO   | MUL | NULL    |       |
| hostName           | varchar(256) | NO   | PRI | NULL    |       |
| geoLocation        | longtext     | YES  |     | NULL    |       |
| ipOwner            | varchar(256) | YES  |     | NULL    |       |
| createdAt          | datetime     | NO   |     | NULL    |       |
| latitude           | varchar(256) | YES  |     | NULL    |       |
| longitude          | varchar(256) | YES  |     | NULL    |       |
| isp                | varchar(256) | YES  |     | NULL    |       |
| os                 | varchar(256) | YES  |     | NULL    |       |
| org                | varchar(256) | YES  |     | NULL    |       |
| asn                | varchar(256) | YES  |     | NULL    |       |
| link               | varchar(256) | YES  |     | NULL    |       |
| country_code       | varchar(256) | YES  |     | NULL    |       |
| shodan_last_update | varchar(256) | YES  |     | NULL    |       |
+--------------------+--------------+------+-----+---------+-------+


CREATE TABLE `db_data`.`tb_host` (
  `ipAddress` VARCHAR(40) NOT NULL,
  `domainName` VARCHAR(256) NOT NULL,
  `hostName` Varchar(256) NOT NULL,
  `geoLocation` JSON NULL,
  `ipOwner` VARCHAR(256) NULL,
  `createdAt` DATETIME NOT NULL,
  `latitude`  VARCHAR(256) NULL,
  `longitude` VARCHAR(256) NULL,
  `isp` VARCHAR(256) NULL,
  `os` VARCHAR(256) NULL,
  `org` VARCHAR(256) NULL,
  `asn` VARCHAR(256) NULL,
  `link` VARCHAR(256) NULL,
  `country_code` VARCHAR(256) NULL,

   PRIMARY KEY (`hostName`),
   FOREIGN KEY (domainName) REFERENCES tb_domain(domainName) ON DELETE CASCADE);

### TB_PORT
MariaDB [db_data]> desc tb_port;
+-----------+--------------+------+-----+---------+----------------+
| Field     | Type         | Null | Key | Default | Extra          |
+-----------+--------------+------+-----+---------+----------------+
| idPort    | int(7)       | NO   | PRI | NULL    | auto_increment |
| ipAddress | varchar(40)  | NO   |     | NULL    |                |
| port      | int(11)      | NO   |     | NULL    |                |
| protocol  | varchar(256) | YES  |     | NULL    |                |
| banner    | blob         | YES  |     | NULL    |                |
| createdAt | datetime     | NO   |     | NULL    |                |
| hostName  | varchar(256) | NO   | MUL | NULL    |                |
| service   | varchar(256) | YES  |     | NULL    |                |
+-----------+--------------+------+-----+---------+----------------+
8 rows in set (0.002 sec)


tb_port: idPort, ipAddress, hostName, port, protocol, banner, createdAt
CREATE TABLE `tb_port` (
  'idPort' int(7) AUTO INCREMENT,
  `ipAddress` varchar(40) NOT NULL,
  `port` int(11) NOT NULL,
  `protocol` varchar(256) DEFAULT NULL,
  `banner` blob DEFAULT NULL,
  `createdAt` datetime NOT NULL,
  `hostName` varchar(256) NOT NULL,
   PRIMARY KEY `fk_ports_hosts1` (`hostName`),
   FOREIGN KEY (hostName) REFERENCES tb_host(hostName) ON DELETE CASCADE);


tb_application: idPort,ApplicationName(Title?), url, createdAt. # For webApplications(?)

CREATE TABLE IF NOT EXISTS `db_data`.`tb_application` (
  `idPort` VARCHAR(36) AUTO INCREMENT,
  `applicationName` VARCHAR(256) NULL,
  `url` VARCHAR(1024) NOT NULL,
  `createdAt` DATETIME NOT NULL,
  PRIMARY KEY (`url`),
  FOREIGN KEY (`idPort`) REFERENCES tb_port(idPort) ON DELETE CASCADE
);

tb_applicationPathsAndFiles: mimeType,uuidFile,extension,hreflFile, isPage, screenshotPath, idApplication -> Alimentar com waybackMachine.
CREATE TABLE IF NOT EXISTS `db_data`.`tb_applicationPathsAndFiles` (
  'url' VARCHAR(1024) NOT NULL,
  `mimeType` VARCHAR(64) NOT NULL,
  `uuidFile` VARCHAR(36) NULL,
  `extension` VARCHAR(8) NULL,
  `hreflFile` VARCHAR(2048) NOT NULL,
  `isPage` TINYINT NOT NULL,
  `screenshotPath` VARCHAR(2120) NOT NULL,
  `idApplication` VARCHAR(2048) NOT NULL,
   PRIMARY KEY (`url`),
   FOREIGN KEY (`url`) REFERENCES tb_application(url) ON DELETE CASCADE
);


tb_pastebin:id_dump, domainName, URL, title, dateDump(Data de publicação), createdAt
CREATE TABLE IF NOT EXISTS `db_data`.`tb_pastebin` (
  `uuidDump` VARCHAR(36) ,
  `domainName` VARCHAR(256) NOT NULL,
  `url` VARCHAR(2048) NULL,
  `title` VARCHAR(2048) NOT NULL,
   'dumpDate' varchar(12) NULL, 
  `createdAt` DATETIME NOT NULL,
   PRIMARY KEY (`uuidDump`),
   FOREIGN KEY (domainName) REFERENCES tb_domain(domainName) ON DELETE CASCADE);
   
tb_aws: id_aws, domainName, url
CREATE TABLE IF NOT EXISTS `db_data`.`tb_aws` (
  `uuidDump` VARCHAR(36) ,
  `domainName` VARCHAR(256) NOT NULL,
  `url` VARCHAR(2048) NULL,
   'dumpDate' varchar(12) NULL, 
  `createdAt` DATETIME NOT NULL,
   PRIMARY KEY (`uuidDump`),
   FOREIGN KEY (domainName) REFERENCES tb_domain(domainName) ON DELETE CASCADE);

tb_victim: uuidVictim,domainName,email,contact,createdAt,socialMedia
CREATE TABLE IF NOT EXISTS `db_data`.`tb_victim` (
  `uuidVictim` VARCHAR(36) AUTO INCREMENT,
  `domainName` VARCHAR(256) NOT NULL,
  `email` VARCHAR(320) NULL,
  `contact` JSON NULL,
  `createdAt` DATETIME NOT NULL,
  `socialMedia` JSON NULL,
  PRIMARY KEY (`uuidVictim`),
  FOREIGN KEY (domainName) REFERENCES tb_domain(domainName) ON DELETE CASCADE);

