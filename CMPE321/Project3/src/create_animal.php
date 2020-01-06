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
                <form action="create_animal_result.php" method="post">
                    <p>Name: <input type="text" name="Name" value = "" /></p>
                    <p>Age: <input type="number" name="Age" value = "" /></p>
                    <p>Species: <input type="text" name="Species" value = "" /></p>
                    <p>Caretaker: <input type="text" name="Caretaker" value = "" /></p>
                    <p>Sponsor: <input type="text" name="Sponsor" value = "" /></p>
                    <p><input type="submit" value = "Create Animal"/></p>
                </form>

            <?php
            }
            $conn->close();
        ?>
    
    </body>

</html>
