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
-- Dumping data for table `application`
--

LOCK TABLES `application` WRITE;
/*!40000 ALTER TABLE `application` DISABLE KEYS */;
INSERT INTO `application` VALUES (32,'doumani','I\'ll bring the food','accepted'),(32,'goulaaas','Pls am nice person','pending'),(32,'han.yolo','I am bringing cds','accepted'),(43,'goulaaas','Hohoho','accepted'),(86,'kostino','AKOUW KAI EGW PAOLA','accepted'),(462,'kostino','I <3 SFHMMY','accepted'),(56342,'kostino','gia sou kokla','rejected');
/*!40000 ALTER TABLE `application` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `creditcard`
--

LOCK TABLES `creditcard` WRITE;
/*!40000 ALTER TABLE `creditcard` DISABLE KEYS */;
INSERT INTO `creditcard` VALUES ('9812376569302124','AmEx','2025-10-01','856',1,'doumani'),('1234567890123451','AmEx','2022-09-01','164',1,'goulaaas'),('9458128759384720','DinersClub','2024-12-01','123',1,'kostino'),('8283454811245050','MasterCard','2024-12-01','163',1,'TheIronMan'),('5898392488279504','DinersClub','2021-11-01','849',2,'han.yolo'),('8283814814945050','VISA','2025-09-01','152',2,'kostino');
/*!40000 ALTER TABLE `creditcard` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `driver`
--

LOCK TABLES `driver` WRITE;
/*!40000 ALTER TABLE `driver` DISABLE KEYS */;
INSERT INTO `driver` VALUES ('Mazda RX-8','as78fdsag.jpg','doumani'),('Tesla Model X','rX832F13.jpg','goulaaas'),('Millennium Falcon','sdf8sf7as.jpg','han.yolo'),('Mazda MX-5','Lf29mBR.jpg','kostino'),('Audi A8','Sd2385H.jpg','TheIronMan');
/*!40000 ALTER TABLE `driver` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `drivercertificationapplication`
--

LOCK TABLES `drivercertificationapplication` WRITE;
/*!40000 ALTER TABLE `drivercertificationapplication` DISABLE KEYS */;
INSERT INTO `drivercertificationapplication` VALUES ('lic_980.jpg','reg_1512653.jpg','Mazda RX-8','ffR05HlX.jpg','FLD83HlX.jpg','doumani'),('lic_88912.jpg','reg_159563.jpg','Tesla Model X','7826HASR.jpg','7826HASR.jpg','goulaaas'),('lic_81231.jpg','reg_346632.jpg','Millenium Falcon','A3d4R4F.jpg','AZC4RTF.jpg','han.yolo'),('lic_5342.jpg','reg_125831.jpg','Toyota Yaris 2002','13asAtdsta.jpg','1Ras2561.jpg','kokkinis'),('lic_4481.jpg','reg_151531.jpg','Mazda MX-5','aSd2384.jpg','RSd2FG4.jpg','kostino'),('lic_1231.jpg','reg_156571.jpg','BMW i3','16oGad61.jpg','1RFXad61.jpg','TheIronMan');
/*!40000 ALTER TABLE `drivercertificationapplication` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `driverrating`
--

LOCK TABLES `driverrating` WRITE;
/*!40000 ALTER TABLE `driverrating` DISABLE KEYS */;
INSERT INTO `driverrating` VALUES ('doumani','goulaaas','2fast2furious',5),('goulaaas','kostino','Very rude driver!!',2),('han.yolo','kostino','Very nice ride!',4),('kostino','doumani','Cool car',3),('kostino','goulaaas','Good driver!',5);
/*!40000 ALTER TABLE `driverrating` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `event`
--

LOCK TABLES `event` WRITE;
/*!40000 ALTER TABLE `event` DISABLE KEYS */;
INSERT INTO `event` VALUES (1,'PAOK-PSV','football match','expired','40.614474','22.972655','Toumba Stadium','2020-10-21 18:00:00','doumani'),(2,'SFHMMY 12','conference','active','40.628277','22.958299','AUTH','2020-10-21 18:00:00','kostino'),(3,'Tomorrowland','festival','expired','51.088699','4.383017','De Schorre','2020-03-21 13:00:00','han.yolo'),(12,'Flogging Molly @Kastoria','concert','active','40.509880','21.282100','Kastoria','2020-01-21 07:00:00',NULL),(13,'YMCA Party','party','expired','45.901325','69.420134','Kazakhstan steppe','2020-11-09 19:00:00','TheIronMan'),(74,'Dropkick Murphys @Ioannina','concert','pending','38.289560','23.903570','Ioannina','2020-11-13 12:00:00','goulaaas'),(83,'MWC 2021','conference','active','41.385063','2.173404','Barcelona','2021-08-27 22:00:00',NULL);
/*!40000 ALTER TABLE `event` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `paymentmethod`
--

LOCK TABLES `paymentmethod` WRITE;
/*!40000 ALTER TABLE `paymentmethod` DISABLE KEYS */;
INSERT INTO `paymentmethod` VALUES (1,'CashMoney Card',1,'doumani'),(1,'MoneyRain AMEX',1,'goulaaas'),(1,'Jaba\'s PayPal',1,'han.yolo'),(1,'Diners GOLD',0,'kostino'),(1,'Business Card',0,'TheIronMan'),(2,'PP',0,'goulaaas'),(2,'ChewysRetirementPlan',0,'han.yolo'),(2,'Mom\'s VISA',1,'kostino'),(3,'moms PayPal',0,'goulaaas'),(3,'Business PP',0,'kostino'),(4,'Personal PayPal',0,'kostino');
/*!40000 ALTER TABLE `paymentmethod` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `paypalaccount`
--

LOCK TABLES `paypalaccount` WRITE;
/*!40000 ALTER TABLE `paypalaccount` DISABLE KEYS */;
INSERT INTO `paypalaccount` VALUES ('waej1j3289odfs98o24n',1,'han.yolo'),('opgwjpo245g23oomf42',2,'goulaaas'),('opgwjpo1e3oomf42',3,'goulaaas'),('89ohsdfkuh12378oasdd',3,'kostino'),('hf8923hksdhf9823h4kn',4,'kostino');
/*!40000 ALTER TABLE `paypalaccount` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `ride`
--

LOCK TABLES `ride` WRITE;
/*!40000 ALTER TABLE `ride` DISABLE KEYS */;
INSERT INTO `ride` VALUES (32,'2020-12-12 13:00:00','2020-12-12 13:00:00',16,'Birthday party RIDE!!!! in kostinos place',3,1,'44.651921','23.23489','kostino\'s place',1,'kostino'),(43,'2021-03-04 11:00:00','2021-03-05 11:30:00',3.5,'We play spot the clouds with a nice company',2,1,'40.519218','53.23489','Sintagma',3,'han.yolo'),(86,'2019-05-06 09:00:00','2019-12-21 19:00:00',12,'Chill vibes',3,2,'25.235234','53.23489','Papazoli',2,'doumani'),(462,'2022-10-12 09:00:00','2022-10-12 09:00:00',4.5,'“Turn Down for What” is stuck on replay',3,2,'32.324123','54.23422','Goula\'s coolcave',74,'han.yolo'),(2125,'2022-12-01 09:00:00','2022-12-01 14:30:00',15,'Paizoume Witcher 3 sto Tesla Control Panel',4,4,'45.235142','69.69693','Mordor',3,'kostino'),(34261,'2023-08-12 06:30:00','2023-08-12 08:30:00',30,'VIP Experience only serious people',5,5,'46.895452','21.26816','aristotelous',83,'kostino'),(56342,'2020-12-23 09:00:00','2020-12-23 09:00:00',12.5,'VAZW PAOLA STO TERMA',3,3,'40.519218','21.26816','Kastoria Plateia',12,'goulaaas');
/*!40000 ALTER TABLE `ride` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES ('doumani','15483fb5d748cfded871670db38412177fce200bd524b101ce636075072135ae','Konstantinos','Doumanidis','doumani.jpg'),('goulaaas','dba131483ae3d5c8c8f8d9bf42c0a4834949cd437ee753aacdd4dbd97f8507e8','Andreas','Goulas','goulaaas.jpg'),('han.yolo','0bcd47fbb5ebd93d8561b799881dca82a058fc29c8988a423512fffe565eba0b','Han','Solo','han.yolo.jpg'),('kokkinis','fd22d4b51a78c6ba8ff4c7999d77ccead9501ee56fe9fc994e9cc0611f74a133','Giorgos','Kokkinis','kokkinis.jpg'),('kostino','fe6bb4b3c7b63e470c08407f1426a698d6ab2e1f82aa1de675f2ec9a6afef3e1','Konstantinos','Triaridis','kostino.jpg'),('TheIronMan','d0623060fa9e0e30924a1f8e33515e8278fd288564c96fc2ee87bc462f64d25f','Robert','Downey','TheIronMan.jpg'),('yoda','71a42b2242e81870b40253b0b93db6b9e3efbf9f85968a8a5b7a84543aa408d6','Master','Yoda','yoda.jpg');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `userrating`
--

LOCK TABLES `userrating` WRITE;
/*!40000 ALTER TABLE `userrating` DISABLE KEYS */;
INSERT INTO `userrating` VALUES ('doumani','kostino','Cool dude, we\'ve hung out a lot since then.',5),('goulaaas','doumani','Kewl dude',5),('goulaaas','han.yolo','Sooooo creepy... Flies around in an old spaceship :(',1),('goulaaas','kostino','Very cool dude, funny too',5),('kostino','doumani','Cool dude',5),('kostino','goulaaas','This guy though',4),('kostino','han.yolo','Very aggressive and rude',1);
/*!40000 ALTER TABLE `userrating` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-12-28 12:45:41
