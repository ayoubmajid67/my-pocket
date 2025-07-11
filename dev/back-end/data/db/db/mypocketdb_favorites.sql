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
-- Table structure for table `favorites`
--

DROP TABLE IF EXISTS `favorites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `favorites` (
  `FavoriId` int NOT NULL AUTO_INCREMENT,
  `DateAjout` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `FK_AdminId` int DEFAULT NULL,
  `FK_AnnonceurId` int DEFAULT NULL,
  `FK_EtudiantId` int DEFAULT NULL,
  `ProduitId` int DEFAULT NULL,
  `LogementId` int DEFAULT NULL,
  `OffreEmploiId` int DEFAULT NULL,
  `Type` varchar(255) NOT NULL,
  PRIMARY KEY (`FavoriId`),
  KEY `fk_Favorites_Admin` (`FK_AdminId`),
  KEY `fk_Favorites_Annonceur` (`FK_AnnonceurId`),
  KEY `fk_Favorites_Etudiant` (`FK_EtudiantId`),
  KEY `fk_Favorites_Produit` (`ProduitId`),
  KEY `fk_Favorites_Logement` (`LogementId`),
  KEY `fk_Favorites_OffreEmploi` (`OffreEmploiId`),
  CONSTRAINT `fk_Favorites_Admin` FOREIGN KEY (`FK_AdminId`) REFERENCES `admin` (`AdminId`) ON DELETE CASCADE,
  CONSTRAINT `fk_Favorites_Annonceur` FOREIGN KEY (`FK_AnnonceurId`) REFERENCES `annonceur` (`AnnonceurId`) ON DELETE CASCADE,
  CONSTRAINT `fk_Favorites_Etudiant` FOREIGN KEY (`FK_EtudiantId`) REFERENCES `etudiant` (`EtudiantId`) ON DELETE CASCADE,
  CONSTRAINT `fk_Favorites_Logement` FOREIGN KEY (`LogementId`) REFERENCES `logement` (`LogementId`) ON DELETE CASCADE,
  CONSTRAINT `fk_Favorites_OffreEmploi` FOREIGN KEY (`OffreEmploiId`) REFERENCES `offreemploi` (`OffreEmploiId`) ON DELETE CASCADE,
  CONSTRAINT `fk_Favorites_Produit` FOREIGN KEY (`ProduitId`) REFERENCES `produit` (`ProduitId`) ON DELETE CASCADE,
  CONSTRAINT `uniqueOffer` UNIQUE (FK_AdminId,FK_AnnonceurId,FK_EtudiantId,ProduitId,LogementId,OffreEmploiId),
  CONSTRAINT `chk_Favorites_TypeMatch` CHECK ((((`Type` = _utf8mb4'Produit') and (`ProduitId` is not null) and (`LogementId` is null) and (`OffreEmploiId` is null)) or ((`Type` = _utf8mb4'Logement') and (`LogementId` is not null) and (`ProduitId` is null) and (`OffreEmploiId` is null)) or ((`Type` = _utf8mb4'OffreEmploi') and (`OffreEmploiId` is not null) and (`ProduitId` is null) and (`LogementId` is null)))),
  CONSTRAINT `chk_Type` CHECK ((`Type` in (_utf8mb4'Produit',_utf8mb4'Logement',_utf8mb4'OffreEmploi')))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `favorites`
--

LOCK TABLES `favorites` WRITE;
/*!40000 ALTER TABLE `favorites` DISABLE KEYS */;
/*!40000 ALTER TABLE `favorites` ENABLE KEYS */;
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
