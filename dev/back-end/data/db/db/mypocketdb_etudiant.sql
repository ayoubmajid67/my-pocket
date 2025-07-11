-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: mypocketdb
-- ------------------------------------------------------
-- Server version	8.0.38

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `etudiant`
--

DROP TABLE IF EXISTS `etudiant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `etudiant` (
  `EtudiantId` int NOT NULL AUTO_INCREMENT,
  `ConterInteret` varchar(255) DEFAULT NULL,
  `Email` varchar(255) NOT NULL,
  `EtablissementScolaire` varchar(255) DEFAULT NULL,
  `Nom` varchar(255) NOT NULL,
  `Password` varchar(255) NOT NULL,
  `Prenom` varchar(255) NOT NULL,
  `Profile_Image` varchar(255) DEFAULT NULL,
  `Telephone` varchar(15) NOT NULL,
  `Ville` varchar(255) NOT NULL,
  `Status` varchar(200) DEFAULT NULL,
  `CarteNationale` varchar(255) NOT NULL,
  `justificationDocument` varchar(255) NOT NULL,
  `VerificationCode` varchar(6) DEFAULT NULL,
  `VerificationCodeExpiration` datetime DEFAULT NULL,
  PRIMARY KEY (`EtudiantId`),
  UNIQUE KEY `unq_Email` (`Email`),
  KEY `idx_email_etudiant` (`Email`),
  CONSTRAINT `check_status_Etudiant` CHECK ((`Status` in (_utf8mb4'active',_utf8mb4'disabled',_utf8mb4'toVerify',_utf8mb4'toVerifyByAdmin'))),
  CONSTRAINT `chk_EmailFormat` CHECK ((`Email` like _utf8mb4'%@%.%')),
  CONSTRAINT `chk_PasswordComplexity_Etudiant` CHECK (regexp_like(`Password`,_utf8mb4'^(?=.*[0-9])(?=.*[!@#$%^&*])(?=.{8,})')),
  CONSTRAINT `chk_PasswordLength` CHECK ((length(`Password`) >= 8)),
  CONSTRAINT `chk_TelephoneFormat` CHECK (regexp_like(`Telephone`,_utf8mb4'^[0-9]{10,15}$')),
  CONSTRAINT `chk_VerificationCode_Etudiant` CHECK (regexp_like(`VerificationCode`,_utf8mb4'^[0-9]{6}$')),
  CONSTRAINT `ConterInteret` CHECK ((`ConterInteret` in (_utf8mb4'productsOffers',_utf8mb4'housingOffers',_utf8mb4'jobOffers')))
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `etudiant`
--

LOCK TABLES `etudiant` WRITE;
/*!40000 ALTER TABLE `etudiant` DISABLE KEYS */;
INSERT INTO `etudiant` VALUES (1,'productsOffers','ayoub.etudiant@gmail.com','University of Casablanca','Ayoub','$2b$12$I0Mb6B1fCS/GgucWLQjAeeFutMS94eC7BCc2TZdAx7WjUgji/aXp6','Etudiant','ayoub.etudiant@gmail.com_Profile_Image.webp','5566778899','Casablanca','toVerifyByAdmin','CN654321','ayoub.etudiant@gmail.com_justificationDocument.pdf',NULL,NULL);
/*!40000 ALTER TABLE `etudiant` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-07 14:24:40
