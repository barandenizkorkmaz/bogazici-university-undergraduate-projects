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
                <form action="view_animals_of_a_species_result.php" method="post">
                    <p>Species: <input type="text" name="Species" value = "" /></p>
                    <p><input type="submit" value = "Search Animals of The Species"/></p>
                </form>

            <?php
            }
            $conn->close();
        ?>
    
    </body>

</html>
