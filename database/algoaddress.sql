-- MySQL dump 10.13  Distrib 8.0.30, for Linux (x86_64)
--
-- Host: godog.dev    Database: algoaddress
-- ------------------------------------------------------
-- Server version	8.0.28

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `app_optins`
--

DROP TABLE IF EXISTS `app_optins`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `app_optins` (
  `address` varchar(58) DEFAULT NULL,
  `app_id` int DEFAULT NULL,
  `round` int DEFAULT NULL,
  KEY `add_app_id_index` (`address`,`app_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `available`
--

DROP TABLE IF EXISTS `available`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `available` (
  `address` varchar(70) DEFAULT NULL,
  `private_key` varchar(200) DEFAULT NULL,
  `match_part` varchar(25) DEFAULT NULL,
  `match_len` int DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `name_len` int DEFAULT NULL,
  KEY `matchlen` (`match_len`),
  KEY `add-name` (`address`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `contest_guesses`
--

DROP TABLE IF EXISTS `contest_guesses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `contest_guesses` (
  `contest_no` int NOT NULL,
  `address` varchar(58) NOT NULL,
  `confirmed_round` int NOT NULL,
  `guess` int DEFAULT NULL,
  PRIMARY KEY (`contest_no`,`address`,`confirmed_round`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `contest_winners`
--

DROP TABLE IF EXISTS `contest_winners`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `contest_winners` (
  `address` varchar(58) DEFAULT NULL,
  `private_key` varchar(200) DEFAULT NULL,
  `name` varchar(58) DEFAULT NULL,
  `name_len` int DEFAULT NULL,
  `user_requests_matches_id` int DEFAULT NULL,
  `contest_no` int DEFAULT NULL,
  `winning_round` int DEFAULT NULL,
  `winner` varchar(58) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `gdw_available`
--

DROP TABLE IF EXISTS `gdw_available`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gdw_available` (
  `address` varchar(58) DEFAULT NULL,
  `private_key` varchar(200) DEFAULT NULL,
  `match_part` varchar(58) DEFAULT NULL,
  `match_len` int DEFAULT NULL,
  `name` varchar(58) DEFAULT NULL,
  `name_len` int DEFAULT NULL,
  `search_request_id` int NOT NULL,
  `type` varchar(45) DEFAULT NULL,
  `text` varchar(58) DEFAULT NULL,
  `requestor` varchar(58) DEFAULT NULL,
  `on_behalf_of` varchar(58) DEFAULT NULL,
  `priority` int DEFAULT NULL,
  `position` varchar(45) DEFAULT NULL,
  `txn_no` varchar(255) DEFAULT NULL,
  `requested_dt` int DEFAULT NULL,
  KEY `address-indx` (`address`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `loader_log`
--

DROP TABLE IF EXISTS `loader_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `loader_log` (
  `loader_log_id` int NOT NULL AUTO_INCREMENT,
  `recorded_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `record_amt` int DEFAULT NULL,
  PRIMARY KEY (`loader_log_id`)
) ENGINE=InnoDB AUTO_INCREMENT=88719 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `matches`
--

DROP TABLE IF EXISTS `matches`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `matches` (
  `address` varchar(58) DEFAULT NULL,
  `private_key` varchar(200) DEFAULT NULL,
  `match_part` varchar(25) DEFAULT NULL,
  `match_len` int DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `name_len` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `names`
--

DROP TABLE IF EXISTS `names`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `names` (
  `name` varchar(100) DEFAULT NULL,
  KEY `names` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `search_matches`
--

DROP TABLE IF EXISTS `search_matches`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `search_matches` (
  `address` varchar(58) DEFAULT NULL,
  `private_key` varchar(200) DEFAULT NULL,
  `match_part` varchar(58) DEFAULT NULL,
  `match_len` int DEFAULT NULL,
  `name` varchar(58) DEFAULT NULL,
  `name_len` int DEFAULT NULL,
  `search_request_id` int NOT NULL,
  `type` varchar(45) DEFAULT NULL,
  `text` varchar(58) DEFAULT NULL,
  `requestor` varchar(58) DEFAULT NULL,
  `on_behalf_of` varchar(58) DEFAULT NULL,
  `priority` int DEFAULT NULL,
  `position` varchar(45) DEFAULT NULL,
  `txn_no` varchar(255) DEFAULT NULL,
  `requested_dt` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `search_requests`
--

DROP TABLE IF EXISTS `search_requests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `search_requests` (
  `search_request_id` int NOT NULL AUTO_INCREMENT,
  `type` varchar(45) DEFAULT NULL,
  `text` varchar(58) DEFAULT NULL,
  `requestor` varchar(58) DEFAULT NULL,
  `on_behalf_of` varchar(58) DEFAULT NULL,
  `priority` int DEFAULT NULL,
  `position` varchar(45) DEFAULT NULL,
  `txn_no` varchar(255) DEFAULT NULL,
  `requested_dt` int DEFAULT NULL,
  PRIMARY KEY (`search_request_id`)
) ENGINE=InnoDB AUTO_INCREMENT=32798 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `unmatched`
--

DROP TABLE IF EXISTS `unmatched`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `unmatched` (
  `address` varchar(58) DEFAULT NULL,
  `private_key` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user_requests_matches`
--

DROP TABLE IF EXISTS `user_requests_matches`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_requests_matches` (
  `address` varchar(58) DEFAULT NULL,
  `private_key` varchar(200) DEFAULT NULL,
  `match_part` varchar(58) DEFAULT NULL,
  `match_len` int DEFAULT NULL,
  `name` varchar(58) DEFAULT NULL,
  `name_len` int DEFAULT NULL,
  `search_request_id` int NOT NULL,
  `type` varchar(45) DEFAULT NULL,
  `text` varchar(58) DEFAULT NULL,
  `requestor` varchar(58) DEFAULT NULL,
  `on_behalf_of` varchar(58) DEFAULT NULL,
  `priority` int DEFAULT NULL,
  `position` varchar(45) DEFAULT NULL,
  `txn_no` varchar(255) DEFAULT NULL,
  `requested_dt` int DEFAULT NULL,
  `user_requests_matches_id` int NOT NULL AUTO_INCREMENT,
  `inprogress` varchar(1) DEFAULT NULL,
  PRIMARY KEY (`user_requests_matches_id`)
) ENGINE=InnoDB AUTO_INCREMENT=548 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-09-14 15:38:49
