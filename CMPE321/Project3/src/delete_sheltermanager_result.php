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
                $sql = "DELETE FROM SHELTERMANAGER WHERE Username = '" . $_POST['Username'] . "'";

                if ($conn->query($sql) === TRUE) {
                    echo "Shelter manager deleted succesfully! <br />";
                    echo "<a href = 'homepage.php'>Back</a>";
                } else {
                    echo "Error deleting shelter manager: " . $conn->error;
                }
            }
            $conn->close();
        ?>

    </body>
</html>
