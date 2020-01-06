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
                echo "<a href = 'homepage.php'>Go back</a>";
                // Fetch the record
                $sql = "SELECT * FROM SHELTERMANAGER WHERE Username ='" . $_GET['id'] . "'";
                $result = $conn->query($sql);

                // If the record actually exists
                if ($result->num_rows > 0) {
                    ?>
                    <form action="delete_sheltermanager_result.php" method="post">
                    <?php

                    // Get the data
                    $row = $result->fetch_assoc();
                    ?>
                        Are you sure you want to delete the following record? <br />
                        <input type="hidden" name="oldUsername" value="<?php echo $row["Username"];?>">
                        <p>Username: <input type="text" name="Username" value = "<?php echo $row["Username"] ?>"readonly /></p>
                        <p>Password: <input type="text" name="Password" value = "<?php echo $row["Password"] ?>"readonly /></p>
                        <p><input type="submit" value = "Save Changes" /></p>
                    </form>
                    <?php
                } else {
                    echo "No such shelter manager exists!";
                }
            }
            $conn->close();

        
        ?>
        
    
    </body>


</html>