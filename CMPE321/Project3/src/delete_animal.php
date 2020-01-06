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
                $sql = "SELECT * FROM ANIMAL WHERE Name ='" . $_GET['id'] . "'";
                $result = $conn->query($sql);

                // If the record actually exists
                if ($result->num_rows > 0) {
                    ?>
                    <form action="delete_animal_result.php" method="post">
                    <?php

                    // Get the data
                    $row = $result->fetch_assoc();
                    ?>
                        Are you sure you want to delete the following record? <br />
                        <input type="hidden" name="oldName" value="<?php echo $row["Name"];?>">
                        <p>Name: <input type="text" name="Name" value = "<?php echo $row["Name"] ?>"readonly /></p>
                        <p>Age: <input type="number" name="Number" value = "<?php echo $row["Number"] ?>"readonly /></p>
                        <p>Species: <input type="text" name="Species" value = "<?php echo $row["Species"] ?>"readonly /></p>
                        <p>Caretaker: <input type="text" name="Caretaker" value = "<?php echo $row["Caretaker"] ?>"readonly /></p>
                        <p>Sponsor: <input type="text" name="Sponsor" value = "<?php echo $row["Sponsor"] ?>"readonly /></p>
                        <p><input type="submit" value = "Save Changes" /></p>
                    </form>
                    <?php
                } else {
                    echo "No such animal exists!";
                }
            }
            $conn->close();

        
        ?>
        
    
    </body>


</html>