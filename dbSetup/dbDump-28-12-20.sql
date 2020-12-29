-- MySQL dump 10.13  Distrib 5.7.9, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: shotgundb
-- ------------------------------------------------------
-- Server version	5.5.57-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `application`
--

DROP TABLE IF EXISTS `application`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `application` (
  `ride_id` int(11) NOT NULL,
  `username` varchar(16) NOT NULL,
  `message` text NOT NULL,
  `status` enum('pending','accepted','rejected') NOT NULL,
  PRIMARY KEY (`ride_id`,`username`),
  KEY `fk_Ride_has_User_User1_idx` (`username`),
  KEY `fk_Ride_has_User_Ride1_idx` (`ride_id`),
  CONSTRAINT `fk_Ride_has_User_Ride1` FOREIGN KEY (`ride_id`) REFERENCES `ride` (`ride_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_Ride_has_User_User1` FOREIGN KEY (`username`) REFERENCES `user` (`username`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `application`
--

LOCK TABLES `application` WRITE;
/*!40000 ALTER TABLE `application` DISABLE KEYS */;
INSERT INTO `application` VALUES (32,'doumani','I\'ll bring the food','accepted'),(32,'goulaaas','Pls am nice person','pending'),(32,'han.yolo','I am bringing cds','accepted'),(43,'goulaaas','Hohoho','accepted'),(86,'kostino','AKOUW KAI EGW PAOLA','accepted'),(462,'kostino','I <3 SFHMMY','accepted'),(56342,'kostino','gia sou kokla','rejected');
/*!40000 ALTER TABLE `application` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `avg_driver_rating`
--

DROP TABLE IF EXISTS `avg_driver_rating`;
/*!50001 DROP VIEW IF EXISTS `avg_driver_rating`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE VIEW `avg_driver_rating` AS SELECT 
 1 AS `ratee`,
 1 AS `average_driver_rating`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `avg_user_rating`
--

DROP TABLE IF EXISTS `avg_user_rating`;
/*!50001 DROP VIEW IF EXISTS `avg_user_rating`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE VIEW `avg_user_rating` AS SELECT 
 1 AS `ratee`,
 1 AS `average_user_rating`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `creditcard`
--

DROP TABLE IF EXISTS `creditcard`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `creditcard` (
  `number` char(16) NOT NULL,
  `type` enum('VISA','MasterCard','AmEx','DinersClub') NOT NULL,
  `exp_date` date NOT NULL,
  `cvv` char(3) NOT NULL,
  `payment_id` int(11) NOT NULL,
  `username` varchar(16) NOT NULL,
  PRIMARY KEY (`payment_id`,`username`),
  CONSTRAINT `fk_CreditCard_PaymentMethod1` FOREIGN KEY (`payment_id`, `username`) REFERENCES `paymentmethod` (`payment_id`, `username`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `creditcard`
--

LOCK TABLES `creditcard` WRITE;
/*!40000 ALTER TABLE `creditcard` DISABLE KEYS */;
INSERT INTO `creditcard` VALUES ('9812376569302124','AmEx','2025-10-01','856',1,'doumani'),('1234567890123451','AmEx','2022-09-01','164',1,'goulaaas'),('9458128759384720','DinersClub','2024-12-01','123',1,'kostino'),('8283454811245050','MasterCard','2024-12-01','163',1,'TheIronMan'),('5898392488279504','DinersClub','2021-11-01','849',2,'han.yolo'),('8283814814945050','VISA','2025-09-01','152',2,'kostino');
/*!40000 ALTER TABLE `creditcard` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `discount_eligible_users`
--

DROP TABLE IF EXISTS `discount_eligible_users`;
/*!50001 DROP VIEW IF EXISTS `discount_eligible_users`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE VIEW `discount_eligible_users` AS SELECT 
 1 AS `username`,
 1 AS `first_name`,
 1 AS `surname`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `driver`
--

DROP TABLE IF EXISTS `driver`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `driver` (
  `vehicle` varchar(50) NOT NULL,
  `vehicle_image` text NOT NULL,
  `username` varchar(16) NOT NULL,
  PRIMARY KEY (`username`),
  KEY `fk_Driver_User1_idx` (`username`),
  CONSTRAINT `fk_Driver_User1` FOREIGN KEY (`username`) REFERENCES `user` (`username`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `driver`
--

LOCK TABLES `driver` WRITE;
/*!40000 ALTER TABLE `driver` DISABLE KEYS */;
INSERT INTO `driver` VALUES ('Mazda RX-8','as78fdsag.jpg','doumani'),('Tesla Model X','rX832F13.jpg','goulaaas'),('Millennium Falcon','sdf8sf7as.jpg','han.yolo'),('Mazda MX-5','Lf29mBR.jpg','kostino'),('Audi A8','Sd2385H.jpg','TheIronMan');
/*!40000 ALTER TABLE `driver` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `drivercertificationapplication`
--

DROP TABLE IF EXISTS `drivercertificationapplication`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `drivercertificationapplication` (
  `license` text NOT NULL,
  `registration` text NOT NULL,
  `vehicle` varchar(50) NOT NULL,
  `vehicle_image` text NOT NULL,
  `identification_document` text NOT NULL,
  `username` varchar(16) NOT NULL,
  PRIMARY KEY (`username`),
  CONSTRAINT `fk_DriverCertificationApplication_User1` FOREIGN KEY (`username`) REFERENCES `user` (`username`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `drivercertificationapplication`
--

LOCK TABLES `drivercertificationapplication` WRITE;
/*!40000 ALTER TABLE `drivercertificationapplication` DISABLE KEYS */;
INSERT INTO `drivercertificationapplication` VALUES ('lic_980.jpg','reg_1512653.jpg','Mazda RX-8','ffR05HlX.jpg','FLD83HlX.jpg','doumani'),('lic_88912.jpg','reg_159563.jpg','Tesla Model X','7826HASR.jpg','7826HASR.jpg','goulaaas'),('lic_81231.jpg','reg_346632.jpg','Millenium Falcon','A3d4R4F.jpg','AZC4RTF.jpg','han.yolo'),('lic_5342.jpg','reg_125831.jpg','Toyota Yaris 2002','13asAtdsta.jpg','1Ras2561.jpg','kokkinis'),('lic_4481.jpg','reg_151531.jpg','Mazda MX-5','aSd2384.jpg','RSd2FG4.jpg','kostino'),('lic_1231.jpg','reg_156571.jpg','BMW i3','16oGad61.jpg','1RFXad61.jpg','TheIronMan');
/*!40000 ALTER TABLE `drivercertificationapplication` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `driverrating`
--

DROP TABLE IF EXISTS `driverrating`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `driverrating` (
  `rater` varchar(16) NOT NULL,
  `ratee` varchar(16) NOT NULL,
  `comment` text,
  `stars` tinyint(4) NOT NULL,
  PRIMARY KEY (`rater`,`ratee`),
  KEY `fk_User_has_Driver_Driver1_idx` (`ratee`),
  KEY `fk_User_has_Driver_User1_idx` (`rater`),
  CONSTRAINT `fk_User_has_Driver_Driver1` FOREIGN KEY (`ratee`) REFERENCES `driver` (`username`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_User_has_Driver_User1` FOREIGN KEY (`rater`) REFERENCES `user` (`username`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `driverrating`
--

LOCK TABLES `driverrating` WRITE;
/*!40000 ALTER TABLE `driverrating` DISABLE KEYS */;
INSERT INTO `driverrating` VALUES ('doumani','goulaaas','2fast2furious',5),('goulaaas','kostino','Very rude driver!!',2),('han.yolo','kostino','Very nice ride!',4),('kostino','doumani','Cool car',3),('kostino','goulaaas','Good driver!',5);
/*!40000 ALTER TABLE `driverrating` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event`
--

DROP TABLE IF EXISTS `event`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `event` (
  `event_id` int(11) NOT NULL,
  `title` text NOT NULL,
  `type` varchar(50) DEFAULT NULL,
  `status` enum('pending','active','expired') NOT NULL,
  `latitude` varchar(16) NOT NULL,
  `longitude` varchar(16) NOT NULL,
  `location_name` varchar(50) NOT NULL,
  `datetime` datetime NOT NULL,
  `creator` varchar(16) DEFAULT NULL,
  PRIMARY KEY (`event_id`),
  KEY `fk_Event_User1_idx` (`creator`),
  CONSTRAINT `fk_Event_User1` FOREIGN KEY (`creator`) REFERENCES `user` (`username`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event`
--

LOCK TABLES `event` WRITE;
/*!40000 ALTER TABLE `event` DISABLE KEYS */;
INSERT INTO `event` VALUES (1,'PAOK-PSV','football match','expired','40.614474','22.972655','Toumba Stadium','2020-10-21 18:00:00','doumani'),(2,'SFHMMY 12','conference','active','40.628277','22.958299','AUTH','2020-10-21 18:00:00','kostino'),(3,'Tomorrowland','festival','expired','51.088699','4.383017','De Schorre','2020-03-21 13:00:00','han.yolo'),(12,'Flogging Molly @Kastoria','concert','active','40.509880','21.282100','Kastoria','2020-01-21 07:00:00',NULL),(13,'YMCA Party','party','expired','45.901325','69.420134','Kazakhstan steppe','2020-11-09 19:00:00','TheIronMan'),(74,'Dropkick Murphys @Ioannina','concert','pending','38.289560','23.903570','Ioannina','2020-11-13 12:00:00','goulaaas'),(83,'MWC 2021','conference','active','41.385063','2.173404','Barcelona','2021-08-27 22:00:00',NULL);
/*!40000 ALTER TABLE `event` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `future_events`
--

DROP TABLE IF EXISTS `future_events`;
/*!50001 DROP VIEW IF EXISTS `future_events`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE VIEW `future_events` AS SELECT 
 1 AS `event_id`,
 1 AS `title`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `not_applied_as_driver`
--

DROP TABLE IF EXISTS `not_applied_as_driver`;
/*!50001 DROP VIEW IF EXISTS `not_applied_as_driver`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE VIEW `not_applied_as_driver` AS SELECT 
 1 AS `username`,
 1 AS `first_name`,
 1 AS `surname`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `paymentmethod`
--

DROP TABLE IF EXISTS `paymentmethod`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `paymentmethod` (
  `payment_id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `is_primary` tinyint(1) NOT NULL,
  `username` varchar(16) NOT NULL,
  PRIMARY KEY (`payment_id`,`username`),
  KEY `fk_PaymentMethod_User_idx` (`username`),
  CONSTRAINT `fk_PaymentMethod_User` FOREIGN KEY (`username`) REFERENCES `user` (`username`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `paymentmethod`
--

LOCK TABLES `paymentmethod` WRITE;
/*!40000 ALTER TABLE `paymentmethod` DISABLE KEYS */;
INSERT INTO `paymentmethod` VALUES (1,'CashMoney Card',1,'doumani'),(1,'MoneyRain AMEX',1,'goulaaas'),(1,'Jaba\'s PayPal',1,'han.yolo'),(1,'Diners GOLD',0,'kostino'),(1,'Business Card',0,'TheIronMan'),(2,'PP',0,'goulaaas'),(2,'ChewysRetirementPlan',0,'han.yolo'),(2,'Mom\'s VISA',1,'kostino'),(3,'moms PayPal',0,'goulaaas'),(3,'Business PP',0,'kostino'),(4,'Personal PayPal',0,'kostino');
/*!40000 ALTER TABLE `paymentmethod` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `paypalaccount`
--

DROP TABLE IF EXISTS `paypalaccount`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `paypalaccount` (
  `paypal_token` text NOT NULL,
  `payment_id` int(11) NOT NULL,
  `username` varchar(16) NOT NULL,
  PRIMARY KEY (`payment_id`,`username`),
  CONSTRAINT `fk_PayPalAccount_PaymentMethod1` FOREIGN KEY (`payment_id`, `username`) REFERENCES `paymentmethod` (`payment_id`, `username`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `paypalaccount`
--

LOCK TABLES `paypalaccount` WRITE;
/*!40000 ALTER TABLE `paypalaccount` DISABLE KEYS */;
INSERT INTO `paypalaccount` VALUES ('waej1j3289odfs98o24n',1,'han.yolo'),('opgwjpo245g23oomf42',2,'goulaaas'),('opgwjpo1e3oomf42',3,'goulaaas'),('89ohsdfkuh12378oasdd',3,'kostino'),('hf8923hksdhf9823h4kn',4,'kostino');
/*!40000 ALTER TABLE `paypalaccount` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `pending_driver_application`
--

DROP TABLE IF EXISTS `pending_driver_application`;
/*!50001 DROP VIEW IF EXISTS `pending_driver_application`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE VIEW `pending_driver_application` AS SELECT 
 1 AS `username`,
 1 AS `first_name`,
 1 AS `surname`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `pending_events`
--

DROP TABLE IF EXISTS `pending_events`;
/*!50001 DROP VIEW IF EXISTS `pending_events`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE VIEW `pending_events` AS SELECT 
 1 AS `event_id`,
 1 AS `title`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `ride`
--

DROP TABLE IF EXISTS `ride`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ride` (
  `ride_id` int(11) NOT NULL,
  `start_datetime` datetime NOT NULL,
  `return_datetime` datetime DEFAULT NULL,
  `cost` float NOT NULL,
  `description` varchar(512) NOT NULL,
  `seats` int(11) NOT NULL,
  `available_seats` int(11) NOT NULL,
  `longitude` varchar(16) NOT NULL,
  `latitude` varchar(16) NOT NULL,
  `location_name` varchar(50) NOT NULL,
  `event_id` int(11) NOT NULL,
  `driver_username` varchar(16) NOT NULL,
  PRIMARY KEY (`ride_id`),
  KEY `fk_Ride_Event1_idx` (`event_id`),
  KEY `fk_Ride_Driver1_idx` (`driver_username`),
  CONSTRAINT `fk_Ride_Driver1` FOREIGN KEY (`driver_username`) REFERENCES `driver` (`username`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_Ride_Event1` FOREIGN KEY (`event_id`) REFERENCES `event` (`event_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ride`
--

LOCK TABLES `ride` WRITE;
/*!40000 ALTER TABLE `ride` DISABLE KEYS */;
INSERT INTO `ride` VALUES (32,'2020-12-12 13:00:00','2020-12-12 13:00:00',16,'Birthday party RIDE!!!! in kostinos place',3,1,'44.651921','23.23489','kostino\'s place',1,'kostino'),(43,'2021-03-04 11:00:00','2021-03-05 11:30:00',3.5,'We play spot the clouds with a nice company',2,1,'40.519218','53.23489','Sintagma',3,'han.yolo'),(86,'2019-05-06 09:00:00','2019-12-21 19:00:00',12,'Chill vibes',3,2,'25.235234','53.23489','Papazoli',2,'doumani'),(462,'2022-10-12 09:00:00','2022-10-12 09:00:00',4.5,'“Turn Down for What” is stuck on replay',3,2,'32.324123','54.23422','Goula\'s coolcave',74,'han.yolo'),(2125,'2022-12-01 09:00:00','2022-12-01 14:30:00',15,'Paizoume Witcher 3 sto Tesla Control Panel',4,4,'45.235142','69.69693','Mordor',3,'kostino'),(34261,'2023-08-12 06:30:00','2023-08-12 08:30:00',30,'VIP Experience only serious people',5,5,'46.895452','21.26816','aristotelous',83,'kostino'),(56342,'2020-12-23 09:00:00','2020-12-23 09:00:00',12.5,'VAZW PAOLA STO TERMA',3,3,'40.519218','21.26816','Kastoria Plateia',12,'goulaaas');
/*!40000 ALTER TABLE `ride` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `username` varchar(16) NOT NULL,
  `password` text NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `surname` varchar(50) NOT NULL,
  `profile_picture` text,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES ('doumani','15483fb5d748cfded871670db38412177fce200bd524b101ce636075072135ae','Konstantinos','Doumanidis','doumani.jpg'),('goulaaas','dba131483ae3d5c8c8f8d9bf42c0a4834949cd437ee753aacdd4dbd97f8507e8','Andreas','Goulas','goulaaas.jpg'),('han.yolo','0bcd47fbb5ebd93d8561b799881dca82a058fc29c8988a423512fffe565eba0b','Han','Solo','han.yolo.jpg'),('kokkinis','fd22d4b51a78c6ba8ff4c7999d77ccead9501ee56fe9fc994e9cc0611f74a133','Giorgos','Kokkinis','kokkinis.jpg'),('kostino','fe6bb4b3c7b63e470c08407f1426a698d6ab2e1f82aa1de675f2ec9a6afef3e1','Konstantinos','Triaridis','kostino.jpg'),('TheIronMan','d0623060fa9e0e30924a1f8e33515e8278fd288564c96fc2ee87bc462f64d25f','Robert','Downey','TheIronMan.jpg'),('yoda','71a42b2242e81870b40253b0b93db6b9e3efbf9f85968a8a5b7a84543aa408d6','Master','Yoda','yoda.jpg');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `user_num_rides`
--

DROP TABLE IF EXISTS `user_num_rides`;
/*!50001 DROP VIEW IF EXISTS `user_num_rides`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE VIEW `user_num_rides` AS SELECT 
 1 AS `username`,
 1 AS `num_rides`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `userrating`
--

DROP TABLE IF EXISTS `userrating`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `userrating` (
  `rater` varchar(16) NOT NULL,
  `ratee` varchar(16) NOT NULL,
  `comment` text,
  `stars` tinyint(4) NOT NULL,
  PRIMARY KEY (`rater`,`ratee`),
  KEY `fk_User_has_User_User2_idx` (`ratee`),
  KEY `fk_User_has_User_User1_idx` (`rater`),
  CONSTRAINT `fk_User_has_User_User1` FOREIGN KEY (`rater`) REFERENCES `user` (`username`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_User_has_User_User2` FOREIGN KEY (`ratee`) REFERENCES `user` (`username`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `userrating`
--

LOCK TABLES `userrating` WRITE;
/*!40000 ALTER TABLE `userrating` DISABLE KEYS */;
INSERT INTO `userrating` VALUES ('doumani','kostino','Cool dude, we\'ve hung out a lot since then.',5),('goulaaas','doumani','Kewl dude',5),('goulaaas','han.yolo','Sooooo creepy... Flies around in an old spaceship :(',1),('goulaaas','kostino','Very cool dude, funny too',5),('kostino','doumani','Cool dude',5),('kostino','goulaaas','This guy though',4),('kostino','han.yolo','Very aggressive and rude',1);
/*!40000 ALTER TABLE `userrating` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Final view structure for view `avg_driver_rating`
--

/*!50001 DROP VIEW IF EXISTS `avg_driver_rating`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `avg_driver_rating` AS select `driverrating`.`ratee` AS `ratee`,avg(`driverrating`.`stars`) AS `average_driver_rating` from `driverrating` group by `driverrating`.`ratee` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `avg_user_rating`
--

/*!50001 DROP VIEW IF EXISTS `avg_user_rating`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `avg_user_rating` AS select `userrating`.`ratee` AS `ratee`,avg(`userrating`.`stars`) AS `average_user_rating` from `userrating` group by `userrating`.`ratee` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `discount_eligible_users`
--

/*!50001 DROP VIEW IF EXISTS `discount_eligible_users`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `discount_eligible_users` AS select `u`.`username` AS `username`,`u`.`first_name` AS `first_name`,`u`.`surname` AS `surname` from (`user_num_rides` `n` join `user` `u` on((`u`.`username` = `n`.`username`))) where (`n`.`num_rides` < 5) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `future_events`
--

/*!50001 DROP VIEW IF EXISTS `future_events`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `future_events` AS select `event`.`event_id` AS `event_id`,`event`.`title` AS `title` from `event` where ((`event`.`status` = 'active') and (`event`.`datetime` > now())) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `not_applied_as_driver`
--

/*!50001 DROP VIEW IF EXISTS `not_applied_as_driver`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `not_applied_as_driver` AS select `user`.`username` AS `username`,`user`.`first_name` AS `first_name`,`user`.`surname` AS `surname` from `user` where (not(`user`.`username` in (select `drivercertificationapplication`.`username` from `drivercertificationapplication`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `pending_driver_application`
--

/*!50001 DROP VIEW IF EXISTS `pending_driver_application`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `pending_driver_application` AS select `d`.`username` AS `username`,`u`.`first_name` AS `first_name`,`u`.`surname` AS `surname` from (`drivercertificationapplication` `d` join `user` `u` on((`d`.`username` = `u`.`username`))) where (not(`u`.`username` in (select `driver`.`username` from `driver`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `pending_events`
--

/*!50001 DROP VIEW IF EXISTS `pending_events`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `pending_events` AS select `event`.`event_id` AS `event_id`,`event`.`title` AS `title` from `event` where (`event`.`status` = 'pending') */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `user_num_rides`
--

/*!50001 DROP VIEW IF EXISTS `user_num_rides`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `user_num_rides` AS select `application`.`username` AS `username`,count(0) AS `num_rides` from `application` where (`application`.`status` = 'accepted') group by `application`.`username` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-12-29 13:51:12
