<html>
    <body>
    
        <?php
            $servername = "localhost";
            $username = "root";
            $password = "";
            $dbname = "sheltermanagerdb";

            // Create connection
            $conn = new mysqli($servername, $username, $password, $dbname);
        
            if ($conn->connect_error) {
                die("Connection failed: " . $conn->connect_error);
            }else{
                // Update the record
                $sql = "UPDATE SHELTERMANAGER SET Username = '" . $_POST['Username'] . "', Password = '" . $_POST['Password'] . "' WHERE Username = '" . $_POST['oldUsername'] . "'";
                
                if ($conn->query($sql) === TRUE) {
                    echo "The shelter manager updated succesfully! <br />";
                    echo "<a href = 'homepage.php'>Back</a>";
  
                    
                } else {
                    echo "Error updating record: " . $conn->error;
                }
            }
            $conn->close();
        
        ?>
    
    
    </body>

</html>