-- Create database for Pool
CREATE SCHEMA IF NOT EXISTS `pool_request`;

-- Use the Pool database
USE `pool_request`;

-- Create the Pool table
CREATE TABLE IF NOT EXISTS `pool_request` (
  `pool_requestID` int(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `PoolID` int(11) NOT NULL,
  `UserID` int(11) NOT NULL,
  `status` VARCHAR(30) NOT NULL
)ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

-- Insert sample data into Pool table
INSERT INTO `pool_request` (`PoolID`, `UserID`, `status`)
VALUES 
(1, 2, 'pending'),
(1, 3, 'pending'),
(1, 4, 'pending');

