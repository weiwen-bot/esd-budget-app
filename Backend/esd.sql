--
-- Database: `User`
--
CREATE DATABASE IF NOT EXISTS `User` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `User`;
--
-- Table structure for table `User`
--
DROP TABLE IF EXISTS `User`;
CREATE TABLE IF NOT EXISTS `User` (
  `UserID` int(11) NOT NULL AUTO_INCREMENT,
  `UserName` varchar(50) NOT NULL,
  `PhoneNumber` varchar(20) NOT NULL,
  `Credits` decimal(10,5) NOT NULL,
  `Account_no` varchar(20) NOT NULL,
  `Email` varchar(50) NOT NULL,
  `Password` varchar(50) NOT NULL,
  PRIMARY KEY (`UserID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO User ( `UserName`, `PhoneNumber`,`Credits`, `Account_no`,`Email`,`Password`)
VALUES ('User1', '99998888', 200, '4242424242424242', 'user1@gmail.com','pwd1'),
('User2', '99998888', 200, '4242424242424242', 'user2@gmail.com','pwd2'),
('User3', '99998888', 200, '4242424242424242', 'user2@gmail.com','pwd2');
--
-- Dumping data for table `User`
--

-- No data is inserted initially for the 'User' table.
-- You can insert data as needed using INSERT INTO statements.

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

INSERT INTO pool (`pool_name`, `pool_desc`, `Expiry_Date`, `Current_amount`, `Budget`, `Pool_Type`, `UserID`, `Status`) VALUES
('Pool1', 'Pool1 Description', '2021-12-31', 0, 1000, 'Budget', 1, 'Active');

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
  `paymentIntent` varchar(255) NULL,
  `refund_status` varchar(36) NULL,
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

CREATE DATABASE IF NOT EXISTS `refund` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `refund`;
--
-- Table structure for table `transaction`
--

DROP TABLE IF EXISTS `refund`;
CREATE TABLE IF NOT EXISTS `refund` (
  `refundID` int(11) NOT NULL AUTO_INCREMENT,
  `amount` decimal(10,2) NOT NULL,
  `status` varchar(36) NOT NULL,
  `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `userID` int(11) NOT NULL,
  `poolID` int(11) NOT NULL,
  PRIMARY KEY (`refundID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


COMMIT;
