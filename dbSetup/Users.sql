# Create user admin with all rights and grant option
CREATE USER 'admin'@'localhost' IDENTIFIED BY 'adminPassword';
GRANT ALL PRIVILEGES ON shotgundb.* TO 'admin'@'localhost' WITH GRANT OPTION;

# Create user moderator 
CREATE USER 'mod'@'localhost' IDENTIFIED BY 'modPassword';
CREATE USER 'mod'@'%' IDENTIFIED BY 'modPassword';

GRANT SELECT ON shotgundb.application TO 'mod'@'%';
GRANT SELECT ON shotgundb.driverrating TO 'mod'@'%';
GRANT SELECT ON shotgundb.ride TO 'mod'@'%';
GRANT SELECT ON shotgundb.user TO 'mod'@'%';
GRANT SELECT ON shotgundb.userrating TO 'mod'@'%';
GRANT SELECT, INSERT, UPDATE, DELETE ON shotgundb.driver TO 'mod'@'%';
GRANT SELECT, INSERT, UPDATE, DELETE ON shotgundb.drivercertificationapplication TO 'mod'@'%';
GRANT SELECT, INSERT, UPDATE, DELETE ON shotgundb.event TO 'mod'@'%';

GRANT SELECT ON shotgundb.application TO 'mod'@'localhost';
GRANT SELECT ON shotgundb.driverrating TO 'mod'@'localhost';
GRANT SELECT ON shotgundb.ride TO 'mod'@'localhost';
GRANT SELECT ON shotgundb.user TO 'mod'@'localhost';
GRANT SELECT ON shotgundb.userrating TO 'mod'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON shotgundb.driver TO 'mod'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON shotgundb.drivercertificationapplication TO 'mod'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON shotgundb.event TO 'mod'@'localhost';

# Create user appUser
CREATE USER 'appUser'@'localhost' IDENTIFIED BY 'appUserPassword';
CREATE USER 'appUser'@'%' IDENTIFIED BY 'appUserPassword';

GRANT SELECT, INSERT, DELETE ON shotgundb.application TO 'appUser'@'%';
GRANT SELECT, INSERT ON shotgundb.driverrating TO 'appUser'@'%';
GRANT SELECT ON shotgundb.ride TO 'appUser'@'%';
GRANT SELECT, UPDATE ON shotgundb.user TO 'appUser'@'%';
GRANT SELECT, INSERT ON shotgundb.userrating TO 'appUser'@'%';
GRANT SELECT ON shotgundb.driver TO 'appUser'@'%';
GRANT SELECT, INSERT ON shotgundb.drivercertificationapplication TO 'appUser'@'%';
GRANT SELECT, INSERT ON shotgundb.event TO 'appUser'@'%';
GRANT SELECT, INSERT, UPDATE, DELETE ON shotgundb.paymentmethod TO 'appUser'@'%';
GRANT SELECT, INSERT, UPDATE, DELETE ON shotgundb.paypalaccount TO 'appUser'@'%';
GRANT SELECT, INSERT, UPDATE, DELETE ON shotgundb.creditcard TO 'appUser'@'%';

GRANT SELECT, INSERT, DELETE ON shotgundb.application TO 'appUser'@'localhost';
GRANT SELECT, INSERT ON shotgundb.driverrating TO 'appUser'@'localhost';
GRANT SELECT ON shotgundb.ride TO 'appUser'@'localhost';
GRANT SELECT, UPDATE ON shotgundb.user TO 'appUser'@'localhost';
GRANT SELECT, INSERT ON shotgundb.userrating TO 'appUser'@'localhost';
GRANT SELECT ON shotgundb.driver TO 'appUser'@'localhost';
GRANT SELECT, INSERT ON shotgundb.drivercertificationapplication TO 'appUser'@'localhost';
GRANT SELECT, INSERT ON shotgundb.event TO 'appUser'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON shotgundb.paymentmethod TO 'appUser'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON shotgundb.paypalaccount TO 'appUser'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON shotgundb.creditcard TO 'appUser'@'localhost';

# Create user appDriver
CREATE USER 'appDriver'@'localhost' IDENTIFIED BY 'appDriverPassword';
CREATE USER 'appDriver'@'%' IDENTIFIED BY 'appDriverPassword';

GRANT SELECT, INSERT, UPDATE, DELETE ON shotgundb.application TO 'appDriver'@'%';
GRANT SELECT, INSERT ON shotgundb.driverrating TO 'appDriver'@'%';
GRANT SELECT, INSERT, UPDATE, DELETE ON shotgundb.ride TO 'appDriver'@'%';
GRANT SELECT, UPDATE ON shotgundb.user TO 'appDriver'@'%';
GRANT SELECT, INSERT ON shotgundb.userrating TO 'appDriver'@'%';
GRANT SELECT, UPDATE ON shotgundb.driver TO 'appDriver'@'%';
GRANT SELECT ON shotgundb.drivercertificationapplication TO 'appDriver'@'%';
GRANT SELECT, INSERT ON shotgundb.event TO 'appDriver'@'%';
GRANT SELECT, INSERT, UPDATE, DELETE ON shotgundb.paymentmethod TO 'appDriver'@'%';
GRANT SELECT, INSERT, UPDATE, DELETE ON shotgundb.paypalaccount TO 'appDriver'@'%';
GRANT SELECT, INSERT, UPDATE, DELETE ON shotgundb.creditcard TO 'appDriver'@'%';

GRANT SELECT, INSERT, UPDATE, DELETE ON shotgundb.application TO 'appDriver'@'localhost';
GRANT SELECT, INSERT ON shotgundb.driverrating TO 'appDriver'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON shotgundb.ride TO 'appDriver'@'localhost';
GRANT SELECT, UPDATE ON shotgundb.user TO 'appDriver'@'localhost';
GRANT SELECT, INSERT ON shotgundb.userrating TO 'appDriver'@'localhost';
GRANT SELECT, UPDATE ON shotgundb.driver TO 'appDriver'@'localhost';
GRANT SELECT ON shotgundb.drivercertificationapplication TO 'appDriver'@'localhost';
GRANT SELECT, INSERT ON shotgundb.event TO 'appDriver'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON shotgundb.paymentmethod TO 'appDriver'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON shotgundb.paypalaccount TO 'appDriver'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON shotgundb.creditcard TO 'appDriver'@'localhost';