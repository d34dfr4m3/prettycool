-- MariaDB dump 10.19  Distrib 10.6.7-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: 127.0.0.1    Database: db_data
-- ------------------------------------------------------
-- Server version	10.6.7-MariaDB-3

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `tb_application`
--

DROP TABLE IF EXISTS `tb_application`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_application` (
  `idApp` int(6) NOT NULL AUTO_INCREMENT,
  `service` varchar(256) DEFAULT NULL,
  `idPort` int(6) NOT NULL,
  `applicationName` varchar(256) DEFAULT NULL,
  `url` varchar(1024) NOT NULL,
  `createdAt` datetime NOT NULL,
  PRIMARY KEY (`idApp`),
  KEY `idPort` (`idPort`),
  CONSTRAINT `tb_application_ibfk_1` FOREIGN KEY (`idPort`) REFERENCES `tb_port` (`idPort`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_applicationContent`
--

DROP TABLE IF EXISTS `tb_applicationContent`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_applicationContent` (
  `idApplication` int(6) NOT NULL AUTO_INCREMENT,
  `idApp` int(6) NOT NULL,
  `url` varchar(1024) NOT NULL,
  `page_content` text DEFAULT NULL,
  `status_code` int(3) DEFAULT NULL,
  `sitemap_hash` varchar(256) DEFAULT NULL,
  `fileExtension` varchar(256) DEFAULT NULL,
  `screenshotPath` varchar(2120) DEFAULT NULL,
  `createdAt` datetime NOT NULL,
  PRIMARY KEY (`idApplication`),
  KEY `idApp` (`idApp`),
  CONSTRAINT `tb_applicationContent_ibfk_1` FOREIGN KEY (`idApp`) REFERENCES `tb_application` (`idApp`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_aws`
--

DROP TABLE IF EXISTS `tb_aws`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_aws` (
  `uuidDump` int(6) NOT NULL AUTO_INCREMENT,
  `domainName` varchar(256) NOT NULL,
  `url` varchar(2048) DEFAULT NULL,
  `dumpDate` varchar(12) DEFAULT NULL,
  `createdAt` datetime NOT NULL,
  PRIMARY KEY (`uuidDump`),
  KEY `domainName` (`domainName`),
  CONSTRAINT `tb_aws_ibfk_1` FOREIGN KEY (`domainName`) REFERENCES `tb_domain` (`domainName`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_domain`
--

DROP TABLE IF EXISTS `tb_domain`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_domain` (
  `domainName` varchar(256) NOT NULL,
  `whois` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`whois`)),
  `createdAt` datetime NOT NULL,
  `cd_status` int(2) NOT NULL,
  PRIMARY KEY (`domainName`),
  UNIQUE KEY `domainName` (`domainName`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_host`
--

DROP TABLE IF EXISTS `tb_host`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_host` (
  `ipAddress` varchar(40) NOT NULL,
  `domainName` varchar(256) NOT NULL,
  `hostName` varchar(256) NOT NULL,
  `geoLocation` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`geoLocation`)),
  `ipOwner` varchar(256) DEFAULT NULL,
  `latitude` varchar(256) DEFAULT NULL,
  `longitude` varchar(256) DEFAULT NULL,
  `isp` varchar(256) DEFAULT NULL,
  `os` varchar(256) DEFAULT NULL,
  `org` varchar(256) DEFAULT NULL,
  `asn` varchar(256) DEFAULT NULL,
  `link` varchar(256) DEFAULT NULL,
  `last_update` datetime DEFAULT NULL,
  `country_code` varchar(256) DEFAULT NULL,
  `shodan_last_update` varchar(256) DEFAULT NULL,
  `createdAt` datetime NOT NULL,
  PRIMARY KEY (`hostName`),
  KEY `domainName` (`domainName`),
  CONSTRAINT `tb_host_ibfk_1` FOREIGN KEY (`domainName`) REFERENCES `tb_domain` (`domainName`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_key`
--

DROP TABLE IF EXISTS `tb_key`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_key` (
  `id_key` int(3) NOT NULL AUTO_INCREMENT,
  `key_name` varchar(256) NOT NULL,
  `token` varchar(512) NOT NULL,
  `key_status` int(3) DEFAULT NULL,
  PRIMARY KEY (`id_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_pastebin`
--

DROP TABLE IF EXISTS `tb_pastebin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_pastebin` (
  `uuidDump` int(6) NOT NULL AUTO_INCREMENT,
  `domainName` varchar(256) NOT NULL,
  `url` varchar(2048) DEFAULT NULL,
  `title` varchar(2048) NOT NULL,
  `dumpDate` varchar(256) DEFAULT NULL,
  `createdAt` datetime NOT NULL,
  PRIMARY KEY (`uuidDump`),
  KEY `domainName` (`domainName`),
  CONSTRAINT `tb_pastebin_ibfk_1` FOREIGN KEY (`domainName`) REFERENCES `tb_domain` (`domainName`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_port`
--

DROP TABLE IF EXISTS `tb_port`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_port` (
  `idPort` int(7) NOT NULL AUTO_INCREMENT,
  `ipAddress` varchar(40) NOT NULL,
  `port` int(11) NOT NULL,
  `protocol` varchar(256) DEFAULT NULL,
  `banner` blob DEFAULT NULL,
  `createdAt` datetime NOT NULL,
  `service` varchar(256) DEFAULT NULL,
  `hostName` varchar(256) NOT NULL,
  `last_update` datetime DEFAULT NULL,
  PRIMARY KEY (`idPort`),
  KEY `hostName` (`hostName`),
  CONSTRAINT `tb_port_ibfk_1` FOREIGN KEY (`hostName`) REFERENCES `tb_host` (`hostName`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_relatedDomains`
--

DROP TABLE IF EXISTS `tb_relatedDomains`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_relatedDomains` (
  `mainDomain` varchar(256) NOT NULL,
  `domainName` varchar(256) NOT NULL,
  `whois` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`whois`)),
  `createdAt` datetime NOT NULL,
  PRIMARY KEY (`domainName`),
  KEY `mainDomain` (`mainDomain`),
  CONSTRAINT `tb_relatedDomains_ibfk_1` FOREIGN KEY (`mainDomain`) REFERENCES `tb_domain` (`domainName`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_status`
--

DROP TABLE IF EXISTS `tb_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_status` (
  `cd_status` int(3) NOT NULL AUTO_INCREMENT,
  `status_value` varchar(256) NOT NULL,
  PRIMARY KEY (`cd_status`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_victim`
--

DROP TABLE IF EXISTS `tb_victim`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_victim` (
  `uuidVictim` int(6) NOT NULL AUTO_INCREMENT,
  `domainName` varchar(256) NOT NULL,
  `email` varchar(320) DEFAULT NULL,
  `contact` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`contact`)),
  `createdAt` datetime NOT NULL,
  `socialMedia` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`socialMedia`)),
  PRIMARY KEY (`uuidVictim`),
  KEY `domainName` (`domainName`),
  CONSTRAINT `tb_victim_ibfk_1` FOREIGN KEY (`domainName`) REFERENCES `tb_domain` (`domainName`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-06-14 17:34:07
