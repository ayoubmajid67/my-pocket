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
-- Table structure for table `annonceur`
--

DROP TABLE IF EXISTS `annonceur`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `annonceur` (
  `AnnonceurId` int NOT NULL AUTO_INCREMENT,
  `CarteNationale` varchar(255) NOT NULL,
  `Email` varchar(255) NOT NULL,
  `Nom` varchar(255) NOT NULL,
  `Password` varchar(255) NOT NULL,
  `Prenom` varchar(255) NOT NULL,
  `Profile_Image` varchar(255) DEFAULT NULL,
  `Telephone` varchar(15) NOT NULL,
  `Ville` varchar(255) NOT NULL,
  `Status` varchar(200) DEFAULT NULL,
  `VerificationCode` varchar(6) DEFAULT NULL,
  `VerificationCodeExpiration` datetime DEFAULT NULL,
  PRIMARY KEY (`AnnonceurId`),
  UNIQUE KEY `unq_CarteNationale_Annonceur` (`CarteNationale`),
  UNIQUE KEY `unq_Email_Annonceur` (`Email`),
  KEY `idx_email_annonceur` (`Email`),
  CONSTRAINT `check_status_Annonceur` CHECK ((`Status` in (_utf8mb4'active',_utf8mb4'disabled',_utf8mb4'toVerify',_utf8mb4'toVerifyByAdmin'))),
  CONSTRAINT `chk_EmailFormat_Annonceur` CHECK ((`Email` like _utf8mb4'%@%.%')),
  CONSTRAINT `chk_PasswordComplexity_Annonceur` CHECK (regexp_like(`Password`,_utf8mb4'^(?=.*[0-9])(?=.*[!@#$%^&*])(?=.{8,})')),
  CONSTRAINT `chk_PasswordLength_Annonceur` CHECK ((length(`Password`) >= 8)),
  CONSTRAINT `chk_TelephoneFormat_Annonceur` CHECK (regexp_like(`Telephone`,_utf8mb4'^[0-9]{10,15}$')),
  CONSTRAINT `chk_VerificationCode_Annonceur` CHECK (regexp_like(`VerificationCode`,_utf8mb4'^[0-9]{6}$'))
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `annonceur`
--

LOCK TABLES `annonceur` WRITE;
/*!40000 ALTER TABLE `annonceur` DISABLE KEYS */;
INSERT INTO `annonceur` VALUES (2,'ayoub.annonceur@gmail.com_CarteNationale.pdf','ayoub.annonceur@gmail.com','Ayoub','$2b$12$I0Mb6B1fCS/GgucWLQjAeeFutMS94eC7BCc2TZdAx7WjUgji/aXp6','Annonceur','ayoub.annonceur@gmail.com_Profile_Image.webp','1122334455','Casablanca','active',NULL,NULL),(4,'iliasswakkar.wip@gmail.com_CarteNationale.pdf','iliasswakkar.wip@gmail.com','ilias','$2b$12$sdREo/0VY34bRYS8C2CCy.HsOGbfRKh3/yw3aNYmDAbym1IzkDHpW','annonceur','iliasswakkar.wip@gmail.com_Profile_Image.webp','0771798765','rabat','toVerify',NULL,NULL),(5,'ayoubmajid071wip@gmail.com_CarteNationale.pdf','ayoubmajid071wip@gmail.com','majid','$2b$12$TeIfxR63SsXw4diJJ0rd.uiHVW4F9AsSCKXqjMh93dHCL41KnIHAm','annonceur','ayoubmajid071wip@gmail.com_Profile_Image.webp','0771798765','rabat','toVerify','164114','2025-02-27 22:12:24'),(14,'ayoubmajid071@gmail.com_CarteNationale.pdf','ayoubmajid071@gmail.com','majid','$2b$12$WpJS7uzAL.OeXzMyPG9Ri.CE1U52m7ZRq4q.7IVi30KUNXlKFv2L2','annonceur','ayoubmajid071@gmail.com_Profile_Image.webp','0771798765','rabat','disabled','567435','2025-03-03 21:34:47'),(15,'john.doe@example.com_CarteNationale.pdf','john.doe@example.com','Doe','P@ssword123!','John','john.doe@example.com_Profile_Image.webp','0612345678','Casablanca','active','123456','2025-03-05 12:21:04'),(16,'jane.smith@example.com_CarteNationale.pdf','jane.smith@example.com','Smith','Secur3@Pass!','Jane','jane.smith@example.com_Profile_Image.webp','0623456789','Marrakech','toVerify','654321','2025-03-06 12:21:04'),(17,'ali.ahmed@example.com_CarteNationale.pdf','ali.ahmed@example.com','Ahmed','StrongPass99$','Ali','ali.ahmed@example.com_Profile_Image.webp','0634567890','Rabat','toVerifyByAdmin','987654','2025-03-07 12:21:04'),(18,'sara.mohamed@example.com_CarteNationale.pdf','sara.mohamed@example.com','Mohamed','S@fePassw0rd!','Sara','sara.mohamed@example.com_Profile_Image.webp','0645678901','Fes','disabled',NULL,NULL),(19,'mehdi.ben@example.com_CarteNationale.pdf','mehdi.ben@example.com','Ben','Mehdi#Secure2023','Mehdi','mehdi.ben@example.com_Profile_Image.webp','0656789012','Tangier','active','321654','2025-03-05 12:21:04');
/*!40000 ALTER TABLE `annonceur` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-07 14:24:39
