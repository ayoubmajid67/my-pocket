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
-- Table structure for table `commandeline`
--

DROP TABLE IF EXISTS `commandeline`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `commandeline` (
  `PK_CommandeId` int NOT NULL,
  `PK_ProduitId` int NOT NULL,
  `PrixUnitaire` double NOT NULL,
  `Quantite` int NOT NULL,
  PRIMARY KEY (`PK_CommandeId`,`PK_ProduitId`),
  KEY `fk_CommandeLine_Produit` (`PK_ProduitId`),
  CONSTRAINT `fk_CommandeLine_Commande` FOREIGN KEY (`PK_CommandeId`) REFERENCES `commande` (`CommandeId`) ON DELETE CASCADE,
  CONSTRAINT `fk_CommandeLine_Produit` FOREIGN KEY (`PK_ProduitId`) REFERENCES `produit` (`ProduitId`) ON DELETE CASCADE,
  CONSTRAINT `chk_PrixUnitaire` CHECK ((`PrixUnitaire` >= 0)),
  CONSTRAINT `chk_Quantite` CHECK ((`Quantite` > 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `commandeline`
--

LOCK TABLES `commandeline` WRITE;
/*!40000 ALTER TABLE `commandeline` DISABLE KEYS */;
/*!40000 ALTER TABLE `commandeline` ENABLE KEYS */;
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
