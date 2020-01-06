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
                $username = $_POST['Username'];
                $password = $_POST['Password'];
                
                $sql = "SELECT * FROM sheltermanager WHERE Username = '" . $username . "' AND Password = '" . $password . "'";
                $result =  $conn->query($sql);
                
                if($result->num_rows > 0){
                    session_start();
                    $_SESSION['username'] = $username;
                    
                    header("Location:http://localhost/2015400183/homepage.php");
                    die();
                }else{
                    $conn->close();
                    die("Please enter a valid username and password! Click <a href = 'login.php'>here</a> to log in.");
                }
            }
            $conn->close();
        
        ?>
    
    </body>
</html>