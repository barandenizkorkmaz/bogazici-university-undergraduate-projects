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
                
                $sql = "SELECT * FROM SHELTERMANAGER WHERE Username ='" . $_GET['id'] . "'";
                $result = $conn->query($sql);
                // If the record actually exists
                if ($result->num_rows > 0) {
                    ?>
                    <form action="update_sheltermanager_result.php" method="post">
                        
                    <?php

                    // Get the data
                    $row = $result->fetch_assoc();
                    ?>
                        <input type="hidden" name="oldUsername" value="<?php echo $row["Username"];?>">
                        <p>Username: <input type="text" name="Username" value = "<?php echo $row["Username"] ?>" /></p>
                        <p>Password: <input type="text" name="Password" value = "<?php echo $row["Password"] ?>" /></p>
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