DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `getAnimals`(IN `speciesName` VARCHAR(255))
    NO SQL
SELECT * FROM animal WHERE Species=speciesName$$
DELIMITER ;