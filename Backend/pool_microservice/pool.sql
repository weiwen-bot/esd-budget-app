-- Create database for Pool
CREATE DATABASE IF NOT EXISTS `pool`;

-- Use the Pool database
USE `pool`;

-- Create the Pool table
CREATE TABLE IF NOT EXISTS `pool` (
  `PoolID` int(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `DateCreation` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `pool_name` varchar(36) NOT NULL,
  `pool_desc` varchar(256),
  `Expiry_Date` DATE NOT NULL,
  `Current_amount` FLOAT NOT NULL,
  `Budget` FLOAT NOT NULL,
  `Pool_Type` VARCHAR(36) NOT NULL,
  `UserID` int(11) NOT NULL,
  `Status` VARCHAR(36) NOT NULL
)ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;




CREATE TABLE IF NOT EXISTS `poolmapping` (
  `PoolID` int(11) NOT NULL,
  `UserID` int(11) NOT NULL,
  PRIMARY KEY (`PoolID`, `UserID`)
);


