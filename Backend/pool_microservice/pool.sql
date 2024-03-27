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

-- Insert sample data into Pool table
INSERT INTO `pool` (`pool_name`,`pool_desc`,`Expiry_Date`, `Current_amount`, `Budget`, `Pool_Type`, `UserID`, `Status`)
VALUES 
('Family trip','TEsting','2024-03-20', 500.00, 1000.00, 'Group', 1, 'Active'),
('Family trip','TEsting','2024-03-21', 700.00, 1500.00, 'Team', 2, 'Active'),
('Family trip','TEsting','2024-03-22', 300.00, 800.00, 'Family', 2, 'Inactive');



CREATE TABLE IF NOT EXISTS `poolmapping` (
  `PoolID` int(11) NOT NULL,
  `UserID` int(11) NOT NULL,
  PRIMARY KEY (`PoolID`, `UserID`)
)

-- Insert sample data into PoolMapping table
INSERT INTO `poolmapping` (`PoolID`, `UserID`)
VALUES 
(1, 1),
(1, 2),
(2, 2),
(3, 2);
