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
                $sql = "SELECT * FROM ANIMAL WHERE Sponsor ='"."' OR Sponsor IS NULL";
                $result =  $conn->query($sql);
                 if ($result->num_rows > 0) {
                    ?>
                    <tr>
                        <th>ANIMALS WITHOUT A SPONSOR</th>
                    </tr>
                    <table border = 3>
                        
                        <tr>
                            <th>Name</th>
                            <th>Age</th>
                            <th>Species</th>
                            <th>Caretaker</th>
                            <th>Sponsor</th>
                        </tr>
                    <?php
                    // output data of each row
                    while($row = $result->fetch_assoc()) {
                        ?>
                        <tr>
                            <td><?php echo $row["Name"]; ?></td>
                            <td><?php echo $row["Age"]; ?></td>
                            <td><?php echo $row["Species"]; ?></td>
                            <td><?php echo $row["Caretaker"]; ?></td>
                            <td><?php echo $row["Sponsor"]; ?></td>
                        </tr>
                        <?php
                    }

                    ?>
                    </table>
                    <?php
                    echo "<a href = 'homepage.php'>Back</a>";
                } else {
                    echo "No animals without sponsor!"."<br>";
                    echo "<a href = 'homepage.php'>Back</a>";
                }
            }
            $conn->close();
        
        
        ?>
    
    
    </body>

</html>