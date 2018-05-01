LOCK TABLES `test_table` WRITE;
INSERT INTO `test_table` VALUES ('world'),('moon'),('mars'),('galaxy'),('black hole');
UNLOCK TABLES;

LOCK TABLES `users` WRITE;
INSERT INTO `users` VALUES (1,1,'Aidik','vaclav@ixsystems.com','1234','Václav','Navrátil'),
						   (2,1,'Sirdik','ladislav@ixsystems.com','abcd','Ladislav','Sirový'),
						   (3,1,'Luisbob','luis@ixsystems.com','password','Luis','Antonio'),
						   (4,0,'Pegasus','pegasus@no.nic','123','Aerial','Horse'),
						   (5,0,'Binky','binky@no.nic','123','Binky','Horse'),
						   (6,0,'Roach','roach@no.nic','123','Geralt\'s','Horse');
UNLOCK TABLES;

LOCK TABLES `machines` WRITE;
INSERT INTO `machines` VALUES (1,1,'Mini','CXIRq_9gQUSofK3xPl2dUA'),
							  (2,1,'Maxi','NsmFzz5S106eTw1FQODtAw'),
							  (3,4,'Xena','9EGxVzwJ_0y-uGdlgT5_1A'),
							  (4,6,'Ciri','Pcp3rdxXQ02TwppU4oLJmg');
UNLOCK TABLES;


LOCK TABLES `files` WRITE;
INSERT INTO `files` VALUES (1,1,'FN9.10 DB Dump','2014-02-14 11:43:41'),
						   (2,1,'FN11.0 DB Dump','2016-12-03 23:11:42'),
						   (3,1,'FN11.1 DB Dump','2018-01-16 14:27:15'),
						   (4,3,'Secret','2008-01-20 21:14:56');
UNLOCK TABLES;