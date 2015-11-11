-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               5.6.27-0ubuntu0.14.04.1 - (Ubuntu)
-- Server OS:                    debian-linux-gnu
-- HeidiSQL Version:             9.3.0.4984
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

-- Dumping database structure for elasistente
CREATE DATABASE IF NOT EXISTS `elasistente` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `elasistente`;


-- Dumping structure for table elasistente.auth_cas
CREATE TABLE IF NOT EXISTS `auth_cas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `created_on` datetime DEFAULT NULL,
  `service` varchar(512) DEFAULT NULL,
  `ticket` varchar(512) DEFAULT NULL,
  `renew` char(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id__idx` (`user_id`),
  CONSTRAINT `auth_cas_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.


-- Dumping structure for table elasistente.auth_event
CREATE TABLE IF NOT EXISTS `auth_event` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `time_stamp` datetime DEFAULT NULL,
  `client_ip` varchar(512) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `origin` varchar(512) DEFAULT NULL,
  `description` longtext,
  PRIMARY KEY (`id`),
  KEY `user_id__idx` (`user_id`),
  CONSTRAINT `auth_event_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.


-- Dumping structure for table elasistente.auth_group
CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `role` varchar(512) DEFAULT NULL,
  `description` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.


-- Dumping structure for table elasistente.auth_membership
CREATE TABLE IF NOT EXISTS `auth_membership` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `group_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id__idx` (`user_id`),
  KEY `group_id__idx` (`group_id`),
  CONSTRAINT `auth_membership_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE,
  CONSTRAINT `auth_membership_ibfk_2` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.


-- Dumping structure for table elasistente.auth_permission
CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) DEFAULT NULL,
  `name` varchar(512) DEFAULT NULL,
  `table_name` varchar(512) DEFAULT NULL,
  `record_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `group_id__idx` (`group_id`),
  CONSTRAINT `auth_permission_ibfk_1` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.


-- Dumping structure for table elasistente.auth_user
CREATE TABLE IF NOT EXISTS `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(128) DEFAULT NULL,
  `last_name` varchar(128) DEFAULT NULL,
  `email` varchar(512) DEFAULT NULL,
  `password` varchar(512) DEFAULT NULL,
  `registration_key` varchar(512) DEFAULT NULL,
  `reset_password_key` varchar(512) DEFAULT NULL,
  `registration_id` varchar(512) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.


-- Dumping structure for table elasistente.correlativa
CREATE TABLE IF NOT EXISTS `correlativa` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `materia` int(11) DEFAULT NULL,
  `rpc` longtext,
  `apc` longtext,
  PRIMARY KEY (`id`),
  UNIQUE KEY `materia` (`materia`),
  KEY `materia__idx` (`materia`),
  CONSTRAINT `correlativa_ibfk_1` FOREIGN KEY (`materia`) REFERENCES `materia` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.


-- Dumping structure for table elasistente.estado_academico
CREATE TABLE IF NOT EXISTS `estado_academico` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `usuario` int(11) DEFAULT NULL,
  `regulares` longtext,
  `aprobadas` longtext,
  PRIMARY KEY (`id`),
  UNIQUE KEY `usuario` (`usuario`),
  KEY `usuario__idx` (`usuario`),
  CONSTRAINT `estado_academico_ibfk_1` FOREIGN KEY (`usuario`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.


-- Dumping structure for table elasistente.horario_clases
CREATE TABLE IF NOT EXISTS `horario_clases` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `turno` int(11) DEFAULT NULL,
  `materia` int(11) DEFAULT NULL,
  `comision` varchar(3) DEFAULT NULL,
  `dia` varchar(2) DEFAULT NULL,
  `modulo` longtext,
  PRIMARY KEY (`id`),
  KEY `turno__idx` (`turno`),
  KEY `materia__idx` (`materia`),
  CONSTRAINT `horario_clases_ibfk_1` FOREIGN KEY (`turno`) REFERENCES `turno` (`id`) ON DELETE CASCADE,
  CONSTRAINT `horario_clases_ibfk_2` FOREIGN KEY (`materia`) REFERENCES `materia` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.


-- Dumping structure for table elasistente.materia
CREATE TABLE IF NOT EXISTS `materia` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `anio` varchar(512) DEFAULT NULL,
  `nombre` varchar(200) DEFAULT NULL,
  `anual` varchar(20) DEFAULT NULL,
  `primer_cuatrimestre` varchar(20) DEFAULT NULL,
  `segundo_cuatrimestre` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.


-- Dumping structure for table elasistente.modulo
CREATE TABLE IF NOT EXISTS `modulo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `turno` int(11) DEFAULT NULL,
  `hora_inicio` time DEFAULT NULL,
  `numero_modulo` varchar(3) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `turno__idx` (`turno`),
  CONSTRAINT `modulo_ibfk_1` FOREIGN KEY (`turno`) REFERENCES `turno` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.


-- Dumping structure for table elasistente.turno
CREATE TABLE IF NOT EXISTS `turno` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `descripcion` varchar(15) DEFAULT NULL,
  `numero_turno` varchar(2) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
