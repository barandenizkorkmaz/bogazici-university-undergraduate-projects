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
                $sql = "DELETE FROM ANIMAL WHERE Name = '" . $_POST['Name'] . "'";

                if ($conn->query($sql) === TRUE) {
                    echo "Animal deleted succesfully! <br />";
                    //Add necessary modifications!
                    echo "<a href = 'homepage.php'>Back</a>";
                } else {
                    echo "Error deleting animal: " . $conn->error;
                }
            }
            $conn->close();
        ?>

    </body>
</html>
