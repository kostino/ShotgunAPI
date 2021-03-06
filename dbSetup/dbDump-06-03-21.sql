-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               10.5.8-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win64
-- HeidiSQL Version:             11.0.0.5919
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Dumping database structure for ShotgunDB
DROP DATABASE IF EXISTS `ShotgunDB`;
CREATE DATABASE IF NOT EXISTS `shotgundb` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `ShotgunDB`;

-- Dumping structure for table ShotgunDB.application
DROP TABLE IF EXISTS `application`;
CREATE TABLE IF NOT EXISTS `application` (
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

-- Dumping data for table ShotgunDB.application: ~16 rows (approximately)
/*!40000 ALTER TABLE `application` DISABLE KEYS */;
INSERT INTO `application` (`ride_id`, `username`, `message`, `status`) VALUES
	(32, 'doumani', 'I\'ll bring the food', 'accepted'),
	(32, 'goulaaas', 'Pls am nice person', 'pending'),
	(32, 'han.yolo', 'I am bringing cds', 'accepted'),
	(43, 'goulaaas', 'Hohoho', 'accepted'),
	(86, 'kostino', 'AKOUW KAI EGW PAOLA', 'accepted'),
	(462, 'kostino', 'I <3 SFHMMY', 'accepted'),
	(34261, 'han.yolo', '', 'accepted'),
	(56342, 'kostino', 'gia sou kokla', 'rejected'),
	(56343, 'doumani', 'Hey there, id like to join this ride!', 'pending'),
	(56343, 'goulaaas', 'ompaaa', 'accepted'),
	(56343, 'kokkinis', 'Hey there... can I come?', 'pending'),
	(56343, 'kostino', 'Please Accept Me Senpai UwU AyAyA :3', 'pending'),
	(56345, 'han.yolo', 'pls accept', 'pending'),
	(56345, 'kokkinis', 'ela rostinho', 'accepted'),
	(56346, 'goulaaas', '', 'accepted'),
	(56346, 'TheIronMan', '', 'accepted');
/*!40000 ALTER TABLE `application` ENABLE KEYS */;

-- Dumping structure for view ShotgunDB.avg_driver_rating
DROP VIEW IF EXISTS `avg_driver_rating`;
-- Creating temporary table to overcome VIEW dependency errors
CREATE TABLE `avg_driver_rating` (
	`ratee` VARCHAR(16) NOT NULL COLLATE 'utf8_general_ci',
	`average_driver_rating` DECIMAL(7,4) NULL
) ENGINE=MyISAM;

-- Dumping structure for view ShotgunDB.avg_user_rating
DROP VIEW IF EXISTS `avg_user_rating`;
-- Creating temporary table to overcome VIEW dependency errors
CREATE TABLE `avg_user_rating` (
	`ratee` VARCHAR(16) NOT NULL COLLATE 'utf8_general_ci',
	`average_user_rating` DECIMAL(7,4) NULL
) ENGINE=MyISAM;

-- Dumping structure for table ShotgunDB.creditcard
DROP TABLE IF EXISTS `creditcard`;
CREATE TABLE IF NOT EXISTS `creditcard` (
  `number` char(16) NOT NULL,
  `type` enum('VISA','MasterCard','AmEx','DinersClub') NOT NULL,
  `exp_date` date NOT NULL,
  `cvv` char(3) NOT NULL,
  `payment_id` int(11) NOT NULL,
  `username` varchar(16) NOT NULL,
  PRIMARY KEY (`payment_id`,`username`),
  CONSTRAINT `fk_CreditCard_PaymentMethod1` FOREIGN KEY (`payment_id`, `username`) REFERENCES `paymentmethod` (`payment_id`, `username`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table ShotgunDB.creditcard: ~6 rows (approximately)
/*!40000 ALTER TABLE `creditcard` DISABLE KEYS */;
INSERT INTO `creditcard` (`number`, `type`, `exp_date`, `cvv`, `payment_id`, `username`) VALUES
	('9812376569302124', 'AmEx', '2025-10-01', '856', 1, 'doumani'),
	('1234567890123451', 'AmEx', '2022-09-01', '164', 1, 'goulaaas'),
	('9458128759384720', 'DinersClub', '2024-12-01', '123', 1, 'kostino'),
	('8283454811245050', 'MasterCard', '2024-12-01', '163', 1, 'TheIronMan'),
	('5898392488279504', 'DinersClub', '2021-11-01', '849', 2, 'han.yolo'),
	('8283814814945050', 'VISA', '2025-09-01', '152', 2, 'kostino');
/*!40000 ALTER TABLE `creditcard` ENABLE KEYS */;

-- Dumping structure for view ShotgunDB.discount_eligible_users
DROP VIEW IF EXISTS `discount_eligible_users`;
-- Creating temporary table to overcome VIEW dependency errors
CREATE TABLE `discount_eligible_users` (
	`username` VARCHAR(16) NOT NULL COLLATE 'utf8_general_ci',
	`first_name` VARCHAR(50) NOT NULL COLLATE 'utf8_general_ci',
	`surname` VARCHAR(50) NOT NULL COLLATE 'utf8_general_ci'
) ENGINE=MyISAM;

-- Dumping structure for table ShotgunDB.driver
DROP TABLE IF EXISTS `driver`;
CREATE TABLE IF NOT EXISTS `driver` (
  `vehicle` varchar(50) NOT NULL,
  `vehicle_image` text NOT NULL,
  `username` varchar(16) NOT NULL,
  PRIMARY KEY (`username`),
  KEY `fk_Driver_User1_idx` (`username`),
  CONSTRAINT `fk_Driver_User1` FOREIGN KEY (`username`) REFERENCES `user` (`username`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table ShotgunDB.driver: ~5 rows (approximately)
/*!40000 ALTER TABLE `driver` DISABLE KEYS */;
INSERT INTO `driver` (`vehicle`, `vehicle_image`, `username`) VALUES
	('Mazda RX-8', 'doumani.jpg', 'doumani'),
	('Tesla Model X', 'goulaaas.jpg', 'goulaaas'),
	('Millennium Falcon', 'han.yolo.jpg', 'han.yolo'),
	('Mazda MX-5', 'kostino.jpg', 'kostino'),
	('Audi A8', 'TheIronMan.jpg', 'TheIronMan');
/*!40000 ALTER TABLE `driver` ENABLE KEYS */;

-- Dumping structure for table ShotgunDB.drivercertificationapplication
DROP TABLE IF EXISTS `drivercertificationapplication`;
CREATE TABLE IF NOT EXISTS `drivercertificationapplication` (
  `license` text NOT NULL,
  `registration` text NOT NULL,
  `vehicle` varchar(50) NOT NULL,
  `vehicle_image` text NOT NULL,
  `identification_document` text NOT NULL,
  `username` varchar(16) NOT NULL,
  PRIMARY KEY (`username`),
  CONSTRAINT `fk_DriverCertificationApplication_User1` FOREIGN KEY (`username`) REFERENCES `user` (`username`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table ShotgunDB.drivercertificationapplication: ~6 rows (approximately)
/*!40000 ALTER TABLE `drivercertificationapplication` DISABLE KEYS */;
INSERT INTO `drivercertificationapplication` (`license`, `registration`, `vehicle`, `vehicle_image`, `identification_document`, `username`) VALUES
	('doumani/license.jpg', 'doumani/registration.jpg', 'Mazda RX-8', 'doumani/vehicle.jpg', 'doumani/id.jpg', 'doumani'),
	('goulaaas/license.jpg', 'goulaaas/registration.jpg', 'Tesla Model X', 'goulaaas/vehicle.jpg', 'goulaaas/id.jpg', 'goulaaas'),
	('han.yolo/license.jpg', 'han.yolo/registration.jpg', 'Millenium Falcon', 'han.yolo/vehicle.jpg', 'han.yolo/id.jpg', 'han.yolo'),
	('kokkinis/license.jpg', 'kokkinis/registration.jpg', 'Toyota Yaris 2002', 'kokkinis/vehicle.jpg', 'kokkinis/id.jpg', 'kokkinis'),
	('kostino/license.jpg', 'kostino/registration.jpg', 'Mazda MX-5', 'kostino/vehicle.jpg', 'kostino/id.jpg', 'kostino'),
	('TheIronMan/license.jpg', 'TheIronMan/registration.jpg', 'BMW i3', 'TheIronMan/vehicle.jpg', 'TheIronMan/id.jpg', 'TheIronMan');
/*!40000 ALTER TABLE `drivercertificationapplication` ENABLE KEYS */;

-- Dumping structure for table ShotgunDB.driverrating
DROP TABLE IF EXISTS `driverrating`;
CREATE TABLE IF NOT EXISTS `driverrating` (
  `rater` varchar(16) NOT NULL,
  `ratee` varchar(16) NOT NULL,
  `comment` text DEFAULT NULL,
  `stars` tinyint(4) NOT NULL,
  PRIMARY KEY (`rater`,`ratee`),
  KEY `fk_User_has_Driver_Driver1_idx` (`ratee`),
  KEY `fk_User_has_Driver_User1_idx` (`rater`),
  CONSTRAINT `fk_User_has_Driver_Driver1` FOREIGN KEY (`ratee`) REFERENCES `driver` (`username`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_User_has_Driver_User1` FOREIGN KEY (`rater`) REFERENCES `user` (`username`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table ShotgunDB.driverrating: ~5 rows (approximately)
/*!40000 ALTER TABLE `driverrating` DISABLE KEYS */;
INSERT INTO `driverrating` (`rater`, `ratee`, `comment`, `stars`) VALUES
	('doumani', 'goulaaas', '2fast2furious', 5),
	('goulaaas', 'kostino', 'Very rude driver!!', 2),
	('han.yolo', 'kostino', 'Very nice ride!', 4),
	('kostino', 'doumani', 'Cool car', 3),
	('kostino', 'goulaaas', 'Good driver!', 5);
/*!40000 ALTER TABLE `driverrating` ENABLE KEYS */;

-- Dumping structure for table ShotgunDB.event
DROP TABLE IF EXISTS `event`;
CREATE TABLE IF NOT EXISTS `event` (
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

-- Dumping data for table ShotgunDB.event: ~10 rows (approximately)
/*!40000 ALTER TABLE `event` DISABLE KEYS */;
INSERT INTO `event` (`event_id`, `title`, `type`, `status`, `latitude`, `longitude`, `location_name`, `datetime`, `creator`) VALUES
	(1, 'PAOK-PSV', 'Sports', 'expired', '40.614474', '22.972655', 'Toumba Stadium', '2020-10-21 18:00:00', 'doumani'),
	(2, 'SFHMMY 12', 'Conference', 'active', '40.628277', '22.958299', 'AUTH', '2020-10-21 18:00:00', 'kostino'),
	(3, 'Tomorrowland', 'Festival', 'expired', '51.088699', '4.383017', 'De Schorre', '2020-03-21 13:00:00', 'han.yolo'),
	(12, 'Flogging Molly @Kastoria', 'Concert', 'active', '40.509880', '21.282100', 'Kastoria', '2020-01-21 07:00:00', NULL),
	(13, 'YMCA Party', 'Party', 'expired', '45.901325', '69.420134', 'Kazakhstan steppe', '2020-11-09 19:00:00', 'TheIronMan'),
	(74, 'Dropkick Murphys @Ioannina', 'Concert', 'pending', '38.289560', '23.903570', 'Ioannina', '2020-11-13 12:00:00', 'goulaaas'),
	(83, 'MWC 2021', 'Conference', 'active', '41.385063', '2.173404', 'Barcelona', '2021-08-27 22:00:00', NULL),
	(84, 'DataBases Project presentation', 'Education', 'active', '40.627669', '22.95989', 'AUTH', '2021-01-19 12:00:00', 'han.yolo'),
	(85, 'Summer 2021 pls no corona', 'Dance', 'pending', '40.6234131', '22.9482666', 'Thessaloniki', '2021-07-12 12:00:00', 'han.yolo'),
	(86, 'Birthday Party', 'Networking', 'active', '40.588117', '23.03139', 'spiti kostino', '2021-12-12 12:12:00', 'kostino');
/*!40000 ALTER TABLE `event` ENABLE KEYS */;

-- Dumping structure for view ShotgunDB.future_events
DROP VIEW IF EXISTS `future_events`;
-- Creating temporary table to overcome VIEW dependency errors
CREATE TABLE `future_events` (
	`event_id` INT(11) NOT NULL,
	`title` TEXT NOT NULL COLLATE 'utf8_general_ci'
) ENGINE=MyISAM;

-- Dumping structure for view ShotgunDB.not_applied_as_driver
DROP VIEW IF EXISTS `not_applied_as_driver`;
-- Creating temporary table to overcome VIEW dependency errors
CREATE TABLE `not_applied_as_driver` (
	`username` VARCHAR(16) NOT NULL COLLATE 'utf8_general_ci',
	`first_name` VARCHAR(50) NOT NULL COLLATE 'utf8_general_ci',
	`surname` VARCHAR(50) NOT NULL COLLATE 'utf8_general_ci'
) ENGINE=MyISAM;

-- Dumping structure for table ShotgunDB.paymentmethod
DROP TABLE IF EXISTS `paymentmethod`;
CREATE TABLE IF NOT EXISTS `paymentmethod` (
  `payment_id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `is_primary` tinyint(1) NOT NULL,
  `username` varchar(16) NOT NULL,
  PRIMARY KEY (`payment_id`,`username`),
  KEY `fk_PaymentMethod_User_idx` (`username`),
  CONSTRAINT `fk_PaymentMethod_User` FOREIGN KEY (`username`) REFERENCES `user` (`username`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table ShotgunDB.paymentmethod: ~11 rows (approximately)
/*!40000 ALTER TABLE `paymentmethod` DISABLE KEYS */;
INSERT INTO `paymentmethod` (`payment_id`, `name`, `is_primary`, `username`) VALUES
	(1, 'CashMoney Card', 1, 'doumani'),
	(1, 'MoneyRain AMEX', 1, 'goulaaas'),
	(1, 'Jaba\'s PayPal', 1, 'han.yolo'),
	(1, 'Diners GOLD', 0, 'kostino'),
	(1, 'Business Card', 0, 'TheIronMan'),
	(2, 'PP', 0, 'goulaaas'),
	(2, 'ChewysRetirementPlan', 0, 'han.yolo'),
	(2, 'Mom\'s VISA', 1, 'kostino'),
	(3, 'moms PayPal', 0, 'goulaaas'),
	(3, 'Business PP', 0, 'kostino'),
	(4, 'Personal PayPal', 0, 'kostino');
/*!40000 ALTER TABLE `paymentmethod` ENABLE KEYS */;

-- Dumping structure for table ShotgunDB.paypalaccount
DROP TABLE IF EXISTS `paypalaccount`;
CREATE TABLE IF NOT EXISTS `paypalaccount` (
  `paypal_token` text NOT NULL,
  `payment_id` int(11) NOT NULL,
  `username` varchar(16) NOT NULL,
  PRIMARY KEY (`payment_id`,`username`),
  CONSTRAINT `fk_PayPalAccount_PaymentMethod1` FOREIGN KEY (`payment_id`, `username`) REFERENCES `paymentmethod` (`payment_id`, `username`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table ShotgunDB.paypalaccount: ~5 rows (approximately)
/*!40000 ALTER TABLE `paypalaccount` DISABLE KEYS */;
INSERT INTO `paypalaccount` (`paypal_token`, `payment_id`, `username`) VALUES
	('waej1j3289odfs98o24n', 1, 'han.yolo'),
	('opgwjpo245g23oomf42', 2, 'goulaaas'),
	('opgwjpo1e3oomf42', 3, 'goulaaas'),
	('89ohsdfkuh12378oasdd', 3, 'kostino'),
	('hf8923hksdhf9823h4kn', 4, 'kostino');
/*!40000 ALTER TABLE `paypalaccount` ENABLE KEYS */;

-- Dumping structure for view ShotgunDB.pending_driver_application
DROP VIEW IF EXISTS `pending_driver_application`;
-- Creating temporary table to overcome VIEW dependency errors
CREATE TABLE `pending_driver_application` (
	`username` VARCHAR(16) NOT NULL COLLATE 'utf8_general_ci',
	`first_name` VARCHAR(50) NOT NULL COLLATE 'utf8_general_ci',
	`surname` VARCHAR(50) NOT NULL COLLATE 'utf8_general_ci'
) ENGINE=MyISAM;

-- Dumping structure for view ShotgunDB.pending_events
DROP VIEW IF EXISTS `pending_events`;
-- Creating temporary table to overcome VIEW dependency errors
CREATE TABLE `pending_events` (
	`event_id` INT(11) NOT NULL,
	`title` TEXT NOT NULL COLLATE 'utf8_general_ci'
) ENGINE=MyISAM;

-- Dumping structure for table ShotgunDB.ride
DROP TABLE IF EXISTS `ride`;
CREATE TABLE IF NOT EXISTS `ride` (
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

-- Dumping data for table ShotgunDB.ride: ~11 rows (approximately)
/*!40000 ALTER TABLE `ride` DISABLE KEYS */;
INSERT INTO `ride` (`ride_id`, `start_datetime`, `return_datetime`, `cost`, `description`, `seats`, `available_seats`, `longitude`, `latitude`, `location_name`, `event_id`, `driver_username`) VALUES
	(32, '2020-12-12 13:00:00', '2020-12-12 13:00:00', 16, 'Birthday party RIDE!!!! in kostinos place', 3, 1, '44.651921', '23.23489', 'kostino\'s place', 1, 'kostino'),
	(43, '2021-03-04 11:00:00', '2021-03-05 11:30:00', 3.5, 'We play spot the clouds with a nice company', 2, 1, '40.519218', '53.23489', 'Sintagma', 3, 'han.yolo'),
	(86, '2019-05-06 09:00:00', '2019-12-21 19:00:00', 12, 'Chill vibes', 3, 2, '25.235234', '53.23489', 'Papazoli', 2, 'doumani'),
	(462, '2022-10-12 09:00:00', '2022-10-12 09:00:00', 4.5, '“Turn Down for What” is stuck on replay', 3, 2, '32.324123', '54.23422', 'Goula\'s coolcave', 74, 'han.yolo'),
	(2125, '2022-12-01 09:00:00', '2022-12-01 14:30:00', 15, 'Paizoume Witcher 3 sto Tesla Control Panel', 4, 4, '45.235142', '69.69693', 'Mordor', 3, 'kostino'),
	(34261, '2023-08-12 06:30:00', '2023-08-12 08:30:00', 30, 'VIP Experience only serious people', 5, 4, '46.895452', '21.26816', 'aristotelous', 83, 'kostino'),
	(56342, '2020-12-23 09:00:00', '2020-12-23 09:00:00', 12.5, 'VAZW PAOLA STO TERMA', 3, 3, '40.519218', '21.26816', 'Kastoria Plateia', 12, 'goulaaas'),
	(56343, '2021-01-19 10:00:00', NULL, 5, 'come see my fantastic project with me!', 3, 2, '40.0', '40.0', 'wherever han solo lives', 84, 'han.yolo'),
	(56344, '2021-08-26 22:00:00', NULL, 5, 'WOOOHOOOO', 2, 2, '40.64086', '22.94444', 'goulospito', 83, 'goulaaas'),
	(56345, '2021-12-12 10:00:00', NULL, 15, 'elate kosme', 2, 1, '40.6234131', '22.9482666', 'aristotelous', 86, 'kostino'),
	(56346, '2021-12-12 11:00:00', NULL, 2, 'come with me!', 7, 5, '40.62170', '22.95710', 'spiti kwsta', 86, 'doumani');
/*!40000 ALTER TABLE `ride` ENABLE KEYS */;

-- Dumping structure for table ShotgunDB.user
DROP TABLE IF EXISTS `user`;
CREATE TABLE IF NOT EXISTS `user` (
  `username` varchar(16) NOT NULL,
  `password` text NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `surname` varchar(50) NOT NULL,
  `profile_picture` text DEFAULT NULL,
  `email` varchar(255) NOT NULL,
  PRIMARY KEY (`username`),
  UNIQUE KEY `email_UNIQUE` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table ShotgunDB.user: ~8 rows (approximately)
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` (`username`, `password`, `first_name`, `surname`, `profile_picture`, `email`) VALUES
	('doumani', 'pbkdf2:sha256:150000$pHL5losn$52e23562e933f9ff0e6bc82dc6d52c98774629d09720cde43e2985562dc853c5', 'Konstantinos', 'Doumanidis', 'doumani.jpg', 'kdoumani@shotgun.com'),
	('goulaaas', 'pbkdf2:sha256:150000$Bt0WRWM7$50f1c08d7bd9a13c9a11d28846722e617ac6cb623926b420ea68be5be4020b6f', 'Andreas', 'Goulas', 'goulaaas.jpg', 'goulaaas@shotgun.com'),
	('han.yolo', 'pbkdf2:sha256:150000$XTKvywRP$bce5458b680f13523ab4e9df0e9446cc0974404ad3e954361a187952d1de190b', 'Han', 'Solo', 'han.yolo.jpg', 'han.yolo@shotgun.com'),
	('kokkinis', 'pbkdf2:sha256:150000$VUtSUMqF$9ccaf5b30b9a51ec80a6479bb41a453fa3c04cd3397d35b5f2f9aaa587edb6b3', 'Giorgos', 'Kokkinis', 'kokkinis.jpg', 'kokkinis@shotgun.com'),
	('kostino', 'pbkdf2:sha256:150000$863Oqfr3$ff345d6e4ce741d0fc27f091de3e346d1f95a9acaf75c3ea6748f7f26b7a5f4b', 'Konstantinos', 'Triaridis', 'kostino.jpg', 'kostino@shotgun.com'),
	('rickAstley', 'pbkdf2:sha256:150000$iTddI4Pk$d9f6bfd99d6fc639213c8098bd0cf7dfc67b272a04ca2d6c830f20afe08522d2', 'Rick', 'Astley', '5868fa48-beb3-4639-9fb9-2162d4a6130d.jpg', 'rick@roll.com'),
	('TheIronMan', 'pbkdf2:sha256:150000$RH4PMv15$23b2814dfb2383671f6e15931ca8cfd822838a9938a2421c21a2ebae8a5de8e4', 'Robert', 'Downey', 'TheIronMan.jpg', 'TheIronMan@shotgun.com'),
	('yoda', 'pbkdf2:sha256:150000$rR3H72Vm$48b7e0e38bb9aeeea3997236fa11ed254d104b4a968bd62db29f697690581a31', 'Master', 'Yoda', 'yoda.jpg', 'yoda@shotgun.com');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;

-- Dumping structure for table ShotgunDB.userrating
DROP TABLE IF EXISTS `userrating`;
CREATE TABLE IF NOT EXISTS `userrating` (
  `rater` varchar(16) NOT NULL,
  `ratee` varchar(16) NOT NULL,
  `comment` text DEFAULT NULL,
  `stars` tinyint(4) NOT NULL,
  PRIMARY KEY (`rater`,`ratee`),
  KEY `fk_User_has_User_User2_idx` (`ratee`),
  KEY `fk_User_has_User_User1_idx` (`rater`),
  CONSTRAINT `fk_User_has_User_User1` FOREIGN KEY (`rater`) REFERENCES `user` (`username`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_User_has_User_User2` FOREIGN KEY (`ratee`) REFERENCES `user` (`username`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table ShotgunDB.userrating: ~7 rows (approximately)
/*!40000 ALTER TABLE `userrating` DISABLE KEYS */;
INSERT INTO `userrating` (`rater`, `ratee`, `comment`, `stars`) VALUES
	('doumani', 'kostino', 'Cool dude, we\'ve hung out a lot since then.', 5),
	('goulaaas', 'doumani', 'Kewl dude', 5),
	('goulaaas', 'han.yolo', 'Sooooo creepy... Flies around in an old spaceship :(', 1),
	('goulaaas', 'kostino', 'Very cool dude, funny too', 5),
	('kostino', 'doumani', 'Cool dude', 5),
	('kostino', 'goulaaas', 'This guy though', 4),
	('kostino', 'han.yolo', 'Very aggressive and rude', 1);
/*!40000 ALTER TABLE `userrating` ENABLE KEYS */;

-- Dumping structure for view ShotgunDB.user_num_rides
DROP VIEW IF EXISTS `user_num_rides`;
-- Creating temporary table to overcome VIEW dependency errors
CREATE TABLE `user_num_rides` (
	`username` VARCHAR(16) NOT NULL COLLATE 'utf8_general_ci',
	`num_rides` BIGINT(21) NOT NULL
) ENGINE=MyISAM;

-- Dumping structure for view ShotgunDB.avg_driver_rating
DROP VIEW IF EXISTS `avg_driver_rating`;
-- Removing temporary table and create final VIEW structure
DROP TABLE IF EXISTS `avg_driver_rating`;
CREATE ALGORITHM=UNDEFINED SQL SECURITY DEFINER VIEW `avg_driver_rating` AS select `driverrating`.`ratee` AS `ratee`,avg(`driverrating`.`stars`) AS `average_driver_rating` from `driverrating` group by `driverrating`.`ratee` ;

-- Dumping structure for view ShotgunDB.avg_user_rating
DROP VIEW IF EXISTS `avg_user_rating`;
-- Removing temporary table and create final VIEW structure
DROP TABLE IF EXISTS `avg_user_rating`;
CREATE ALGORITHM=UNDEFINED SQL SECURITY DEFINER VIEW `avg_user_rating` AS select `userrating`.`ratee` AS `ratee`,avg(`userrating`.`stars`) AS `average_user_rating` from `userrating` group by `userrating`.`ratee` ;

-- Dumping structure for view ShotgunDB.discount_eligible_users
DROP VIEW IF EXISTS `discount_eligible_users`;
-- Removing temporary table and create final VIEW structure
DROP TABLE IF EXISTS `discount_eligible_users`;
CREATE ALGORITHM=UNDEFINED SQL SECURITY DEFINER VIEW `discount_eligible_users` AS select `u`.`username` AS `username`,`u`.`first_name` AS `first_name`,`u`.`surname` AS `surname` from (`user_num_rides` `n` join `user` `u` on((`u`.`username` = `n`.`username`))) where (`n`.`num_rides` < 5) ;

-- Dumping structure for view ShotgunDB.future_events
DROP VIEW IF EXISTS `future_events`;
-- Removing temporary table and create final VIEW structure
DROP TABLE IF EXISTS `future_events`;
CREATE ALGORITHM=UNDEFINED SQL SECURITY DEFINER VIEW `future_events` AS select `event`.`event_id` AS `event_id`,`event`.`title` AS `title` from `event` where ((`event`.`status` = 'active') and (`event`.`datetime` > now())) ;

-- Dumping structure for view ShotgunDB.not_applied_as_driver
DROP VIEW IF EXISTS `not_applied_as_driver`;
-- Removing temporary table and create final VIEW structure
DROP TABLE IF EXISTS `not_applied_as_driver`;
CREATE ALGORITHM=UNDEFINED SQL SECURITY DEFINER VIEW `not_applied_as_driver` AS select `user`.`username` AS `username`,`user`.`first_name` AS `first_name`,`user`.`surname` AS `surname` from `user` where (not(`user`.`username` in (select `drivercertificationapplication`.`username` from `drivercertificationapplication`))) ;

-- Dumping structure for view ShotgunDB.pending_driver_application
DROP VIEW IF EXISTS `pending_driver_application`;
-- Removing temporary table and create final VIEW structure
DROP TABLE IF EXISTS `pending_driver_application`;
CREATE ALGORITHM=UNDEFINED SQL SECURITY DEFINER VIEW `pending_driver_application` AS select `d`.`username` AS `username`,`u`.`first_name` AS `first_name`,`u`.`surname` AS `surname` from (`drivercertificationapplication` `d` join `user` `u` on((`d`.`username` = `u`.`username`))) where (not(`u`.`username` in (select `driver`.`username` from `driver`))) ;

-- Dumping structure for view ShotgunDB.pending_events
DROP VIEW IF EXISTS `pending_events`;
-- Removing temporary table and create final VIEW structure
DROP TABLE IF EXISTS `pending_events`;
CREATE ALGORITHM=UNDEFINED SQL SECURITY DEFINER VIEW `pending_events` AS select `event`.`event_id` AS `event_id`,`event`.`title` AS `title` from `event` where (`event`.`status` = 'pending') ;

-- Dumping structure for view ShotgunDB.user_num_rides
DROP VIEW IF EXISTS `user_num_rides`;
-- Removing temporary table and create final VIEW structure
DROP TABLE IF EXISTS `user_num_rides`;
CREATE ALGORITHM=UNDEFINED SQL SECURITY DEFINER VIEW `user_num_rides` AS select `application`.`username` AS `username`,count(0) AS `num_rides` from `application` where (`application`.`status` = 'accepted') group by `application`.`username` ;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
