
-- Create database for Pool
CREATE DATABASE IF NOT EXISTS `pool` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `pool`;

-- Create the Pool table
DROP TABLE IF EXISTS `pool`;
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
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE DATABASE IF NOT EXISTS `transaction` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `transaction`;
--
-- Table structure for table `transaction`
--
DROP TABLE IF EXISTS `transaction`;
CREATE TABLE IF NOT EXISTS `transaction` (
  `transactionID` int(11) NOT NULL AUTO_INCREMENT,
  `amount` decimal(10,2) NOT NULL,
  `status` varchar(36) NOT NULL,
  `transactionDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `userID` int(11) NOT NULL,
  `poolID` int(11) NOT NULL,
  PRIMARY KEY (`transactionID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Create database for Pool
CREATE DATABASE IF NOT EXISTS `pool_request` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `pool_request`;

-- Create the Pool table
DROP TABLE IF EXISTS `pool_request`;
CREATE TABLE IF NOT EXISTS `pool_request` (
  `pool_requestID` int(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `PoolID` int(11) NOT NULL,
  `UserID` int(11) NOT NULL,
  `status` VARCHAR(30) NOT NULL
)ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE DATABASE IF NOT EXISTS `notification` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `notification`;
--
-- Table structure for table `User`
--
DROP TABLE IF EXISTS `notification`;
CREATE TABLE IF NOT EXISTS `notification` (
  `notificationID` int(11) NOT NULL AUTO_INCREMENT,
  `notificationType` varchar(50) NOT NULL,
  `receiverID` int(11) NOT NULL,
  `message` varchar(255) NOT NULL,
  `notificationDate` timestamp NOT NULL,
  `status` varchar(36) NOT NULL,
  PRIMARY KEY (`notificationID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--

COMMIT;
