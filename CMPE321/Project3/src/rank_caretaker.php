<html>
    <body>
        <?php
            $servername = "localhost";
            $username = "root";
            $password = "";
            $dbname = "sheltermanagerdb";

            // Create connection
            $conn = new mysqli($servername, $username, $password, $dbname);
            
            // Check connection
            if ($conn->connect_error) {
                die("Connection failed: " . $conn->connect_error);
            }else{

                // Insert the record
                $sql = "SELECT A.Name,A.Surname,A.Count_,(RANK() OVER(ORDER BY A.Count_ DESC))AS Rank FROM (SELECT Name,Surname,COUNT(*) AS Count_ FROM CARETAKER GROUP BY Name,Surname) AS A";
                $result =  $conn->query($sql);
                 if ($result->num_rows > 0) {
                    ?>
                    <tr>
                        <th>CARETAKERS BY RANKS</th>
                    </tr>
                    <table border = 3>
                        
                        <tr>
                            <th>Rank</th>
                            <th>Name</th>
                            <th>Surname</th>
                            <th>Number of Animals</th>
                        </tr>
                    <?php
                    // output data of each row
                    while($row = $result->fetch_assoc()) {
                        ?>
                        <tr>
                            <td><?php echo $row["Rank"]; ?></td>
                            <td><?php echo $row["Name"]; ?></td>
                            <td><?php echo $row["Surname"]; ?></td>
                            <td><?php echo $row["Count_"]; ?></td>
                        </tr>
                        <?php
                    }

                    ?>
                    </table>
                    <?php
                    echo "<a href = 'homepage.php'>Back</a>";
                } else {
                    echo "No caretakers to list!"."<br>";
                    echo "<a href = 'homepage.php'>Back</a>";
                }
            }
            $conn->close();
        
        
        ?>
    
    
    </body>

</html>