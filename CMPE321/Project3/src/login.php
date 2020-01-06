<html>
    <body>
        <?php
            #these 5 variables are necessary in every php file.
            $servername = "localhost";
            $username = "root";
            $password = "";
            $dbname = "sheltermanagerdb"; #name of the database created in phpmyadmin.
            //creating connection
            $conn = new mysqli($servername, $username, $password, $dbname);
            
        
            if ($conn->connect_error) {
                die("Connection failed: " . $conn->connect_error);
            }else{
                ?>
                <form action="check.php" method="post">
                    <p>Username: <input type="text" name="Username" value = "" /></p>
                    <p>Password: <input type="password" name="Password" value = "" /></p>
                    <p><input type="submit" value = "Login"/></p>
                </form>
        
            <?php
            }
            $conn->close();
        
        ?>
    
    
    </body>
</html>