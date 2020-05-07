CREATE TABLE IF NOT EXISTS `metadata` (
    `id` int NOT NULL AUTO_INCREMENT,
    `FileName` VARCHAR(255) NOT NULL,
    `DateTime` DATETIME NOT NULL,
    `DateTimeOriginal` DATETIME NOT NULL,
    `DateTimeDigitized` DATETIME NOT NULL,
    `XResolution` DECIMAL (5,2) NOT NULL,
    `YResolution` DECIMAL (5,2) NOT NULL,
    `ResolutionUnit` ENUM('RESUNIT_NONE','RESUNIT_INCH','RESUNIT_CENTIMETER') NOT NULL,
    PRIMARY KEY (`id`)) ENGINE=InnoDB