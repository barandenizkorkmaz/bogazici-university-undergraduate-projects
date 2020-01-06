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
                $sql = "UPDATE CARETAKER SET Name = '" . $_POST['Name'] . "', Surname = '" . $_POST['Surname'] . "', Animal = '" . $_POST['Animal'] . "' WHERE Name = '" . $_POST['oldName'] . "'
                AND Surname = '" . $_POST['oldSurname'] . "' AND Animal = '" . $_POST['oldAnimal'] . "'";
                
                if ($conn->query($sql) === TRUE) {
                    echo "The caretaker updated succesfully! <br />";
                    echo "<a href = 'homepage.php'>Back</a>";
  
                    
                } else {
                    echo "Error updating record: " . $conn->error;
                }
            }
            $conn->close();
        
        ?>
    
    
    </body>

</html>