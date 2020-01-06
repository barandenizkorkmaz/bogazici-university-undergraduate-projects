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
                $sql = "UPDATE ANIMAL SET Name = '" . $_POST['Name'] . "', Age = '" . $_POST['Age'] . "', Species = '" . $_POST['Species'] . "', Caretaker = '" . $_POST['Caretaker'] . "', Sponsor = '" . $_POST['Sponsor'] . "' WHERE Name = '" . $_POST['oldName'] . "'";
                
                if ($conn->query($sql) === TRUE) {
                    echo "The animal updated succesfully! <br />";
                    echo "<a href = 'homepage.php'>Back</a>";
  
                    
                } else {
                    echo "Error updating record: " . $conn->error;
                }
            }
            $conn->close();
        
        ?>
    
    
    </body>

</html>