CREATE DATABASE db_data;

CREATE TABLE  `db_data`.`tb_domain`(
  `domainName` VARCHAR(256) NOT NULL UNIQUE,
  `whois` JSON NULL,
  `createdAt` DATETIME NOT NULL,
  `cd_status` INT(2) NOT NULL,
  PRIMARY KEY (`domainName`));

CREATE TABLE `db_data`.`tb_relatedDomains`(
  `mainDomain` VARCHAR(256) NOT NULL,
  `domainName` VARCHAR(256) NOT NULL,
  `whois` JSON NULL,
  `createdAt` DATETIME NOT NULL,
  PRIMARY KEY (`domainName`),
  FOREIGN KEY (mainDomain) REFERENCES tb_domain(domainName) ON DELETE CASCADE
); 

CREATE TABLE `db_data`.`tb_status`(
  `cd_status` INT(3) NOT NULL AUTO_INCREMENT,
  `status_value` VARCHAR(256) NOT NULL,
   PRIMARY KEY (`cd_status`)
);

INSERT INTO `db_data`.`tb_status`(cd_status, status_value) VALUES (001, "NOT STARTED");
INSERT INTO `db_data`.`tb_status`(cd_status, status_value) VALUES (002, "STARTED");
INSERT INTO `db_data`.`tb_status`(cd_status, status_value) VALUES (003, "FINISHED");
INSERT INTO `db_data`.`tb_status`(cd_status, status_value) VALUES (004, "ERROR");
INSERT INTO `db_data`.`tb_status`(cd_status, status_value) VALUES (005, "WAITING");
INSERT INTO `db_data`.`tb_status`(cd_status, status_value) VALUES (006, "BURNED");
INSERT INTO `db_data`.`tb_status`(cd_status, status_value) VALUES (007, "FINE");

CREATE TABLE `db_data`.`tb_key`(
  `id_key` INT (3) NOT NULL  AUTO_INCREMENT,
  `key_name` VARCHAR(256) NOT NULL,
  `token` VARCHAR(512) NOT NULL,
  `key_status` int(3),
   PRIMARY KEY (`id_key`)
);

CREATE TABLE `db_data`.`tb_host` (
  `ipAddress` VARCHAR(40) NOT NULL,
  `domainName` VARCHAR(256) NOT NULL,
  `hostName` Varchar(256) NOT NULL,
  `geoLocation` JSON NULL,
  `ipOwner` VARCHAR(256) NULL,
  `latitude`  VARCHAR(256) NULL,
  `longitude` VARCHAR(256) NULL,
  `isp` VARCHAR(256) NULL,
  `os` VARCHAR(256) NULL,
  `org` VARCHAR(256) NULL,
  `asn` VARCHAR(256) NULL,
  `link` VARCHAR(256) NULL, 
  `last_update` DATETIME NULL,
  `country_code` VARCHAR(256) NULL,
  `shodan_last_update`  VARCHAR(256) NULL,
  `createdAt` DATETIME NOT NULL,
   PRIMARY KEY (`hostName`),
   FOREIGN KEY (domainName) REFERENCES tb_domain(domainName) ON DELETE CASCADE);


CREATE TABLE `db_data`.`tb_port` (
  `idPort` int(7) AUTO_INCREMENT,
  `ipAddress` varchar(40) NOT NULL,
  `port` int(11) NOT NULL,
  `protocol` varchar(256) DEFAULT NULL,
  `banner` blob DEFAULT NULL,
  `createdAt` datetime NOT NULL,
  `service` VARCHAR(256) NULL,
  `hostName` varchar(256) NOT NULL,
  `last_update` DATETIME  NULL,
   PRIMARY KEY (`idPort`),
   FOREIGN KEY (hostName) REFERENCES tb_host(hostName) ON DELETE CASCADE);

CREATE TABLE `db_data`.`tb_application` (
  `idApp` int(6) AUTO_INCREMENT,
  `service`VARCHAR(256) NULL,
  `idPort` int(6) NOT NULL,
  `applicationName` VARCHAR(256) NULL,
  `url` VARCHAR(1024) NOT NULL,
  `createdAt` DATETIME NOT NULL,
  PRIMARY KEY(`idApp`),
  FOREIGN KEY (`idPort`) REFERENCES tb_port(idPort) ON DELETE CASCADE );


CREATE TABLE `db_data`.`tb_applicationContent` (
  `idApplication` int(6) NOT NULL AUTO_INCREMENT,
  `idApp` int(6) NOT NULL,
  `url` VARCHAR(1024) NOT NULL,
  `page_content` TEXT NULL,
  `status_code` INT(3) NULL,
  `sitemap_hash` VARCHAR(256) NULL,
  `fileExtension` VARCHAR(256) NULL,
  `screenshotPath` VARCHAR(2120) NULL,
  `createdAt` DATETIME NOT NULL,
   PRIMARY KEY (idApplication),
   FOREIGN KEY (idApp) REFERENCES tb_application(idApp) ON DELETE CASCADE
);

CREATE TABLE `db_data`.`tb_pastebin` (
  `uuidDump` int(6) AUTO_INCREMENT,
  `domainName` VARCHAR(256) NOT NULL,
  `url` VARCHAR(2048) NULL,
  `title` VARCHAR(2048) NOT NULL,
   `dumpDate` varchar(256) NULL, 
  `createdAt` DATETIME NOT NULL,
   PRIMARY KEY (`uuidDump`),
   FOREIGN KEY (domainName) REFERENCES tb_domain(domainName) ON DELETE CASCADE);
   
CREATE TABLE `db_data`.`tb_aws` (
  `uuidDump` int(6) AUTO_INCREMENT ,
  `domainName` VARCHAR(256) NOT NULL,
  `url` VARCHAR(2048) NULL,
   `dumpDate` varchar(12) NULL, 
  `createdAt` DATETIME NOT NULL,
   PRIMARY KEY (`uuidDump`),
   FOREIGN KEY (domainName) REFERENCES tb_domain(domainName) ON DELETE CASCADE);


CREATE TABLE IF NOT EXISTS `db_data`.`tb_victim` (
  `uuidVictim` int(6) AUTO_INCREMENT,
  `domainName` VARCHAR(256) NOT NULL,
  `email` VARCHAR(320) NULL,
  `contact` JSON NULL,
  `createdAt` DATETIME NOT NULL,
  `socialMedia` JSON NULL,
  PRIMARY KEY (`uuidVictim`),
  FOREIGN KEY (domainName) REFERENCES tb_domain(domainName) ON DELETE CASCADE);

