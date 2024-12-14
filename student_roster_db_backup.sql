-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: student_roster_db
-- ------------------------------------------------------
-- Server version	5.5.5-10.4.32-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `classes`
--

DROP TABLE IF EXISTS `classes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `classes` (
  `idclasses` int(11) NOT NULL AUTO_INCREMENT,
  `description` text NOT NULL,
  `idroom` int(11) DEFAULT NULL,
  `idcourse` int(11) DEFAULT NULL,
  PRIMARY KEY (`idclasses`),
  KEY `fk_classes_rooms_idx` (`idroom`),
  KEY `fk_classes_courses1_idx` (`idcourse`),
  CONSTRAINT `fk_classes_courses1` FOREIGN KEY (`idcourse`) REFERENCES `courses` (`idcourses`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_classes_rooms` FOREIGN KEY (`idroom`) REFERENCES `rooms` (`idrooms`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `classes`
--

LOCK TABLES `classes` WRITE;
/*!40000 ALTER TABLE `classes` DISABLE KEYS */;
INSERT INTO `classes` VALUES (1,'Algebra basics class',1,1),(2,'Physics mechanics lecture',3,2),(3,'Introductory biology',6,3),(4,'Chemical reactions lab',7,4),(5,'Basic programming',8,5),(6,'World history overview',10,6),(7,'Psychology fundamentals',11,7),(8,'Shakespeare analysis',12,8),(9,'Renaissance art history',13,9),(10,'Choral music basics',14,10),(11,'Philosophy and ethics',15,11),(12,'Intro to statistics',16,12),(13,'Environmental challenges',17,13),(14,'Principles of economics',18,14),(15,'Introduction to sociology',19,15),(16,'International relations',20,16),(17,'Marketing strategies',21,17),(18,'Finance for beginners',22,18),(19,'Business startup',23,19),(20,'Code debugging workshop',24,20),(21,'Advanced algorithms',25,21),(22,'Kernel design class',2,22),(23,'Relational database workshop',4,23),(24,'LAN architecture basics',5,24),(25,'Firewall configurations',9,25);
/*!40000 ALTER TABLE `classes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `courses`
--

DROP TABLE IF EXISTS `courses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `courses` (
  `idcourses` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `code` varchar(45) NOT NULL,
  PRIMARY KEY (`idcourses`),
  UNIQUE KEY `code_UNIQUE` (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `courses`
--

LOCK TABLES `courses` WRITE;
/*!40000 ALTER TABLE `courses` DISABLE KEYS */;
INSERT INTO `courses` VALUES (1,'Mathematics 101','MATH101'),(2,'Physics 201','PHYS201'),(3,'Biology 101','BIO101'),(4,'Chemistry 201','CHEM201'),(5,'Computer Science 101','CS101'),(6,'History 101','HIST101'),(7,'Psychology 201','PSYCH201'),(8,'English Literature 101','ENG101'),(9,'Art Appreciation 101','ART101'),(10,'Music Theory 101','MUSIC101'),(11,'Philosophy 101','PHIL101'),(12,'Statistics 201','STAT201'),(13,'Environmental Science 101','ENV101'),(14,'Economics 101','ECON101'),(15,'Sociology 101','SOC101'),(16,'Political Science 201','POL201'),(17,'Marketing 101','MARK101'),(18,'Finance 101','FIN101'),(19,'Business Administration 101','BA101'),(20,'Programming Fundamentals','PROG101'),(21,'Data Structures','DS101'),(22,'Operating Systems','OS101'),(23,'Database Systems','DBS101'),(24,'Networking Basics','NET101'),(25,'Cybersecurity 101','CYBER101');
/*!40000 ALTER TABLE `courses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rooms`
--

DROP TABLE IF EXISTS `rooms`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rooms` (
  `idrooms` int(11) NOT NULL AUTO_INCREMENT,
  `location` varchar(45) NOT NULL,
  `description` text DEFAULT NULL,
  PRIMARY KEY (`idrooms`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rooms`
--

LOCK TABLES `rooms` WRITE;
/*!40000 ALTER TABLE `rooms` DISABLE KEYS */;
INSERT INTO `rooms` VALUES (1,'Building A, Room 101','First floor classroom.'),(2,'Building A, Room 102','Second floor classroom.'),(3,'Building B, Room 201','Lecture hall with projector.'),(4,'Building B, Room 202','Computer lab with 20 PCs.'),(5,'Building C, Room 301','Library conference room.'),(6,'Building C, Room 302','Science lab with equipment.'),(7,'Building D, Room 401','Art studio for workshops.'),(8,'Building D, Room 402','Physics lab with tools.'),(9,'Building E, Room 501','Math lecture hall.'),(10,'Building E, Room 502','Large assembly hall.'),(11,'Building F, Room 601','Faculty meeting room.'),(12,'Building F, Room 602','Language learning lab.'),(13,'Building G, Room 701','Auditorium for events.'),(14,'Building G, Room 702','Music room with instruments.'),(15,'Building H, Room 801','Outdoor pavilion space.'),(16,'Building H, Room 802','Drama rehearsal hall.'),(17,'Building I, Room 901','Reserved for special lectures.'),(18,'Building I, Room 902','Advanced computer lab.'),(19,'Building J, Room 1001','Library annex.'),(20,'Building J, Room 1002','Counseling office.'),(21,'Building K, Room 1101','Small seminar room.'),(22,'Building K, Room 1102','Staff workspace.'),(23,'Building L, Room 1201','Biology lab with microscopes.'),(24,'Building L, Room 1202','Robotics workshop.'),(25,'Building M, Room 1301','Empty classroom for reservations.');
/*!40000 ALTER TABLE `rooms` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roster`
--

DROP TABLE IF EXISTS `roster`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roster` (
  `idroster` int(11) NOT NULL AUTO_INCREMENT,
  `idclass` int(11) DEFAULT NULL,
  `idstudent` int(11) DEFAULT NULL,
  `idteacher` int(11) DEFAULT NULL,
  `class_period` varchar(45) NOT NULL,
  PRIMARY KEY (`idroster`),
  KEY `fk_roster_classes1_idx` (`idclass`),
  KEY `fk_roster_students1_idx` (`idstudent`),
  KEY `fk_roster_teachers1_idx` (`idteacher`),
  CONSTRAINT `fk_roster_classes1` FOREIGN KEY (`idclass`) REFERENCES `classes` (`idclasses`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_roster_students1` FOREIGN KEY (`idstudent`) REFERENCES `students` (`idstudents`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_roster_teachers1` FOREIGN KEY (`idteacher`) REFERENCES `teachers` (`idteachers`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roster`
--

LOCK TABLES `roster` WRITE;
/*!40000 ALTER TABLE `roster` DISABLE KEYS */;
INSERT INTO `roster` VALUES (1,1,1,1,'Morning'),(2,1,2,1,'Morning'),(3,2,3,2,'Afternoon'),(4,2,4,2,'Afternoon'),(5,3,5,3,'Morning'),(6,3,6,3,'Morning'),(7,4,7,4,'Afternoon'),(8,4,8,4,'Afternoon'),(9,5,9,5,'Morning'),(10,5,10,5,'Morning'),(11,6,11,6,'Afternoon'),(12,6,12,6,'Afternoon'),(13,7,13,7,'Morning'),(14,7,14,7,'Morning'),(15,8,15,8,'Afternoon'),(16,8,16,8,'Afternoon'),(17,9,17,9,'Morning'),(18,9,18,9,'Morning'),(19,10,19,10,'Afternoon'),(20,10,20,10,'Afternoon'),(21,11,21,11,'Morning'),(22,11,22,11,'Morning'),(23,12,23,12,'Afternoon'),(24,12,24,12,'Afternoon'),(25,12,25,12,'Afternoon');
/*!40000 ALTER TABLE `roster` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `students`
--

DROP TABLE IF EXISTS `students`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `students` (
  `idstudents` int(11) NOT NULL AUTO_INCREMENT,
  `firstname` varchar(50) NOT NULL,
  `middlename` varchar(50) DEFAULT NULL,
  `lastname` varchar(50) NOT NULL,
  `birthdate` date NOT NULL,
  `gender` varchar(10) NOT NULL COMMENT '0 - Male\n1- Female',
  PRIMARY KEY (`idstudents`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `students`
--

LOCK TABLES `students` WRITE;
/*!40000 ALTER TABLE `students` DISABLE KEYS */;
INSERT INTO `students` VALUES (1,'Alice','May','Johnson','2005-03-21','Female'),(2,'Brian','Lee','Smith','2004-12-15','Male'),(3,'Catherine','Anne','Davis','2003-07-09','Female'),(4,'David','Michael','Garcia','2005-06-25','Male'),(5,'Evelyn','Rose','Martinez','2004-08-18','Female'),(6,'Frank','James','Rodriguez','2003-11-02','Male'),(7,'Grace','Elizabeth','Wilson','2005-01-30','Female'),(8,'Henry','Robert','Anderson','2004-05-22','Male'),(9,'Isabella','Sophia','Thomas','2003-09-14','Female'),(10,'Jacob','William','Taylor','2005-04-05','Male'),(11,'Kayla','Marie','Moore','2004-02-17','Female'),(12,'Liam','Alexander','Harris','2003-03-28','Male'),(13,'Mia','Faith','Clark','2005-10-12','Female'),(14,'Noah','Logan','Lewis','2004-07-19','Male'),(15,'Olivia','Grace','Lee','2003-12-20','Female'),(16,'Patrick','Ryan','Walker','2005-06-07','Male'),(17,'Quinn','Victoria','Hall','2004-09-16','Female'),(18,'Ryan','Thomas','Allen','2003-05-31','Male'),(19,'Sophia','Rose','Young','2005-02-14','Female'),(20,'Tyler','James','King','2004-10-22','Male'),(21,'Uma','Marie','Wright','2003-01-13','Female'),(22,'Victor','Samuel','Scott','2005-07-03','Male'),(23,'Wendy','Anne','Green','2004-03-26','Female'),(24,'Xavier','David','Baker','2003-08-08','Male'),(25,'Yvonne','Claire','Adams','2005-11-18','Female');
/*!40000 ALTER TABLE `students` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teachers`
--

DROP TABLE IF EXISTS `teachers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `teachers` (
  `idteachers` int(11) NOT NULL AUTO_INCREMENT,
  `firstname` varchar(50) NOT NULL,
  `middlename` varchar(50) DEFAULT NULL,
  `lastname` varchar(50) NOT NULL,
  `birthdate` date NOT NULL DEFAULT '1990-01-01',
  `gender` varchar(10) NOT NULL,
  PRIMARY KEY (`idteachers`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teachers`
--

LOCK TABLES `teachers` WRITE;
/*!40000 ALTER TABLE `teachers` DISABLE KEYS */;
INSERT INTO `teachers` VALUES (1,'Anne','Marie','Baker','1980-01-15','Female'),(2,'John','Andrew','Doe','1982-03-22','Male'),(3,'Karen','Elizabeth','White','1975-07-30','Female'),(4,'Michael','David','Black','1990-11-18','Male'),(5,'Susan','Grace','Green','1985-05-27','Female'),(6,'Robert','James','Brown','1978-09-12','Male'),(7,'Emily','Rose','Adams','1987-04-05','Female'),(8,'William','Thomas','Carter','1983-06-14','Male'),(9,'Jessica','Lynn','Evans','1976-10-25','Female'),(10,'Thomas','Daniel','Turner','1992-08-30','Male'),(11,'Rachel','Claire','Taylor','1981-12-19','Female'),(12,'Chris','Edward','Hughes','1974-02-10','Male'),(13,'Olivia','Sophia','Scott','1995-03-09','Female'),(14,'Andrew','Nicholas','Morris','1989-07-21','Male'),(15,'Natalie','Alice','Hall','1977-11-16','Female'),(16,'James','Alexander','Allen','1984-01-02','Male'),(17,'Victoria','Grace','Wright','1973-09-18','Female'),(18,'Peter','Samuel','King','1991-05-13','Male'),(19,'Sarah','Marie','Hill','1988-06-25','Female'),(20,'Kevin','Patrick','Moore','1979-10-07','Male'),(21,'Lucy','Ella','Parker','1986-12-03','Female'),(22,'Mark','Logan','Harris','1980-04-28','Male'),(23,'Chloe','Faith','Ward','1975-08-15','Female'),(24,'Ryan','Jacob','Reed','1993-02-07','Male'),(25,'Mia','Isabelle','Bennett','1982-09-30','Female');
/*!40000 ALTER TABLE `teachers` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-12-14 13:27:39
