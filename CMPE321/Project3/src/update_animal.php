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
                echo "<a href = 'homepage.php'>Back</a>";
                
                
                $sql = "SELECT * FROM ANIMAL WHERE Name ='" . $_GET['id'] . "'";
                $result = $conn->query($sql);
                // If the record actually exists
                if ($result->num_rows > 0) {
                    ?>
                    <form action="update_animal_result.php" method="post">
                        
                    <?php

                    // Get the data
                    $row = $result->fetch_assoc();
                    ?>
                        <input type="hidden" name="oldName" value="<?php echo $row["Name"];?>">
                        <p>Name: <input type="text" name="Name" value = "<?php echo $row["Name"] ?>" /></p>
                        <p>Age: <input type="number" name="Age" value = "<?php echo $row["Age"] ?>" /></p>
                        <p>Species: <input type="text" name="Species" value = "<?php echo $row["Species"] ?>" /></p>
                        <p>Caretaker: <input type="text" name="Caretaker" value = "<?php echo $row["Caretaker"] ?>" /></p>
                        <p>Sponsor: <input type="text" name="Sponsor" value = "<?php echo $row["Sponsor"] ?>" /></p>
                        <p><input type="submit" value = "Save Changes" /></p>
                    </form>
                    <?php
                } else {
                    echo "Record does not exist";
                }
            }
        
        
            $conn->close();
        ?>
    
    </body>


</html>