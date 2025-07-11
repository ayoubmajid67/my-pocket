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
-- Table structure for table `produit`
--

DROP TABLE IF EXISTS `produit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `produit` (
  `ProduitId` int NOT NULL AUTO_INCREMENT,
  `Categorie` varchar(255) NOT NULL,
  `Description` text,
  `Disponible` int NOT NULL,
  `FK_AnnonceurId` int NOT NULL,
  `Nom` varchar(255) NOT NULL,
  `Prix` double NOT NULL,
  `Stock` int NOT NULL,
  PRIMARY KEY (`ProduitId`),
  UNIQUE KEY `Nom` (`Nom`),
  KEY `fk_Produit_Annonceur` (`FK_AnnonceurId`),
  CONSTRAINT `fk_Produit_Annonceur` FOREIGN KEY (`FK_AnnonceurId`) REFERENCES `annonceur` (`AnnonceurId`) ON DELETE CASCADE,
  CONSTRAINT `chk_Disponible` CHECK ((`Disponible` in (0,1))),
  CONSTRAINT `chk_Prix` CHECK ((`Prix` >= 0)),
  CONSTRAINT `chk_Stock` CHECK ((`Stock` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `produit`
--

LOCK TABLES `produit` WRITE;
/*!40000 ALTER TABLE `produit` DISABLE KEYS */;
INSERT INTO `produit` VALUES (11,'Electronics','Smartphone with 128GB storage',1,2,'iPhone 13',999.99,50),(12,'Electronics','Gaming Laptop with RTX 4060',1,4,'Asus ROG Strix',1499.99,30),(13,'Home Appliances','Automatic Coffee Machine',1,5,'DeLonghi Magnifica',499.99,20),(14,'Fashion','Men’s Leather Jacket',1,4,'Premium Leather Jacket',199.99,15),(15,'Books','Best-selling Sci-Fi Novel',1,16,'Dune by Frank Herbert',29.99,100);
/*!40000 ALTER TABLE `produit` ENABLE KEYS */;
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
