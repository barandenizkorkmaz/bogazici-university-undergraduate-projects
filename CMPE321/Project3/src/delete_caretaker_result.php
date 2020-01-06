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

                // Update the record
                $sql = "DELETE FROM CARETAKER WHERE Name ='" . $_POST['Name'] . "'  AND Surname ='" . $_POST['Surname'] . "' AND Animal='" . $_POST['Animal'] . "'";

                if ($conn->query($sql) === TRUE) {
                    echo "Caretaker deleted succesfully! <br />";
                    echo "<a href = 'homepage.php'>Back</a>";
                } else {
                    echo "Error deleting caretaker: " . $conn->error;
                }
            }
            $conn->close();
        ?>

    </body>
</html>
