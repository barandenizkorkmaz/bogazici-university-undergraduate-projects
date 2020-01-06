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
                
                
                $sql = "SELECT * FROM CARETAKER WHERE Name ='" . $_GET['id'] . "'  AND Surname ='" . $_GET['id2'] . "' AND Animal='" . $_GET['id3'] . "'";
                $result = $conn->query($sql);
                // If the record actually exists
                if ($result->num_rows > 0) {
                    ?>
                    <form action="update_caretaker_result.php" method="post">
                        
                    <?php

                    // Get the data
                    $row = $result->fetch_assoc();
                    ?>
                        <input type="hidden" name="oldName" value="<?php echo $row["Name"];?>">
                        <input type="hidden" name="oldSurname" value="<?php echo $row["Surname"];?>">
                        <input type="hidden" name="oldAnimal" value="<?php echo $row["Animal"];?>">
                        <p>Name: <input type="text" name="Name" value = "<?php echo $row["Name"] ?>" /></p>
                        <p>Surname: <input type="text" name="Surname" value = "<?php echo $row["Surname"] ?>" /></p>
                        <p>Animal: <input type="text" name="Animal" value = "<?php echo $row["Animal"] ?>" /></p>
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