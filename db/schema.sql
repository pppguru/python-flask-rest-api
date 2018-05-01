--
-- Lets first drop all the tables in a convinent order
--

DROP TABLE IF EXISTS `test_table`;
DROP TABLE IF EXISTS `sessions`;
DROP TABLE IF EXISTS `files`;
DROP TABLE IF EXISTS `machines`;
DROP TABLE IF EXISTS `users`;

--
-- Lets create all the tables again in convinent order
--

CREATE TABLE `test_table` (
  `hello` varchar(25) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `admin` tinyint(4) DEFAULT NULL,
  `username` varchar(60) NOT NULL,
  `email` varchar(60) NOT NULL,
  `password` varchar(120) NOT NULL,
  `name` varchar(120) DEFAULT NULL,
  `surname` varchar(120) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  UNIQUE KEY `username_UNIQUE` (`username`),
  UNIQUE KEY `email_UNIQUE` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `sessions` (
  `user_id` int(11) NOT NULL,
  `token` varchar(24) NOT NULL,
  `expiration` timestamp NULL DEFAULT NULL,
  KEY `user_id_idx` (`user_id`),
  CONSTRAINT `user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `machines` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `owner_id` int(11) NOT NULL,
  `name` varchar(60) NOT NULL,
  `token` varchar(24) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `owner_id_idx` (`owner_id`),
  CONSTRAINT `id` FOREIGN KEY (`owner_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `files` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `machine_id` int(11) NOT NULL,
  `name` varchar(45) NOT NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `machine_id_idx` (`machine_id`),
  CONSTRAINT `machine_id` FOREIGN KEY (`machine_id`) REFERENCES `machines` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Create triggers
--

-- This one sets expiration date for token. 30min in the future
DELIMITER ;;
CREATE TRIGGER `set_expiration` BEFORE INSERT
    ON `sessions`
    FOR EACH ROW BEGIN
        SET NEW.expiration = (NOW() + interval 30 minute);
  END ;;
DELIMITER ;