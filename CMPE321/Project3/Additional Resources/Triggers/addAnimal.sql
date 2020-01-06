CREATE TRIGGER `addAnimal` BEFORE INSERT ON `animal`
 FOR EACH ROW SET New.Caretaker=(SELECT CONCAT(B.Surname,',',B.Name)
FROM((SELECT A.Name,A.Surname,A.Count_,(ROW_NUMBER() OVER(ORDER BY A.Count_))AS Rank FROM (SELECT Name,Surname,COUNT(*) AS Count_ FROM CARETAKER GROUP BY Name,Surname) AS A))B WHERE B.Rank=1);