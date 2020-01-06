<html>
    <body>
        <?php
            $servername = "localhost";
            $username = "root";
            $password = "";
            $dbname = "sheltermanagerdb";
            //creating connection
            $conn = new mysqli($servername, $username, $password, $dbname);
        
            if ($conn->connect_error) {
                die("Connection failed: " . $conn->connect_error);
            }else{
                echo "<a href = 'homepage.php'>Go back</a>"."<br>";
                ?>
                <form action="create_sheltermanager_result.php" method="post">
                    <p>Username: <input type="text" name="Username" value = "" /></p>
                    <p>Password: <input type="text" name="Password" value = "" /></p>
                    <p><input type="submit" value = "Create Shelter Manager"/></p>
                </form>

            <?php
            }
            $conn->close();
        ?>
    
    </body>

</html>
