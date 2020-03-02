-- MySQL dump 10.13  Distrib 8.0.12, for Win64 (x86_64)
--
-- Host: localhost    Database: digital_office
-- ------------------------------------------------------
-- Server version	8.0.12

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8mb4 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `binnacle`
--

DROP TABLE IF EXISTS `binnacle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `binnacle` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action` varchar(255) DEFAULT NULL,
  `created_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `binnacle`
--

LOCK TABLES `binnacle` WRITE;
/*!40000 ALTER TABLE `binnacle` DISABLE KEYS */;
/*!40000 ALTER TABLE `binnacle` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `meeting`
--

DROP TABLE IF EXISTS `meeting`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `meeting` (
  `idMeeting` int(11) NOT NULL AUTO_INCREMENT,
  `idPerson` int(11) NOT NULL,
  `issue` varchar(50) DEFAULT NULL,
  `date` varchar(50) DEFAULT NULL,
  `path` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`idMeeting`),
  KEY `idPerson` (`idPerson`),
  CONSTRAINT `meeting_ibfk_1` FOREIGN KEY (`idPerson`) REFERENCES `users` (`idperson`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `meeting`
--

LOCK TABLES `meeting` WRITE;
/*!40000 ALTER TABLE `meeting` DISABLE KEYS */;
/*!40000 ALTER TABLE `meeting` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `memo`
--

DROP TABLE IF EXISTS `memo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `memo` (
  `idMemo` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(50) DEFAULT NULL,
  `memo_type` varchar(50) DEFAULT NULL,
  `idPerson` int(11) NOT NULL,
  `content` varchar(2000) DEFAULT NULL,
  PRIMARY KEY (`idMemo`),
  KEY `idPerson` (`idPerson`),
  CONSTRAINT `memo_ibfk_1` FOREIGN KEY (`idPerson`) REFERENCES `users` (`idperson`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `memo`
--

LOCK TABLES `memo` WRITE;
/*!40000 ALTER TABLE `memo` DISABLE KEYS */;
/*!40000 ALTER TABLE `memo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rel_meeting_user`
--

DROP TABLE IF EXISTS `rel_meeting_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `rel_meeting_user` (
  `idRelMeetingUser` int(11) NOT NULL AUTO_INCREMENT,
  `idPerson` int(11) NOT NULL,
  `idMeeting` int(11) NOT NULL,
  PRIMARY KEY (`idRelMeetingUser`),
  KEY `idPerson` (`idPerson`),
  KEY `idMeeting` (`idMeeting`),
  CONSTRAINT `rel_meeting_user_ibfk_1` FOREIGN KEY (`idPerson`) REFERENCES `users` (`idperson`),
  CONSTRAINT `rel_meeting_user_ibfk_2` FOREIGN KEY (`idMeeting`) REFERENCES `meeting` (`idmeeting`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rel_meeting_user`
--

LOCK TABLES `rel_meeting_user` WRITE;
/*!40000 ALTER TABLE `rel_meeting_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `rel_meeting_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rel_memo_user`
--

DROP TABLE IF EXISTS `rel_memo_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `rel_memo_user` (
  `idRelMemoUser` int(11) NOT NULL AUTO_INCREMENT,
  `idPerson` int(11) NOT NULL,
  `idMemo` int(11) NOT NULL,
  `cMessage` varchar(2000) DEFAULT NULL,
  PRIMARY KEY (`idRelMemoUser`),
  KEY `idPerson` (`idPerson`),
  KEY `idMemo` (`idMemo`),
  CONSTRAINT `rel_memo_user_ibfk_1` FOREIGN KEY (`idPerson`) REFERENCES `users` (`idperson`),
  CONSTRAINT `rel_memo_user_ibfk_2` FOREIGN KEY (`idMemo`) REFERENCES `memo` (`idmemo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rel_memo_user`
--

LOCK TABLES `rel_memo_user` WRITE;
/*!40000 ALTER TABLE `rel_memo_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `rel_memo_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `users` (
  `idPerson` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) DEFAULT NULL,
  `email` varchar(40) DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `lastName` varchar(50) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `position` varchar(50) DEFAULT NULL,
  `publicKey` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`idPerson`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'enrike_201408','enrike@hotmail.com','Enrique','Ramos Diaz','pbkdf2:sha256:150000$wqF21T9b$c57214a928acba49cdf5105a7f2016e69d94e11a01ae354cb7342e4b143aa5f6',1,'CEO','-'),(2,'searleser_09','searleser@hotmail.com','Sergio Gabriel','Sanchez Valencia','pbkdf2:sha256:150000$C1LXSz63$2936ad854d2166783bdbef86ac447dc6441bf163e03d8363b7ce606e2da18de6',1,'Senior Developer','-'),(3,'dani_free','daniel@hotmail.com','Daniel Adrian','Gonzalez Nunez','pbkdf2:sha256:150000$xptgIraz$036bb9f33d0e864f8f6d8904b32f8cd94678504366c72237eb296c1847223c98',1,'Financial Director','-'),(4,'rafa_201409','rafael@hotmail.com','Rafael','Hernandez','pbkdf2:sha256:150000$FdOAwfrQ$07bbe17c3a0a2571831519b7522cf1ac32fe2c7a9675c07e511f0b5477c5e70a',1,'Junior Developer','-'),(5,'humberto_Dom','humberto@hotmail.com','Humberto','Dominguez','pbkdf2:sha256:150000$B9cI6aL8$c5a858ea6824774a944fdbb70423ed131261a0a9af9f346d2611e9533ef832a3',1,'Marketing Manager','-'),(6,'Liliana2000','liliana_nic@gmail.com','Liliana','Nicolas Sayago','pbkdf2:sha256:150000$5y97fdOq$e427a542d3383f4f018f234fdd3e155d3dafd9da6f06d06789933c91682459e5',1,'RH','-'),(7,'Cin201409','cinthya@gmail.com','Cinthya','Parra Garcilazo','pbkdf2:sha256:150000$HASMKmFK$86350eda979c0c9155c53588e268ffeb4fe2282be313faa130db325799d02d52',1,'Benefits Administrator','-'),(8,'Joaks201413','joaks@gmail.com','Joaquin','Dominguez Moran','pbkdf2:sha256:150000$jJUQKSt3$d5fe5d56d703389388665e75a544b3cb804bc1a08e177cf5deb68a00cb9b3aa2',0,'Social Media Manager','-'),(9,'memo201414','memo@gmail.com','Guillermo','Naranjo','pbkdf2:sha256:150000$Q4H0Ggpq$f6dd3b44f172d80c587dd04e5d25126c095e5772205e90a9b9b5538bde3e7d9b',0,'Analyst','-'),(10,'barbara201512','barbara@gmail.com','Barbara','Sayago Gonzalez','pbkdf2:sha256:150000$K2AznuZI$7e519015d3c9f2816bbac6b6e221362d805f1dded384db1dececfff03860eacc',0,'Digital Analyst','-'),(11,'victorMorales','victor@gmail.com','Victor','Morales Flores','pbkdf2:sha256:150000$2nqTvES3$d6730317db0d941187937898a69bda5edbbe3c1b0642bddfdb4ab8630574e301',0,'Social Media Manager','-'),(12,'josueDavid2014','deivid@gmail.com','Josue David','Rodriguez','pbkdf2:sha256:150000$Meu1UtoW$a00d4563a454da02a0bc46c2cdfd4fcd0250c209084cf2b9a14b56f07a37cdf4',0,'Personnel Administrator','-'),(13,'leticia2014','lety@gmail.com','Leticia','Canedo','pbkdf2:sha256:150000$QwChWz3y$f3031d065f90535d3aac9a8e827edf201ad6d518b0ddc813446e70431b98c1b5',0,'Accountant','-'),(14,'cesar201517','cesar@gmail.com','Cesar Uriel','Hernandez Castellanos','pbkdf2:sha256:150000$oV7mTan2$a50e5176d93b854f9ea6126832b576108affe3b1b50a4edd854f5abf2ce7bd70',0,'Social Media Manager','-');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-05-22 22:00:09
