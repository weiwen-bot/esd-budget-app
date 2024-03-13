-- Create database for Pool
CREATE DATABASE IF NOT EXISTS `pool`;

-- Use the Pool database
USE `pool`;

-- Create the Pool table
CREATE TABLE IF NOT EXISTS `pool` (
  `PoolID` VARCHAR(36) PRIMARY KEY,
  `DateCreation` DATE NOT NULL,
  `Expiry_Date` DATE NOT NULL,
  `Current_amount` FLOAT NOT NULL,
  `Budget` FLOAT NOT NULL,
  `Pool_Type` VARCHAR(36) NOT NULL,
  `UserID` VARCHAR(36) NOT NULL,
  `Status` VARCHAR(36) NOT NULL
);

-- Insert sample data into Pool table
INSERT INTO `pool` (`PoolID`, `DateCreation`, `Expiry_Date`, `Current_amount`, `Budget`, `Pool_Type`, `UserID`, `Status`)
VALUES 
('1', '2024-03-13', '2024-03-20', 500.00, 1000.00, 'Group', 'user1', 'Active'),
('2', '2024-03-14', '2024-03-21', 700.00, 1500.00, 'Team', 'user2', 'Active'),
('3', '2024-03-15', '2024-03-22', 300.00, 800.00, 'Family', 'user3', 'Inactive');
