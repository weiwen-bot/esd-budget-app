-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Jan 14, 2019 at 06:42 AM
-- Server version: 5.7.19
-- PHP Version: 7.1.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

--
-- Database: `User`
--
CREATE DATABASE IF NOT EXISTS `User` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `User`;

-- --------------------------------------------------------

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

--
-- Dumping data for table `User`
--

-- No data is inserted initially for the 'User' table.
-- You can insert data as needed using INSERT INTO statements.

INSERT INTO User (UserName, PhoneNumber, Credits, Account_no, Email, Password)
VALUES ("John Doe", "123-456-7890", 100.00, "1234567890", "johndoe@example.com", "password123");

CREATE TABLE IF NOT EXISTS `poolmapping` (
  `PoolID` int(11) NOT NULL,
  `UserID` int(11) NOT NULL,
  PRIMARY KEY (`PoolID`, `UserID`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;


COMMIT;
