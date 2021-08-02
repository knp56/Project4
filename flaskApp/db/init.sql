CREATE DATABASE addressData;
use addressData;

CREATE TABLE IF NOT EXISTS addresses (
    `id` int AUTO_INCREMENT,
    `fName` VARCHAR(21) CHARACTER SET utf8,
    `lName` VARCHAR(8) CHARACTER SET utf8,
    `Address` VARCHAR(32) CHARACTER SET utf8,
    `City` VARCHAR(11) CHARACTER SET utf8,
    `State` VARCHAR(3) CHARACTER SET utf8,
    `Zip` INT,
    PRIMARY KEY (`id`)
);
INSERT INTO addresses (fName,lName,Address,City,State,Zip) VALUES
    ('Jack','McGinnis','220 hobo Av.','Phila',' PA',09119),
    ('John "Da Man"','Repici','120 Jefferson St.','Riverside',' NJ',08075),
    ('Stephen','Tyler','7452 Terrace "At the Plaza" road','SomeTown','SD', 91234),
    (NULL,'Blankman',NULL,'SomeTown',' SD', 00298),
    ('Joan "the bone", Anne','Jet','9th, at Terrace plc','Desert City','CO',00123);