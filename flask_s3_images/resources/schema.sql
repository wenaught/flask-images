CREATE TABLE IF NOT EXISTS `metadata` (
    `id` int NOT NULL AUTO_INCREMENT,
    `FileName` VARCHAR(255) NOT NULL,
    `DateTime` DATETIME,
    `DateTimeOriginal` DATETIME,
    `DateTimeDigitized` DATETIME,
    `XResolution` DECIMAL (5,2),
    `YResolution` DECIMAL (5,2),
    `ResolutionUnit` ENUM('RESUNIT_NONE','RESUNIT_INCH','RESUNIT_CENTIMETER'),
    PRIMARY KEY (`id`)) ENGINE=InnoDB