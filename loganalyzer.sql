-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 19, 2023 at 12:44 PM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 8.1.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `loganalyzer`
--

-- --------------------------------------------------------

--
-- Table structure for table `domains_db`
--

CREATE TABLE `domains_db` (
  `id` int(11) NOT NULL,
  `domain_name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `domains_db`
--

INSERT INTO `domains_db` (`id`, `domain_name`) VALUES
(1, 'google.com'),
(2, 'ppdb.sman4tangerang.sch.id'),
(3, 'zeldin.tech'),
(4, 'perpus.sman4tangerang.sch.id');

-- --------------------------------------------------------

--
-- Table structure for table `logs_details_db`
--

CREATE TABLE `logs_details_db` (
  `id` int(11) NOT NULL,
  `domain_id` int(25) NOT NULL,
  `logs_storage_id` int(11) NOT NULL,
  `log_text` text NOT NULL,
  `ip_address` int(11) NOT NULL,
  `date` varchar(255) NOT NULL,
  `method` varchar(255) NOT NULL,
  `url` text NOT NULL,
  `status_code` varchar(30) NOT NULL,
  `user_agent` text NOT NULL,
  `log_type` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `logs_storage_db`
--

CREATE TABLE `logs_storage_db` (
  `id` int(11) NOT NULL,
  `file_location` text NOT NULL,
  `domain_id` int(13) NOT NULL,
  `analyzed` int(1) NOT NULL,
  `created_at` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `logs_storage_db`
--

INSERT INTO `logs_storage_db` (`id`, `file_location`, `domain_id`, `analyzed`, `created_at`) VALUES
(5, 'sman4tangerang.sch.id.ppdb.log.1', 2, 0, '2023-04-12'),
(6, 'sman4tangerang.sch.id.perpus.log.1', 4, 0, '2023-05-16');

-- --------------------------------------------------------

--
-- Table structure for table `patterns_db`
--

CREATE TABLE `patterns_db` (
  `id` int(11) NOT NULL,
  `pattern_name` varchar(50) NOT NULL,
  `pattern_syntax` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `user_db`
--

CREATE TABLE `user_db` (
  `id` int(11) NOT NULL,
  `username` varchar(30) NOT NULL,
  `password_hash` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user_db`
--

INSERT INTO `user_db` (`id`, `username`, `password_hash`) VALUES
(1, 'admin', '$2a$12$LwToUec3VpsvbHP68/CJ6ei3gEDbZbLIAhmbgYDOJWqXkS7cYCHSu');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `domains_db`
--
ALTER TABLE `domains_db`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `logs_details_db`
--
ALTER TABLE `logs_details_db`
  ADD PRIMARY KEY (`id`),
  ADD KEY `logs details need logs storage` (`logs_storage_id`);

--
-- Indexes for table `logs_storage_db`
--
ALTER TABLE `logs_storage_db`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user_db`
--
ALTER TABLE `user_db`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `domains_db`
--
ALTER TABLE `domains_db`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `logs_details_db`
--
ALTER TABLE `logs_details_db`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `logs_storage_db`
--
ALTER TABLE `logs_storage_db`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `user_db`
--
ALTER TABLE `user_db`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `logs_details_db`
--
ALTER TABLE `logs_details_db`
  ADD CONSTRAINT `logs details need logs storage` FOREIGN KEY (`logs_storage_id`) REFERENCES `logs_storage_db` (`id`);

--
-- Constraints for table `logs_storage_db`
--
ALTER TABLE `logs_storage_db`
  ADD CONSTRAINT `storage need domains` FOREIGN KEY (`domain_id`) REFERENCES `domains_db` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
