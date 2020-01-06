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
                echo "<a href = 'homepage.php'>Back</a>"."<br>";
                ?>
                <form action="search_animal_sponsor_result.php" method="post">
                    <p>Name: <input type="text" name="Name" value = "" /></p>
                    <p>Surname: <input type="text" name="Surname" value = "" /></p>
                    <p><input type="submit" value = "Search Animals"/></p>
                </form>

            <?php
            }
            $conn->close();
        ?>
    
    </body>

</html>
