-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: localhost    Database: marketguruhp
-- ------------------------------------------------------
-- Server version	8.0.43

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
-- Table structure for table `cars`
--

DROP TABLE IF EXISTS `cars`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cars` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `year` int DEFAULT NULL,
  `price` varchar(20) DEFAULT NULL,
  `priceN` int DEFAULT NULL,
  `km` varchar(50) DEFAULT NULL,
  `fuel` varchar(20) DEFAULT NULL,
  `trans` varchar(20) DEFAULT NULL,
  `owner` varchar(20) DEFAULT NULL,
  `color` varchar(20) DEFAULT NULL,
  `emoji` varchar(20) DEFAULT NULL,
  `verified` tinyint(1) DEFAULT NULL,
  `emi` varchar(20) DEFAULT NULL,
  `city` varchar(50) DEFAULT NULL,
  `description` text,
  `features` text,
  `listed_by` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cars`
--

LOCK TABLES `cars` WRITE;
/*!40000 ALTER TABLE `cars` DISABLE KEYS */;
INSERT INTO `cars` VALUES (1,'Maruti Swift VXi',2021,'5.20',520000,'32,000','Petrol','Manual','1st','#e8eef5','🚗',1,'9,800','Vadodara','Well maintained single owner car. All service records available.','Power Windows, Airbags, ABS, Bluetooth',NULL),(2,'Hyundai i20 Asta',2020,'6.80',680000,'45,000','Petrol','Manual','1st','#eef0f5','🚙',1,'12,800','Vadodara','Top variant with sunroof. No accidents. Genuine seller.','Sunroof, Rear Camera, ABS, Airbags',NULL),(3,'Honda City ZX CVT',2019,'9.50',950000,'58,000','Petrol','Automatic','2nd','#f0eef5','🚘',0,'17,900','Vadodara','Premium sedan in excellent condition. Service at Honda authorized center.','Cruise Control, Leather Seats, Lane Watch, Android Auto',NULL),(4,'Tata Nexon XZ+ Dark',2022,'11.20',1120000,'22,000','Diesel','Manual','1st','#eef5f0','🛻',1,'21,100','Vadodara','Latest model in dark edition. Under warranty till 2027.','Panoramic Sunroof, iRA Connected, Harman Audio, 6 Airbags',NULL),(5,'Kia Seltos HTX+ AT',2021,'14.50',1450000,'35,000','Petrol','Automatic','1st','#f5eef0','🏎️',1,'27,300','Vadodara','Premium SUV with all luxury features. Full service history.','Bose Audio, Ventilated Seats, 10.25\" Screen, Drive Modes',NULL),(6,'Maruti Ertiga VXi CNG',2020,'7.90',790000,'52,000','CNG','Manual','1st','#eff5ee','🚐',0,'14,900','Vadodara','Factory fitted CNG. Economy family car. Reasonable mileage.','7 Seater, Smart Play, Rear AC Vents, CNG Kit',NULL),(7,'Toyota Fortuner 2.8 4x4',2020,'28.50',2850000,'48,000','Diesel','Automatic','1st','#f5f0ee','🚙',1,'53,700','Surat','Beast condition. All options available. Must see.','4x4, Multi Terrain Select, JBL Audio, Power Tailgate',NULL),(8,'Mahindra Thar LX 4x4',2022,'17.80',1780000,'15,000','Diesel','Automatic','1st','#eef2f5','🛞',1,'33,500','Vadodara','Almost new. Diesel automatic with hard top. All accessories.','4x4, Hardtop, Touchscreen, Rock Mode',NULL);
/*!40000 ALTER TABLE `cars` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customers`
--

DROP TABLE IF EXISTS `customers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `mobile` varchar(20) DEFAULT NULL,
  `city` varchar(50) DEFAULT NULL,
  `interests` varchar(255) DEFAULT NULL,
  `purchases` varchar(10) DEFAULT NULL,
  `last` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customers`
--

LOCK TABLES `customers` WRITE;
/*!40000 ALTER TABLE `customers` DISABLE KEYS */;
INSERT INTO `customers` VALUES (1,'Arjun Mehta','+91 98765-43210','Vadodara','Sedan, Budget 5-8L','1','12 Jun 2025'),(2,'Priya Shah','+91 87654-32109','Ahmedabad','SUV, Automatic','0','12 Jun 2025'),(3,'Kiran Patel','+91 76543-21098','Vadodara','MUV, Diesel','2','10 Jun 2025'),(4,'Rahul Gupta','+91 65432-10987','Surat','Hatchback','1','9 Jun 2025'),(5,'Meera Trivedi','+91 54321-09876','Vadodara','SUV, Petrol','0','10 Jun 2025');
/*!40000 ALTER TABLE `customers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `enquiries`
--

DROP TABLE IF EXISTS `enquiries`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `enquiries` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `mobile` varchar(20) DEFAULT NULL,
  `car` varchar(100) DEFAULT NULL,
  `query` text,
  `date` varchar(50) DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `enquiries`
--

LOCK TABLES `enquiries` WRITE;
/*!40000 ALTER TABLE `enquiries` DISABLE KEYS */;
INSERT INTO `enquiries` VALUES (1,'Mohan Lal','98765-XXXXX','Maruti Swift VXi 2021','Is first owner? Service history?','12 Jun 2:30pm','new'),(2,'Sunita Patel','98765-XXXXX','Honda City ZX','What is lowest price possible?','12 Jun 1:15pm','new'),(3,'Vijay Shah','98765-XXXXX','Tata Nexon XZ+','Still available? Can I test drive?','11 Jun 4:00pm','replied'),(4,'Kavita Mehta','98765-XXXXX','Toyota Fortuner','Any warranty left? Exchange possible?','11 Jun 11:30am','replied'),(5,'Dilip Chauhan','98765-XXXXX','Kia Seltos HTX','What accessories are included?','10 Jun 3:45pm','closed');
/*!40000 ALTER TABLE `enquiries` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `followups`
--

DROP TABLE IF EXISTS `followups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `followups` (
  `id` int NOT NULL AUTO_INCREMENT,
  `customer` varchar(100) DEFAULT NULL,
  `car` varchar(100) DEFAULT NULL,
  `due` varchar(50) DEFAULT NULL,
  `type` varchar(50) DEFAULT NULL,
  `notes` text,
  `status` varchar(20) DEFAULT NULL,
  `assigned` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `followups`
--

LOCK TABLES `followups` WRITE;
/*!40000 ALTER TABLE `followups` DISABLE KEYS */;
INSERT INTO `followups` VALUES (1,'Kiran Patel','Toyota Innova','Today 4:00 PM','Phone Call','Discuss price drop','pending','Rahul S.'),(2,'Suresh Joshi','Tata Nexon','Today 6:00 PM','WhatsApp','Send updated photos','pending','Amit J.'),(3,'Meera Trivedi','Hyundai Creta','Tomorrow 10AM','Test Drive','Confirm time','scheduled','Priya P.'),(4,'Dilip Chauhan','Kia Seltos','Yesterday','Phone Call','Follow up on offer','overdue','Rahul S.'),(5,'Mohan Lal','Swift VXi','13 Jun 2PM','Visit','Show car','scheduled','Amit J.');
/*!40000 ALTER TABLE `followups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `leads`
--

DROP TABLE IF EXISTS `leads`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `leads` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `mobile` varchar(20) DEFAULT NULL,
  `car` varchar(100) DEFAULT NULL,
  `budget` varchar(50) DEFAULT NULL,
  `source` varchar(50) DEFAULT NULL,
  `stage` varchar(50) DEFAULT NULL,
  `assigned` varchar(100) DEFAULT NULL,
  `date` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `leads`
--

LOCK TABLES `leads` WRITE;
/*!40000 ALTER TABLE `leads` DISABLE KEYS */;
INSERT INTO `leads` VALUES (1,'Arjun Mehta','98765-43210','Maruti Swift','4-6L','Website','negotiation','Rahul S.','12 Jun'),(2,'Priya Shah','87654-32109','Honda City','8-12L','Walk-in','test-drive','Priya P.','12 Jun'),(3,'Kiran Patel','76543-21098','Toyota Innova','15-20L','Referral','new','Rahul S.','11 Jun'),(4,'Suresh Joshi','65432-10987','Tata Nexon','10-12L','Social','new','Amit J.','11 Jun'),(5,'Meera Trivedi','54321-09876','Hyundai Creta','8-10L','Website','contacted','Priya P.','10 Jun'),(6,'Rahul Gupta','43210-98765','Kia Seltos','12-16L','Phone','won','Rahul S.','9 Jun'),(7,'Anita Roy','32109-87654','Maruti Baleno','5-7L','Website','lost','Amit J.','8 Jun');
/*!40000 ALTER TABLE `leads` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `revenue`
--

DROP TABLE IF EXISTS `revenue`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `revenue` (
  `id` int NOT NULL AUTO_INCREMENT,
  `date` varchar(50) DEFAULT NULL,
  `car` varchar(100) DEFAULT NULL,
  `buyer` varchar(100) DEFAULT NULL,
  `sale` varchar(20) DEFAULT NULL,
  `cost` varchar(20) DEFAULT NULL,
  `profit` varchar(20) DEFAULT NULL,
  `mode` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `revenue`
--

LOCK TABLES `revenue` WRITE;
/*!40000 ALTER TABLE `revenue` DISABLE KEYS */;
INSERT INTO `revenue` VALUES (1,'12 Jun','Maruti Swift VXi 2021','Arjun Mehta','₹5.20L','₹4.10L','₹1.10L','Bank Transfer'),(2,'10 Jun','Kia Seltos HTX','Rahul Gupta','₹14.50L','₹12.80L','₹1.70L','Loan (HDFC)'),(3,'8 Jun','Honda Amaze S','Sunita Patel','₹7.20L','₹6.30L','₹0.90L','Cash'),(4,'6 Jun','Tata Harrier XZ','Vikram Shah','₹17.80L','₹16.00L','₹1.80L','Loan (SBI)'),(5,'4 Jun','Maruti Dzire ZXi','Pooja Mehta','₹8.10L','₹7.20L','₹0.90L','Bank Transfer');
/*!40000 ALTER TABLE `revenue` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `staff`
--

DROP TABLE IF EXISTS `staff`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `staff` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `role` varchar(50) DEFAULT NULL,
  `dept` varchar(50) DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  `last` varchar(50) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `staff`
--

LOCK TABLES `staff` WRITE;
/*!40000 ALTER TABLE `staff` DISABLE KEYS */;
INSERT INTO `staff` VALUES (1,'Rajesh Patel','rajesh@marketguruhp.in','Super Admin','Management','active','Just now','240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9'),(2,'Rahul Sharma','rahul@marketguruhp.in','Sales Manager','Sales','active','10 min ago','240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9'),(3,'Priya Patel','priya@marketguruhp.in','Executive','Sales','active','1 hr ago','240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9'),(4,'Amit Joshi','amit@marketguruhp.in','Executive','Sales','active','2 hr ago','240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9'),(5,'Neha Verma','neha@marketguruhp.in','Finance','Finance','active','Yesterday','240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9'),(6,'Deepak Shah','deepak@marketguruhp.in','Executive','Sales','inactive','3 days ago','240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9');
/*!40000 ALTER TABLE `staff` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `subscriptions`
--

DROP TABLE IF EXISTS `subscriptions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `subscriptions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_mobile` varchar(20) DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  `expiry` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_mobile` (`user_mobile`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `subscriptions`
--

LOCK TABLES `subscriptions` WRITE;
/*!40000 ALTER TABLE `subscriptions` DISABLE KEYS */;
/*!40000 ALTER TABLE `subscriptions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `mobile` varchar(20) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `account_type` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `mobile` (`mobile`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Raj','Shah','raj@example.com','98765-43210','ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f','private'),(2,'Vadodara','Car Hub','dealer@example.com','9876543210','ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f','dealer'),(3,'Test','User','test@example.com','9999999999','ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f','private');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wishlist`
--

DROP TABLE IF EXISTS `wishlist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `wishlist` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_mobile` varchar(20) DEFAULT NULL,
  `car_id` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wishlist`
--

LOCK TABLES `wishlist` WRITE;
/*!40000 ALTER TABLE `wishlist` DISABLE KEYS */;
/*!40000 ALTER TABLE `wishlist` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-06-16 15:29:10
