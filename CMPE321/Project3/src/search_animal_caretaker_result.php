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
                $sql = "SELECT * FROM CARETAKER WHERE Name ='" . $_POST['Name'] . "' AND Surname ='" . $_POST['Surname'] . "'";
                $result =  $conn->query($sql);
                 if ($result->num_rows > 0) {
                    ?>
                    <tr>
                        <th>ANIMALS of THE CARETAKER</th>
                    </tr>
                    <table border = 3>
                        
                        <tr>
                            <th>Options</th>
                            <th>Name</th>
                            <th>Surname</th>
                            <th>Animal</th>
                        </tr>
                    <?php
                    // output data of each row
                    while($row = $result->fetch_assoc()) {
                        ?>
                        <tr>
                            <td><?php echo $row["Name"]; ?></td>
                            <td><?php echo $row["Surname"]; ?></td>
                            <td><?php echo $row["Animal"]; ?></td>
                        </tr>
                        <?php
                    }

                    ?>
                    </table>
                    <?php
                    echo "<a href = 'homepage.php'>Back</a>";
                } else {
                    echo "No animals for the caretaker!"."<br>";
                    echo "<a href = 'homepage.php'>Back</a>";
                }
            }
            $conn->close();
        
        
        ?>
    
    
    </body>

</html>