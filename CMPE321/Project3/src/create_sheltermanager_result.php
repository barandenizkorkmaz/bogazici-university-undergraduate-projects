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
                $sql = "INSERT INTO SHELTERMANAGER(Username,Password) " .
                    "VALUES('" . $_POST['Username'] . "', '" . $_POST['Password'] . "')";

                if ($conn->query($sql) === TRUE) {
                    echo "New shelter manager added successfully <br />";
                    echo "<a href = 'homepage.php'>Back</a>";
                    
                       
                } else {
                    echo "<a href = 'homepage.php'>Back</a>"."<br>";
                    echo "Error creating record: " . $conn->error;
                }
                
            }
            $conn->close();
        
        
        ?>
    
    
    </body>

</html>