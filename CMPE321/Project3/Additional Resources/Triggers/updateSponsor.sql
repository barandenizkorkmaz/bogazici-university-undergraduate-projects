CREATE TRIGGER `updateSponsor` AFTER DELETE ON `animal`
 FOR EACH ROW UPDATE Sponsor
SET Sponsor.Animal=(SELECT B.Name FROM (SELECT A.Name,(ROW_NUMBER() OVER(ORDER BY A.Age DESC)) AS Rank FROM (SELECT Name,Age FROM animal WHERE Sponsor IS NOT NULL or Sponsor<>'') AS A) AS B WHERE B.Rank=1)
WHERE Sponsor.Animal=Old.Name AND (Old.Sponsor <> '' OR Old.Sponsor IS NOT NULL);