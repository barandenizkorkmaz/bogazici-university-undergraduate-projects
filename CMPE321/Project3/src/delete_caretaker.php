<html>
    <body>
        <?php
            $servername = "localhost";
            $username = "root";
            $password = "";
            $dbname = "sheltermanagerdb";
 
            $conn = new mysqli($servername, $username, $password, $dbname);
            
            if ($conn->connect_error) {
                die("Connection failed: " . $conn->connect_error);
            }else{
                echo "<a href = 'homepage.php'>Back</a>";
                // Fetch the record
                $sql = "SELECT * FROM CARETAKER WHERE Name ='" . $_GET['id'] . "'  AND Surname ='" . $_GET['id2'] . "' AND Animal='" . $_GET['id3'] . "'";
                $result = $conn->query($sql);

                // If the record actually exists
                if ($result->num_rows > 0) {
                    ?>
                    <form action="delete_caretaker_result.php" method="post">
                    <?php

                    // Get the data
                    $row = $result->fetch_assoc();
                    ?>
                        Are you sure you want to delete the following record? <br />
                        <input type="hidden" name="oldName" value="<?php echo $row["Name"];?>">
                        <p>Name: <input type="text" name="Name" value = "<?php echo $row["Name"] ?>"readonly /></p>
                        <p>Surname: <input type="text" name="Surname" value = "<?php echo $row["Surname"] ?>"readonly /></p>
                        <p>Animal: <input type="text" name="Animal" value = "<?php echo $row["Animal"] ?>"readonly /></p>
                        <p><input type="submit" value = "Save Changes" /></p>
                    </form>
                    <?php
                } else {
                    echo "No such caretaker exists!";
                }
            }
            $conn->close();

        
        ?>
        
    
    </body>


</html>