-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 03, 2024 at 06:06 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `iris v0.1`
--

-- --------------------------------------------------------

--
-- Table structure for table `stocks`
--

CREATE TABLE `stocks` (
  `id` int(11) NOT NULL,
  `item_id` mediumtext DEFAULT NULL,
  `name` mediumtext DEFAULT NULL,
  `price` mediumtext DEFAULT NULL,
  `quantity` mediumtext DEFAULT NULL,
  `category` mediumtext DEFAULT NULL,
  `date` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=Aria DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `stocks`
--

INSERT INTO `stocks` (`id`, `item_id`, `name`, `price`, `quantity`, `category`, `date`) VALUES
(18, '058-P', 'Hammer', '150', '200', 'Repair Tools', '2024-11-30 17:34:29'),
(17, '110-H', 'Intel Processor', '12000', '26', 'Computer Parts', '2024-11-30 17:34:14'),
(15, '411-G', 'Power Supply', '100', '200', 'Gadgets', '2024-11-30 16:40:54'),
(14, '817-A', 'Processor AMD 5', '1000000', '154', 'Computer Parts', '2024-11-30 15:52:33'),
(13, '644-K', 'Video Card', '10000', '12', 'Computer Parts', '2024-11-30 15:51:34'),
(19, '878-L', 'hola', '1231', '124124', 'Repair Tools', '2024-11-30 17:52:16');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `stocks`
--
ALTER TABLE `stocks`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `stocks`
--
ALTER TABLE `stocks`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
